"""
SCM compatibility patch for pytorch-wavelets 1.3.0.

Purpose:
Replace the legacy pkg_resources.resource_stream dependency with
Python's modern importlib.resources API.

Validated target:
pytorch-wavelets == 1.3.0

Fix:

    from pkg_resources import resource_stream

becomes:

    from importlib.resources import files

and:

    with resource_stream(
        'pytorch_wavelets.dtcwt.data',
        basename + '.npz'
    ) as f:

becomes:

    with files(
        'pytorch_wavelets.dtcwt.data'
    ).joinpath(
        basename + '.npz'
    ).open('rb') as f:

This keeps pytorch-wavelets compatible with modern setuptools
environments where pkg_resources is no longer available.

The patch is conservative and idempotent.
"""

from importlib import metadata, util
from pathlib import Path
import sys


EXPECTED_VERSION = "1.3.0"


def find_package_root() -> Path:
    spec = util.find_spec("pytorch_wavelets")

    if spec is None or spec.submodule_search_locations is None:
        raise RuntimeError(
            "pytorch_wavelets is not installed in this Python environment."
        )

    return Path(next(iter(spec.submodule_search_locations)))


def patch_coeffs(root: Path) -> None:
    path = root / "dtcwt" / "coeffs.py"
    text = path.read_text(encoding="utf-8")

    old_import = "from pkg_resources import resource_stream"
    new_import = "from importlib.resources import files"

    old_call = (
        "with resource_stream('pytorch_wavelets.dtcwt.data', "
        "basename + '.npz') as f:"
    )

    new_call = (
        "with files('pytorch_wavelets.dtcwt.data')"
        ".joinpath(basename + '.npz').open('rb') as f:"
    )

    # Already patched
    if new_import in text and new_call in text:
        print("[OK] pytorch-wavelets resource loading already patched")
        return

    # Refuse partially modified / unexpected source.
    if old_import not in text:
        raise RuntimeError(
            "pytorch-wavelets: expected pkg_resources import was not found. "
            "Refusing to modify unexpected source."
        )

    if old_call not in text:
        raise RuntimeError(
            "pytorch-wavelets: expected resource_stream call was not found. "
            "Refusing to modify unexpected source."
        )

    text = text.replace(old_import, new_import, 1)
    text = text.replace(old_call, new_call, 1)

    path.write_text(text, encoding="utf-8")

    print("[PATCHED] pytorch-wavelets modern importlib.resources compatibility")


def main() -> int:
    installed_version = metadata.version("pytorch-wavelets")

    print(f"pytorch-wavelets version: {installed_version}")

    if installed_version != EXPECTED_VERSION:
        print(
            f"[ERROR] This patch was validated only for "
            f"pytorch-wavelets {EXPECTED_VERSION}."
        )
        print("Refusing to patch an unvalidated version.")
        return 1

    root = find_package_root()
    print(f"package location: {root}")

    patch_coeffs(root)

    print("[OK] SCM pytorch-wavelets compatibility patch complete.")
    return 0


if __name__ == "__main__":
    sys.exit(main())