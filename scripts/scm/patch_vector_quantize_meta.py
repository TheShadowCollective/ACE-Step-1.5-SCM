"""
SCM compatibility patch for vector-quantize-pytorch 1.31.1.

Purpose:
Make two constructor-time scalar operations meta-device safe under
modern Transformers / PyTorch model initialization.

Validated target:
    vector-quantize-pytorch == 1.31.1

Fixes:
1. ResidualFSQ:
   Replace tensor-based validation
       assert (levels_tensor > 1).all()
   with Python-level validation
       assert all(level > 1 for level in levels)

2. FSQ:
   Replace
       self.codebook_size = self._levels.prod().item()
   with
       self.codebook_size = prod(levels)

The patch is conservative and idempotent.
"""

from importlib import metadata, util
from pathlib import Path
import sys


EXPECTED_VERSION = "1.31.1"


def find_package_root() -> Path:
    spec = util.find_spec("vector_quantize_pytorch")

    if spec is None or spec.submodule_search_locations is None:
        raise RuntimeError(
            "vector_quantize_pytorch is not installed in this Python environment."
        )

    return Path(next(iter(spec.submodule_search_locations)))


def patch_residual_fsq(root: Path) -> None:
    path = root / "residual_fsq.py"
    text = path.read_text(encoding="utf-8")

    old_first = "levels_tensor = tensor(levels)"
    old_second = "assert (levels_tensor > 1).all()"

    new_first = "assert all(level > 1 for level in levels)"
    new_second = "levels_tensor = tensor(levels)"

    # Already patched
    new_first_pos = text.find(new_first)
    new_second_pos = text.find(new_second)

    if (
        new_first_pos != -1
        and new_second_pos != -1
        and new_first_pos < new_second_pos
    ):
        print("[OK] ResidualFSQ already patched")
        return

    # Pristine source
    old_first_pos = text.find(old_first)
    old_second_pos = text.find(old_second)

    if (
        old_first_pos != -1
        and old_second_pos != -1
        and old_first_pos < old_second_pos
    ):
        lines = text.splitlines()

        for i in range(len(lines) - 1):
            if (
                lines[i].strip() == old_first
                and lines[i + 1].strip() == old_second
            ):
                indent = lines[i][: len(lines[i]) - len(lines[i].lstrip())]

                lines[i] = indent + new_first
                lines[i + 1] = indent + new_second

                path.write_text(
                    "\n".join(lines) + "\n",
                    encoding="utf-8",
                )

                print("[PATCHED] ResidualFSQ meta-safe level validation")
                return

    raise RuntimeError(
        "ResidualFSQ: expected source pattern was not found. "
        "Refusing to modify unexpected source."
    )

def patch_fsq(root: Path) -> None:
    path = root / "finite_scalar_quantization.py"
    text = path.read_text(encoding="utf-8")

    old_line = "        self.codebook_size = self._levels.prod().item()"
    new_line = "        self.codebook_size = prod(levels)"

    if old_line in text:
        future_line = "from __future__ import annotations"

        if "from math import prod" not in text:
            if future_line not in text:
                raise RuntimeError(
                    "FSQ: __future__ import not found. "
                    "Refusing to modify unexpected source."
                )

            text = text.replace(
                future_line,
                future_line + "\n\nfrom math import prod",
                1,
            )

        text = text.replace(old_line, new_line, 1)
        path.write_text(text, encoding="utf-8")

        print("[PATCHED] FSQ meta-safe codebook size calculation")
        return

    if new_line in text:
        if "from math import prod" not in text:
            raise RuntimeError(
                "FSQ appears patched but required 'from math import prod' "
                "is missing."
            )

        print("[OK] FSQ already patched")
        return

    raise RuntimeError(
        "FSQ: expected source pattern was not found. "
        "Refusing to modify unexpected source."
    )


def main() -> int:
    installed_version = metadata.version("vector-quantize-pytorch")

    print(f"vector-quantize-pytorch version: {installed_version}")

    if installed_version != EXPECTED_VERSION:
        print(
            f"[ERROR] This patch was validated only for "
            f"vector-quantize-pytorch {EXPECTED_VERSION}."
        )
        print("Refusing to patch an unvalidated version.")
        return 1

    root = find_package_root()
    print(f"package location: {root}")

    patch_residual_fsq(root)
    patch_fsq(root)

    print("[OK] SCM vector-quantize meta compatibility patch complete.")
    return 0


if __name__ == "__main__":
    sys.exit(main())