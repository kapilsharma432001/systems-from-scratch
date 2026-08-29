#!/usr/bin/env python3
"""Validate uncompressed draw.io XML used for AWS architecture diagrams."""

from __future__ import annotations

import argparse
from collections import Counter
from pathlib import Path
import re
import xml.etree.ElementTree as ET


AWS_ICON_RE = re.compile(r"resIcon=mxgraph\.aws4\.([^;]+)")
FONT_RE = re.compile(r"fontSize=(\d+(?:\.\d+)?)")
CATALOG_ROW_RE = re.compile(r"^\|[^|]+\|\s*`([^`]+)`\s*\|\s*$")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("diagram", type=Path)
    parser.add_argument(
        "--catalog",
        type=Path,
        default=Path(__file__).resolve().parent.parent
        / "references"
        / "aws4-common-shapes.md",
        help="Markdown table containing verified AWS4 resIcon names",
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Return a non-zero status when warnings are present",
    )
    return parser.parse_args()


def load_catalog(path: Path) -> set[str]:
    if not path.exists():
        raise ValueError(f"AWS4 catalog not found: {path}")

    names = {
        match.group(1)
        for line in path.read_text(encoding="utf-8").splitlines()
        if (match := CATALOG_ROW_RE.match(line))
    }
    if not names:
        raise ValueError(f"No AWS4 resIcon names found in catalog: {path}")
    return names


def number(value: str | None, default: float = 0.0) -> float:
    try:
        return float(value) if value is not None else default
    except ValueError:
        return default


def geometry(cell: ET.Element) -> tuple[float, float, float, float] | None:
    item = cell.find("mxGeometry")
    if item is None or item.get("relative") == "1":
        return None
    return (
        number(item.get("x")),
        number(item.get("y")),
        number(item.get("width")),
        number(item.get("height")),
    )


def is_node(cell: ET.Element) -> bool:
    if cell.get("vertex") != "1":
        return False
    style = cell.get("style", "")
    if "resIcon=mxgraph.aws4." in style:
        return True
    if style.startswith("text;") or "strokeColor=none" in style:
        return False
    return any(
        token in style
        for token in ("rounded=1", "shape=rhombus", "shape=cylinder", "shape=hexagon")
    )


def overlap_ratio(
    left: tuple[float, float, float, float],
    right: tuple[float, float, float, float],
) -> float:
    lx, ly, lw, lh = left
    rx, ry, rw, rh = right
    width = max(0.0, min(lx + lw, rx + rw) - max(lx, rx))
    height = max(0.0, min(ly + lh, ry + rh) - max(ly, ry))
    intersection = width * height
    smaller = min(lw * lh, rw * rh)
    return intersection / smaller if smaller > 0 else 0.0


def main() -> int:
    args = parse_args()
    if not args.diagram.exists():
        print(f"ERROR: file not found: {args.diagram}")
        return 2

    try:
        tree = ET.parse(args.diagram)
        verified_icons = load_catalog(args.catalog)
    except ET.ParseError as exc:
        print(f"ERROR: invalid XML: {exc}")
        return 1
    except ValueError as exc:
        print(f"ERROR: {exc}")
        return 2

    models = tree.findall(".//mxGraphModel")
    if not models:
        print("ERROR: no uncompressed mxGraphModel found")
        print("Compressed draw.io payloads must be opened and saved as uncompressed XML.")
        return 1

    cells = tree.findall(".//mxCell")
    ids = [cell_id for cell in cells if (cell_id := cell.get("id"))]
    id_set = set(ids)
    errors: list[str] = []
    warnings: list[str] = []

    duplicates = sorted(name for name, count in Counter(ids).items() if count > 1)
    if duplicates:
        errors.append("Duplicate cell IDs: " + ", ".join(duplicates))

    referenced_nodes: set[str] = set()
    aws_icons: list[str] = []

    for cell in cells:
        cell_id = cell.get("id", "<unknown>")
        style = cell.get("style", "")

        if cell.get("edge") == "1":
            source = cell.get("source")
            target = cell.get("target")
            if not source or not target:
                warnings.append(f"Edge {cell_id} has no explicit source or target")
            for field, reference in (("source", source), ("target", target)):
                if reference:
                    referenced_nodes.add(reference)
                    if reference not in id_set:
                        errors.append(
                            f"Edge {cell_id} has missing {field} reference: {reference}"
                        )

        if match := FONT_RE.search(style):
            if float(match.group(1)) < 12:
                warnings.append(f"Cell {cell_id} uses fontSize={match.group(1)}")

        if match := AWS_ICON_RE.search(style):
            icon_name = match.group(1)
            aws_icons.append(icon_name)
            if icon_name not in verified_icons:
                errors.append(
                    f"AWS icon {cell_id} uses unverified resIcon: {icon_name}"
                )

            box = geometry(cell)
            if box is not None:
                _, _, width, height = box
                if width and height and not (
                    48 <= width <= 96 and 48 <= height <= 96
                ):
                    warnings.append(
                        f"AWS icon {cell_id} is {width:g}x{height:g}; "
                        "check visual consistency"
                    )

    nodes = [cell for cell in cells if is_node(cell) and geometry(cell) is not None]
    for node in nodes:
        node_id = node.get("id", "<unknown>")
        if node_id not in referenced_nodes:
            warnings.append(f"Node {node_id} is disconnected")

    for index, left in enumerate(nodes):
        left_box = geometry(left)
        if left_box is None:
            continue
        for right in nodes[index + 1 :]:
            right_box = geometry(right)
            if right_box is None:
                continue
            if overlap_ratio(left_box, right_box) >= 0.10:
                warnings.append(
                    f"Nodes {left.get('id')} and {right.get('id')} likely overlap"
                )

    for model in models:
        page_width = number(model.get("pageWidth"))
        page_height = number(model.get("pageHeight"))
        if not page_width or not page_height:
            warnings.append("Diagram has no usable pageWidth/pageHeight")
            continue
        for cell in cells:
            if cell.get("vertex") != "1" or cell.get("parent") != "1":
                continue
            box = geometry(cell)
            if box is None:
                continue
            x, y, width, height = box
            if x < 0 or y < 0 or x + width > page_width or y + height > page_height:
                warnings.append(f"Cell {cell.get('id')} extends beyond the page bounds")

    edges = sum(1 for cell in cells if cell.get("edge") == "1")
    print(f"Parsed: {args.diagram.name}")
    print(
        f"Cells: {len(cells)} | AWS icons: {len(aws_icons)} | "
        f"Edges: {edges} | Layout nodes: {len(nodes)}"
    )

    for warning in sorted(set(warnings)):
        print("WARNING:", warning)
    for error in sorted(set(errors)):
        print("ERROR:", error)

    if errors:
        return 1
    if warnings and args.strict:
        return 1

    print("Structural and basic layout validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
