"""
SCM compatibility patch for torchao 0.18.0 + PyTorch 2.13.

PyTorch 2.13 natively supports Enum subclasses as opaque values under
torch.compile. torchao 0.18.0 still decorates two Enum classes with
register_as_pytree_constant(), which triggers deprecation warnings and
will become an error in a future PyTorch release.

This patch removes ONLY those two known decorators.

It is deliberately conservative:
- verifies torchao == 0.18.0
- checks exact expected source patterns
- is safe to run more than once
- refuses to modify unexpected source
"""

from importlib import metadata, util
from pathlib import Path
import sys


EXPECTED_TORCHAO_VERSION = "0.18.0"


PATCHES = [
    (
        Path("quantization/quantize_/common/kernel_preference.py"),
        "@register_as_pytree_constant\nclass KernelPreference(str, Enum):",
        "class KernelPreference(str, Enum):",
        "KernelPreference",
    ),
    (
        Path("prototype/mx_formats/config.py"),
        "@register_as_pytree_constant\nclass ScaleCalculationMode(Enum):",
        "class ScaleCalculationMode(Enum):",
        "ScaleCalculationMode",
    ),
]


def find_torchao_root() -> Path:
    spec = util.find_spec("torchao")

    if spec is None or spec.submodule_search_locations is None:
        raise RuntimeError("torchao is not installed in this Python environment.")

    return Path(next(iter(spec.submodule_search_locations)))


def patch_file(
    torchao_root: Path,
    relative_path: Path,
    old_text: str,
    new_text: str,
    label: str,
) -> None:
    path = torchao_root / relative_path

    if not path.exists():
        raise RuntimeError(f"{label}: expected file not found: {path}")

    text = path.read_text(encoding="utf-8")

    if old_text in text:
        path.write_text(text.replace(old_text, new_text, 1), encoding="utf-8")
        print(f"[PATCHED] {label}")
        return

    if new_text in text:
        print(f"[OK] {label} already patched")
        return

    raise RuntimeError(
        f"{label}: expected source pattern was not found.\n"
        "Refusing to modify an unexpected torchao source file."
    )


def main() -> int:
    installed_version = metadata.version("torchao")

    print(f"torchao version: {installed_version}")

    if installed_version != EXPECTED_TORCHAO_VERSION:
        print(
            f"[ERROR] This patch was validated only for torchao "
            f"{EXPECTED_TORCHAO_VERSION}."
        )
        print("Refusing to patch an unvalidated version.")
        return 1

    torchao_root = find_torchao_root()
    print(f"torchao location: {torchao_root}")

    for relative_path, old_text, new_text, label in PATCHES:
        patch_file(
            torchao_root,
            relative_path,
            old_text,
            new_text,
            label,
        )

    print("[OK] SCM torchao PyTree Enum compatibility patch complete.")
    return 0


if __name__ == "__main__":
    sys.exit(main())