#!/usr/bin/env python3
"""Validate native Excalidraw structure and common diagram-layout hazards."""

from __future__ import annotations

import argparse
import json
import math
import sys
from collections import Counter
from pathlib import Path
from typing import Any


KNOWN_TYPES = {
    "rectangle",
    "ellipse",
    "diamond",
    "text",
    "arrow",
    "line",
    "freedraw",
    "image",
    "frame",
    "magicframe",
    "iframe",
    "embeddable",
}
NODE_TYPES = {"rectangle", "ellipse", "diamond", "image", "iframe", "embeddable"}
BINDABLE_TYPES = NODE_TYPES | {"text", "frame", "magicframe"}
BASE_FIELDS = {
    "angle",
    "strokeColor",
    "backgroundColor",
    "fillStyle",
    "strokeWidth",
    "strokeStyle",
    "roughness",
    "opacity",
    "groupIds",
    "frameId",
    "index",
    "roundness",
    "seed",
    "version",
    "versionNonce",
    "isDeleted",
    "boundElements",
    "updated",
    "link",
    "locked",
}


def finite(value: Any) -> bool:
    return isinstance(value, (int, float)) and not isinstance(value, bool) and math.isfinite(value)


def bbox(element: dict[str, Any]) -> tuple[float, float, float, float]:
    x = float(element["x"])
    y = float(element["y"])
    width = float(element["width"])
    height = float(element["height"])
    return min(x, x + width), min(y, y + height), max(x, x + width), max(y, y + height)


def overlap(a: tuple[float, float, float, float], b: tuple[float, float, float, float], tolerance: float = 2) -> bool:
    return min(a[2], b[2]) - max(a[0], b[0]) > tolerance and min(a[3], b[3]) - max(a[1], b[1]) > tolerance


def contains(outer: tuple[float, float, float, float], inner: tuple[float, float, float, float], tolerance: float = 2) -> bool:
    return (
        inner[0] >= outer[0] - tolerance
        and inner[1] >= outer[1] - tolerance
        and inner[2] <= outer[2] + tolerance
        and inner[3] <= outer[3] + tolerance
    )


def orientation(a: tuple[float, float], b: tuple[float, float], c: tuple[float, float]) -> float:
    return (b[1] - a[1]) * (c[0] - b[0]) - (b[0] - a[0]) * (c[1] - b[1])


def on_segment(a: tuple[float, float], b: tuple[float, float], c: tuple[float, float]) -> bool:
    return min(a[0], c[0]) <= b[0] <= max(a[0], c[0]) and min(a[1], c[1]) <= b[1] <= max(a[1], c[1])


def segments_intersect(
    p1: tuple[float, float], q1: tuple[float, float], p2: tuple[float, float], q2: tuple[float, float]
) -> bool:
    o1 = orientation(p1, q1, p2)
    o2 = orientation(p1, q1, q2)
    o3 = orientation(p2, q2, p1)
    o4 = orientation(p2, q2, q1)
    epsilon = 1e-9
    if o1 * o2 < -epsilon and o3 * o4 < -epsilon:
        return True
    if abs(o1) <= epsilon and on_segment(p1, p2, q1):
        return True
    if abs(o2) <= epsilon and on_segment(p1, q2, q1):
        return True
    if abs(o3) <= epsilon and on_segment(p2, p1, q2):
        return True
    if abs(o4) <= epsilon and on_segment(p2, q1, q2):
        return True
    return False


def segment_hits_box(
    start: tuple[float, float], end: tuple[float, float], rectangle: tuple[float, float, float, float]
) -> bool:
    left, top, right, bottom = rectangle
    if left < start[0] < right and top < start[1] < bottom:
        return True
    if left < end[0] < right and top < end[1] < bottom:
        return True
    corners = [(left, top), (right, top), (right, bottom), (left, bottom)]
    return any(
        segments_intersect(start, end, corners[index], corners[(index + 1) % 4])
        for index in range(4)
    )


def bound_ref_present(element: dict[str, Any], target_id: str, target_type: str) -> bool:
    refs = element.get("boundElements") or []
    return any(ref.get("id") == target_id and ref.get("type") == target_type for ref in refs if isinstance(ref, dict))


def intentional_overlap(element: dict[str, Any]) -> bool:
    custom = element.get("customData") or {}
    return bool(custom.get("allowOverlap")) or custom.get("role") in {"background", "overlay"}


class Report:
    def __init__(self) -> None:
        self.errors: list[tuple[str, str]] = []
        self.warnings: list[tuple[str, str]] = []

    def error(self, code: str, message: str) -> None:
        self.errors.append((code, message))

    def warn(self, code: str, message: str) -> None:
        self.warnings.append((code, message))


