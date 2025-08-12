"""Package Janus for alpha/beta testing."""
from __future__ import annotations

import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / "dist"


def build() -> None:
    """Create a zip archive with source and data files."""
    DIST.mkdir(exist_ok=True)
    build_dir = DIST / "janus"
    if build_dir.exists():
        shutil.rmtree(build_dir)
    shutil.copytree(ROOT / "src", build_dir / "src")
    shutil.copytree(ROOT / "data", build_dir / "data")
    shutil.copy(ROOT / "README.md", build_dir / "README.md")
    shutil.make_archive(str(DIST / "janus_alpha"), "zip", build_dir)


if __name__ == "__main__":  # pragma: no cover - manual use
    build()
    print("Created dist/janus_alpha.zip")
