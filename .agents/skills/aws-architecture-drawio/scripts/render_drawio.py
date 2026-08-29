#!/usr/bin/env python3
"""Export a draw.io diagram with an installed diagrams.net/draw.io CLI."""

from __future__ import annotations

import argparse
import os
from pathlib import Path
import shutil
import subprocess


MACOS_EXECUTABLES = (
    Path("/Applications/draw.io.app/Contents/MacOS/draw.io"),
    Path("/Applications/diagrams.net.app/Contents/MacOS/diagrams.net"),
)


def find_renderer() -> str | None:
    configured = os.environ.get("DRAWIO_EXECUTABLE")
    if configured and Path(configured).is_file():
        return configured

    for command in ("drawio", "diagrams.net"):
        if located := shutil.which(command):
            return located

    for candidate in MACOS_EXECUTABLES:
        if candidate.is_file():
            return str(candidate)
    return None


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("diagram", type=Path, nargs="?")
    parser.add_argument("--format", choices=("png", "svg", "pdf"), default="png")
    parser.add_argument("--output", type=Path)
    parser.add_argument(
        "--check",
        action="store_true",
        help="Report whether a compatible renderer is installed and exit",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    renderer = find_renderer()

    if args.check:
        if renderer:
            print(renderer)
            return 0
        print("No draw.io/diagrams.net CLI renderer found.")
        return 2

    if args.diagram is None:
        print("ERROR: diagram is required unless --check is used")
        return 2
    if not args.diagram.exists():
        print(f"ERROR: file not found: {args.diagram}")
        return 2
    if renderer is None:
        print("ERROR: no draw.io/diagrams.net CLI renderer found.")
        print("Install diagrams.net Desktop or set DRAWIO_EXECUTABLE to its CLI path.")
        return 2

    output = args.output or args.diagram.with_suffix(f".{args.format}")
    output.parent.mkdir(parents=True, exist_ok=True)
    command = [
        renderer,
        "--export",
        "--format",
        args.format,
        "--output",
        str(output),
        str(args.diagram),
    ]
    completed = subprocess.run(command, check=False)
    if completed.returncode != 0:
        print(f"ERROR: renderer exited with status {completed.returncode}")
        return completed.returncode
    if not output.exists() or output.stat().st_size == 0:
        print(f"ERROR: renderer did not create a usable output: {output}")
        return 1

    print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
