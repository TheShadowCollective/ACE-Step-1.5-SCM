"""Checkpoint and model-loading helpers for service initialization."""

import importlib
import os
from typing import Optional

import torch
from loguru import logger

from acestep import gpu_config
from .init_service_loader_components import InitServiceLoaderComponentsMixin


class InitServiceLoaderMixin(InitServiceLoaderComponentsMixin):
    """Helpers for heavy model component loading."""

    def _repair_vector_quantize_buffers(self) -> None:
        """Rebuild derived buffers corrupted by Transformers 5 meta initialization."""
        try:
            quantizer = self.model.tokenizer.quantizer
        except Exception:
            return

        try:
            levels = list(quantizer.levels)

            # -------------------------------------------------------------
            # ResidualFSQ scales
            # -------------------------------------------------------------

            levels_f32 = torch.tensor(
                levels,
                dtype=torch.float32,
                device=quantizer.scales.device,
            )

            quantizer.scales = torch.stack(
                [
                    levels_f32 ** -i
                    for i in range(quantizer.num_quantizers)
                ]
            )

            # -------------------------------------------------------------
            # ResidualFSQ soft clamp
            #
            # Original construction occurs in model dtype. For BF16 models
            # this rounding is significant and must be preserved.
            # -------------------------------------------------------------

            clamp_device = quantizer.soft_clamp_input_value.device

            levels_model_dtype = torch.tensor(
                levels,
                dtype=self.dtype,
                device=clamp_device,
            )

            one = torch.tensor(
                1.0,
                dtype=self.dtype,
                device=clamp_device,
            )

            quantizer.soft_clamp_input_value = (
                one + (one / (levels_model_dtype - one))
            )

            # -------------------------------------------------------------
            # FSQ layer derived buffers
            # -------------------------------------------------------------

            for fsq in quantizer.layers:
                device = fsq._basis.device

                fsq._levels = torch.tensor(
                    levels,
                    dtype=torch.int32,
                    device=device,
                )

                fsq._basis = torch.cumprod(
                    torch.tensor(
                        [1] + levels[:-1],
                        dtype=torch.int32,
                        device=device,
                    ),
                    dim=0,
                )

                if hasattr(fsq, "implicit_codebook"):
                    idx = torch.arange(
                        fsq.codebook_size,
                        device=device,
                    )

                    level_indices = fsq.indices_to_level_indices(idx).to(
                        self.dtype
                    )

                    level_values = fsq._levels.to(self.dtype)

                    two = torch.tensor(
                        2.0,
                        dtype=self.dtype,
                        device=device,
                    )

                    one = torch.tensor(
                        1.0,
                        dtype=self.dtype,
                        device=device,
                    )

                    fsq.implicit_codebook = (
                        level_indices
                        * (two / (level_values - one))
                        - one
                    )

            logger.warning(
                "[initialize_service] Rebuilt ResidualFSQ derived buffers after meta initialization"
            )

            # -------------------------------------------------------------
            # Qwen3 rotary embeddings
            #
            # Transformers 5 meta construction can leave persistent=False
            # RoPE buffers materialized with uninitialized data. Constructing
            # a fresh rotary module after loading produces the correct values.
            # -------------------------------------------------------------

            rotary_repairs = 0

            for module in self.model.modules():
                if module.__class__.__name__ != "Qwen3RotaryEmbedding":
                    continue

                device = module.inv_freq.device

                fresh_rotary = module.__class__(
                    config=self.model.config,
                    device=device,
                )

                module.inv_freq = fresh_rotary.inv_freq.to(device)

                if hasattr(module, "original_inv_freq"):
                    if hasattr(fresh_rotary, "original_inv_freq"):
                        module.original_inv_freq = (
                            fresh_rotary.original_inv_freq.to(device)
                        )
                    else:
                        module.original_inv_freq = module.inv_freq.clone()

                rotary_repairs += 1

            logger.warning(
                f"[initialize_service] Rebuilt {rotary_repairs} Qwen3 rotary embedding buffers after meta initialization"
            )

        except Exception as exc:
            logger.warning(
                f"[initialize_service] Derived buffer repair skipped: {exc}"
            )

    def _cuda_supports_bool_argsort(self) -> bool:
        """Return whether CUDA argsort supports bool tensors on the active device."""
        if not torch.cuda.is_available():
            return True
        target_device = str(getattr(self, "device", "cuda"))
        if not target_device.startswith("cuda"):
            target_device = "cuda"
        try:
            mask_cat = torch.tensor([[True, False]], device=target_device)
            _ = mask_cat.argsort(dim=1, descending=True, stable=True)
            return True
        except RuntimeError as exc:
            logger.debug(
                "[_cuda_supports_bool_argsort] Treating CUDA bool argsort probe failure as unsupported: {}",
                exc,
            )
            return False

    def _apply_cuda_bool_argsort_workaround(self) -> None:
        """Patch dynamic model helpers when bool argsort is unsupported on CUDA."""
        target_device = str(getattr(self, "device", ""))
        if not target_device.startswith("cuda"):
            return
        if self._cuda_supports_bool_argsort():
            return

        model_module_name = getattr(self.model.__class__, "__module__", "")
        if not model_module_name:
            return

        try:
            model_module = importlib.import_module(model_module_name)
        except Exception as exc:
            logger.warning(
                "[initialize_service] Failed to import model module for CUDA bool-argsort workaround: {}",
                exc,
            )
            return

        original_pack_sequences = getattr(model_module, "pack_sequences", None)
        if original_pack_sequences is None:
            return
        if getattr(original_pack_sequences, "__acestep_bool_argsort_patched__", False):
            return

        def _pack_sequences_cuda_compat(hidden1, hidden2, mask1, mask2):
            # ``pack_sequences`` only needs sortable integer-like masks here; keep
            # truthy/falsey semantics while avoiding CUDA bool argsort failures.
            if isinstance(mask1, torch.Tensor) and mask1.is_cuda and mask1.dtype == torch.bool:
                mask1 = mask1.to(torch.int32)
            if isinstance(mask2, torch.Tensor) and mask2.is_cuda and mask2.dtype == torch.bool:
                mask2 = mask2.to(torch.int32)
            return original_pack_sequences(hidden1, hidden2, mask1, mask2)

        _pack_sequences_cuda_compat.__acestep_bool_argsort_patched__ = True
        setattr(model_module, "pack_sequences", _pack_sequences_cuda_compat)
        logger.warning(
            "[initialize_service] Applied CUDA bool-argsort workaround to {}.pack_sequences",
            model_module_name,
        )

    @staticmethod
    def _build_quantization_config(quantization: str):
        """Return a torchao quantization config object for the requested mode."""
        if quantization == "int8_weight_only":
            from torchao.quantization import Int8WeightOnlyConfig
            return Int8WeightOnlyConfig()
        if quantization == "fp8_weight_only":
            from torchao.quantization import Float8WeightOnlyConfig
            return Float8WeightOnlyConfig()
        if quantization == "w8a8_dynamic":
            from torchao.quantization import Int8DynamicActivationInt8WeightConfig, MappingType
            return Int8DynamicActivationInt8WeightConfig(act_mapping_type=MappingType.ASYMMETRIC)
        raise ValueError(f"Unsupported quantization type: {quantization}")

    def _apply_dit_quantization(self, quantization: Optional[str]) -> None:
        """Apply torchao quantization to DiT linear layers when requested."""
        if quantization is None:
            return
        from torchao.quantization import quantize_
        from torchao.quantization.quant_api import _is_linear

        quant_config = self._build_quantization_config(quantization)
        def _dit_filter_fn(module, fqn):
            """Keep only decoder-side DiT linear layers and exclude tokenizers."""
            if not _is_linear(module, fqn):
                return False
            parts = fqn.split(".")
            if not parts or parts[0] != "decoder":
                return False
            for part in parts:
                if part in ("tokenizer", "detokenizer"):
                    return False
            return True

        quantize_(self.model, quant_config, filter_fn=_dit_filter_fn)
        logger.info(f"[initialize_service] DiT quantized with: {quantization}")

    def _load_main_model_from_checkpoint(
        self,
        *,
        model_checkpoint_path: str,
        device: str,
        use_flash_attention: bool,
        compile_model: bool,
        quantization: Optional[str],
    ) -> str:
        """Load DiT, apply compile/quantization options, and return selected attention backend."""
        from transformers import AutoModel

        if not os.path.exists(model_checkpoint_path):
            raise FileNotFoundError(f"ACE-Step V1.5 checkpoint not found at {model_checkpoint_path}")

        if torch.cuda.is_available():
            if getattr(self, "model", None) is not None:
                del self.model
                self.model = None
            torch.cuda.empty_cache()
            try:
                torch.cuda.synchronize()
            except RuntimeError as exc:
                logger.warning(
                    "[initialize_service] cuda.synchronize() failed during pre-load cleanup: {}. "
                    "Continuing with fresh load attempt.",
                    exc,
                )

        if use_flash_attention and self.is_flash_attention_available(device):
            attn_implementation = "flash_attention_2"
        elif device == "cuda" and not gpu_config.cuda_supports_bfloat16():
            # Pre-Ampere GPUs (compute capability < 8.0) run in float16 which
            # can overflow in SDPA's fused softmax with longer sequences,
            # producing NaN/Inf latents (see issues #924, #927).  Eager
            # attention upcasts to float32 for softmax, avoiding the overflow.
            logger.info(
                "[initialize_service] Pre-Ampere CUDA detected: using eager "
                "attention for float16 numerical stability."
            )
            attn_implementation = "eager"
        else:
            if use_flash_attention:
                logger.warning(
                    f"[initialize_service] Flash attention requested but unavailable for device={device}. "
                    "Falling back to SDPA."
                )
            attn_implementation = "sdpa"

        attn_candidates = [attn_implementation]
        if "sdpa" not in attn_candidates:
            attn_candidates.append("sdpa")
        if "eager" not in attn_candidates:
            attn_candidates.append("eager")

        last_attn_error = None
        self.model = None
        for candidate in attn_candidates:
            try:
                logger.info(f"[initialize_service] Attempting to load model with attention implementation: {candidate}")
                self.model = AutoModel.from_pretrained(
                    model_checkpoint_path,
                    trust_remote_code=True,
                    attn_implementation=candidate,
                    dtype=self.dtype,
                )
                attn_implementation = candidate
                break
            except Exception as exc:
                last_attn_error = exc
                logger.warning(f"[initialize_service] Failed to load model with {candidate}: {exc}")

        if self.model is None:
            raise RuntimeError(
                f"Failed to load model with attention implementations {attn_candidates}: {last_attn_error}"
            ) from last_attn_error

        self._repair_vector_quantize_buffers()
        self.model.config._attn_implementation = attn_implementation
        self.config = self.model.config
        self._sync_alignment_config()
        self._apply_cuda_bool_argsort_workaround()

        if not self.offload_to_cpu:
            self.model = self.model.to(device).to(self.dtype)
        elif not self.offload_dit_to_cpu:
            logger.info(f"[initialize_service] Keeping main model on {device} (persistent)")
            self.model = self.model.to(device).to(self.dtype)
        else:
            self.model = self.model.to("cpu").to(self.dtype)
        self.model.eval()

        if compile_model:
            self._ensure_len_for_compile(self.model, "model")
            self.model = torch.compile(self.model)
        self._apply_dit_quantization(quantization)

        silence_latent_path = os.path.join(model_checkpoint_path, "silence_latent.pt")
        if not os.path.exists(silence_latent_path):
            raise FileNotFoundError(f"Silence latent not found at {silence_latent_path}")
        self.silence_latent = torch.load(silence_latent_path, weights_only=True).transpose(1, 2)
        silence_latent_device = "cpu" if self.offload_to_cpu and self.offload_dit_to_cpu else device
        self.silence_latent = self.silence_latent.to(silence_latent_device).to(self.dtype)
        return attn_implementation