def validate(path: Path) -> tuple[Report, dict[str, int]]:
    report = Report()
    try:
        with path.open("r", encoding="utf-8") as handle:
            scene = json.load(handle)
    except (OSError, json.JSONDecodeError) as error:
        report.error("INVALID_JSON", str(error))
        return report, {}

    if not isinstance(scene, dict):
        report.error("INVALID_ROOT", "scene root must be a JSON object")
        return report, {}
    if scene.get("type") != "excalidraw":
        report.error("INVALID_TYPE", "top-level type must be 'excalidraw'")
    if scene.get("version") != 2:
        report.error("INVALID_VERSION", "top-level version must be 2")
    if not isinstance(scene.get("source"), str):
        report.warn("MISSING_SOURCE", "top-level source should be a string")
    if not isinstance(scene.get("appState"), dict):
        report.error("INVALID_APP_STATE", "top-level appState must be an object")
    if not isinstance(scene.get("files"), dict):
        report.error("INVALID_FILES", "top-level files must be an object")

    elements = scene.get("elements")
    if not isinstance(elements, list):
        report.error("INVALID_ELEMENTS", "top-level elements must be an array")
        return report, {}

    by_id: dict[str, dict[str, Any]] = {}
    order: dict[str, int] = {}
    active: list[dict[str, Any]] = []
    type_counts: Counter[str] = Counter()
    for index, raw in enumerate(elements):
        if not isinstance(raw, dict):
            report.error("INVALID_ELEMENT", f"element at index {index} is not an object")
            continue
        element_id = raw.get("id")
        element_type = raw.get("type")
        if not isinstance(element_id, str) or not element_id:
            report.error("MISSING_ID", f"element at index {index} has no valid id")
            continue
        if element_id in by_id:
            report.error("DUPLICATE_ID", f"duplicate element id: {element_id}")
            continue
        by_id[element_id] = raw
        order[element_id] = index
        if not isinstance(element_type, str):
            report.error("MISSING_ELEMENT_TYPE", f"element {element_id} has no valid type")
            continue
        type_counts[element_type] += 1
        if element_type not in KNOWN_TYPES:
            report.warn("UNKNOWN_ELEMENT_TYPE", f"element {element_id} uses unknown type {element_type}")
        for field in ("x", "y", "width", "height"):
            if not finite(raw.get(field)):
                report.error("INVALID_GEOMETRY", f"element {element_id}.{field} must be finite")
        if all(finite(raw.get(field)) for field in ("width", "height")):
            if raw["width"] < 0 or raw["height"] < 0:
                report.error("NEGATIVE_GEOMETRY", f"element {element_id} has negative width or height")
            if element_type not in {"arrow", "line", "freedraw", "text"} and (
                raw["width"] < 1 or raw["height"] < 1
            ):
                report.error("INVISIBLE_ELEMENT", f"element {element_id} is invisibly small")
        missing = sorted(BASE_FIELDS - raw.keys())
        if missing:
            report.warn("PARTIAL_ELEMENT", f"element {element_id} lacks full native fields: {', '.join(missing)}")
        opacity = raw.get("opacity")
        if finite(opacity) and not 0 <= opacity <= 100:
            report.error("INVALID_OPACITY", f"element {element_id} opacity must be between 0 and 100")
        if not isinstance(raw.get("groupIds", []), list):
            report.error("INVALID_GROUPS", f"element {element_id}.groupIds must be an array")
        if not raw.get("isDeleted", False):
            active.append(raw)

    files = scene.get("files") if isinstance(scene.get("files"), dict) else {}
    active_by_id = {element["id"]: element for element in active if isinstance(element.get("id"), str)}

    for element in active:
        element_id = element["id"]
        element_type = element.get("type")
        frame_id = element.get("frameId")
        if frame_id is not None:
            frame = active_by_id.get(frame_id)
            if not frame or frame.get("type") not in {"frame", "magicframe"}:
                report.error("INVALID_FRAME_REFERENCE", f"element {element_id} references missing frame {frame_id}")
            elif order.get(element_id, 0) > order.get(frame_id, 0):
                report.warn("FRAME_ORDER", f"frame child {element_id} should precede frame {frame_id} in scene order")

        refs = element.get("boundElements") or []
        if not isinstance(refs, list):
            report.error("INVALID_BOUND_ELEMENTS", f"element {element_id}.boundElements must be null or an array")
        else:
            for ref in refs:
                if not isinstance(ref, dict) or not isinstance(ref.get("id"), str):
                    report.error("INVALID_BOUND_REFERENCE", f"element {element_id} contains a malformed bound reference")
                    continue
                target = active_by_id.get(ref["id"])
                if target is None:
                    report.error("DANGLING_BOUND_REFERENCE", f"element {element_id} references missing {ref['id']}")
                elif ref.get("type") not in {"arrow", "text"}:
                    report.error("INVALID_BOUND_TYPE", f"element {element_id} has invalid bound type for {ref['id']}")

        if element_type == "text":
            required = {
                "text",
                "originalText",
                "fontSize",
                "fontFamily",
                "textAlign",
                "verticalAlign",
                "containerId",
                "autoResize",
                "lineHeight",
            }
            missing = sorted(required - element.keys())
            if missing:
                report.error("INVALID_TEXT", f"text {element_id} lacks: {', '.join(missing)}")
            if finite(element.get("fontSize")) and element["fontSize"] < 12:
                report.warn("SMALL_TEXT", f"text {element_id} uses fontSize {element['fontSize']}")
            container_id = element.get("containerId")
            if container_id is not None:
                container = active_by_id.get(container_id)
                if container is None:
                    report.error("MISSING_TEXT_CONTAINER", f"text {element_id} references missing container {container_id}")
                elif not bound_ref_present(container, element_id, "text"):
                    report.error("NONRECIPROCAL_TEXT_BINDING", f"container {container_id} does not reference text {element_id}")
                elif element_type == "text" and container.get("type") != "arrow":
                    if all(finite(element.get(field)) for field in ("x", "y", "width", "height")) and all(
                        finite(container.get(field)) for field in ("x", "y", "width", "height")
                    ) and not contains(bbox(container), bbox(element), 3):
                        report.warn("TEXT_OVERFLOW", f"text {element_id} extends outside container {container_id}")

        if element_type in {"arrow", "line"}:
            points = element.get("points")
            if not isinstance(points, list) or len(points) < 2:
                report.error("INVALID_POINTS", f"linear element {element_id} requires at least two points")
            elif any(
                not isinstance(point, list)
                or len(point) != 2
                or not all(finite(value) for value in point)
                for point in points
            ):
                report.error("INVALID_POINTS", f"linear element {element_id} contains malformed points")
            else:
                custom_data = element.get("customData") or {}
                segment_count = len(points) - 1
                if (
                    element_type == "arrow"
                    and segment_count > 1
                    and element.get("roundness") is not None
                    and not custom_data.get("allowCurvedRoute")
                ):
                    report.warn(
                        "ROUNDED_MULTISEGMENT_CONNECTOR",
                        f"connector {element_id} rounds a {segment_count}-segment route; "
                        "use roundness null or explicitly allow the curved route",
                    )
                if segment_count > 3 and not custom_data.get("allowComplexRoute"):
                    report.warn(
                        "COMPLEX_CONNECTOR",
                        f"connector {element_id} uses {segment_count} segments; "
                        "simplify it or explicitly allow the complex route",
                    )
            for binding_name in ("startBinding", "endBinding"):
                binding = element.get(binding_name)
                if binding is None:
                    continue
                if not isinstance(binding, dict) or not isinstance(binding.get("elementId"), str):
                    report.error("INVALID_BINDING", f"{element_id}.{binding_name} is malformed")
                    continue
                target_id = binding["elementId"]
                target = active_by_id.get(target_id)
                if target is None or target.get("type") not in BINDABLE_TYPES:
                    report.error("DANGLING_BINDING", f"{element_id}.{binding_name} references invalid target {target_id}")
                elif not bound_ref_present(target, element_id, "arrow"):
                    report.error("NONRECIPROCAL_ARROW_BINDING", f"target {target_id} does not reference arrow {element_id}")
                fixed_point = binding.get("fixedPoint")
                if fixed_point is not None:
                    if (
                        not isinstance(fixed_point, list)
                        or len(fixed_point) != 2
                        or not all(finite(value) and 0 <= value <= 1 for value in fixed_point)
                    ):
                        report.error("INVALID_FIXED_POINT", f"{element_id}.{binding_name}.fixedPoint must be two ratios")
                    if binding.get("mode") not in {"inside", "orbit", "skip"}:
                        report.error("INVALID_BIND_MODE", f"{element_id}.{binding_name}.mode is invalid")
                elif "focus" in binding or "gap" in binding:
                    report.warn("LEGACY_BINDING", f"{element_id}.{binding_name} uses legacy focus/gap binding fields")
                else:
                    report.error("INCOMPLETE_BINDING", f"{element_id}.{binding_name} lacks fixedPoint/mode")

        if element_type == "image":
            file_id = element.get("fileId")
            if not isinstance(file_id, str) or file_id not in files:
                report.error("MISSING_IMAGE_FILE", f"image {element_id} has no matching files entry")
            else:
                file_data = files[file_id]
                if not isinstance(file_data, dict) or not str(file_data.get("dataURL", "")).startswith("data:image/"):
                    report.error("INVALID_IMAGE_FILE", f"files entry {file_id} is not an embedded image data URL")

    nodes = [
        element
        for element in active
        if element.get("type") in NODE_TYPES
        and all(finite(element.get(field)) for field in ("x", "y", "width", "height"))
        and not intentional_overlap(element)
    ]
    for index, first in enumerate(nodes):
        for second in nodes[index + 1 :]:
            groups_a = set(first.get("groupIds") or [])
            groups_b = set(second.get("groupIds") or [])
            if groups_a & groups_b:
                continue
            if overlap(bbox(first), bbox(second), 3):
                report.warn("NODE_OVERLAP", f"nodes {first['id']} and {second['id']} overlap")

    text_elements = [
        element
        for element in active
        if element.get("type") == "text"
        and all(finite(element.get(field)) for field in ("x", "y", "width", "height"))
        and not intentional_overlap(element)
    ]
    for text in text_elements:
        container_id = text.get("containerId")
        arrow_endpoint_ids: set[str] = set()
        if container_id in active_by_id and active_by_id[container_id].get("type") == "arrow":
            arrow = active_by_id[container_id]
            for binding_name in ("startBinding", "endBinding"):
                binding = arrow.get(binding_name) or {}
                if isinstance(binding.get("elementId"), str):
                    arrow_endpoint_ids.add(binding["elementId"])
        for node in nodes:
            if node["id"] == container_id or node["id"] in arrow_endpoint_ids:
                continue
            if set(text.get("groupIds") or []) & set(node.get("groupIds") or []):
                continue
            if overlap(bbox(text), bbox(node), 2):
                report.warn("TEXT_NODE_OVERLAP", f"text {text['id']} overlaps node {node['id']}")

    for arrow in [element for element in active if element.get("type") in {"arrow", "line"}]:
        points = arrow.get("points")
        if not isinstance(points, list) or len(points) < 2 or any(
            not isinstance(point, list) or len(point) != 2 or not all(finite(value) for value in point)
            for point in points
        ):
            continue
        absolute = [(float(arrow.get("x", 0)) + point[0], float(arrow.get("y", 0)) + point[1]) for point in points]
        endpoint_ids = {
            binding.get("elementId")
            for binding in (arrow.get("startBinding"), arrow.get("endBinding"))
            if isinstance(binding, dict)
        }
        for node in nodes:
            if node["id"] in endpoint_ids:
                continue
            left, top, right, bottom = bbox(node)
            if right - left > 8 and bottom - top > 8:
                inner = (left + 3, top + 3, right - 3, bottom - 3)
            else:
                inner = (left, top, right, bottom)
            if any(segment_hits_box(start, end, inner) for start, end in zip(absolute, absolute[1:])):
                report.warn("ROUTE_NODE_INTERSECTION", f"connector {arrow['id']} crosses node {node['id']}")

    frames = {
        element["id"]: element
        for element in active
        if element.get("type") in {"frame", "magicframe"}
        and all(finite(element.get(field)) for field in ("x", "y", "width", "height"))
    }
    for element in active:
        frame_id = element.get("frameId")
        if frame_id in frames and element.get("type") not in {"arrow", "line", "freedraw"}:
            if all(finite(element.get(field)) for field in ("x", "y", "width", "height")) and not contains(
                bbox(frames[frame_id]), bbox(element), 2
            ):
                report.warn("FRAME_OVERFLOW", f"element {element['id']} extends outside frame {frame_id}")

    font_families = {
        element.get("fontFamily") for element in active if element.get("type") == "text" and finite(element.get("fontFamily"))
    }
    if len(font_families) > 2:
        report.warn("TOO_MANY_FONTS", f"scene uses {len(font_families)} font families: {sorted(font_families)}")
    fills = {
        element.get("backgroundColor")
        for element in active
        if element.get("backgroundColor") not in {None, "transparent", "#ffffff", "#FFFFFF"}
    }
    if len(fills) > 6:
        report.warn("TOO_MANY_FILLS", f"scene uses {len(fills)} non-transparent fill colors")

    counts = dict(sorted(type_counts.items()))
    counts["active"] = len(active)
    counts["total"] = len(elements)
    return report, counts


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("scene", type=Path, help=".excalidraw file to validate")
    parser.add_argument("--strict", action="store_true", help="fail when any warning is present")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    report, counts = validate(args.scene)
    if counts:
        breakdown = ", ".join(f"{key}={value}" for key, value in counts.items())
        print(f"Parsed: {args.scene}")
        print(f"Elements: {breakdown}")
    for code, message in report.errors:
        print(f"ERROR [{code}]: {message}")
    for code, message in report.warnings:
        print(f"WARNING [{code}]: {message}")
    if report.errors:
        print(f"FAIL: {len(report.errors)} error(s), {len(report.warnings)} warning(s)")
        return 1
    if args.strict and report.warnings:
        print(f"FAIL (strict): {len(report.warnings)} warning(s)")
        return 2
    print(f"PASS: {len(report.warnings)} warning(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
