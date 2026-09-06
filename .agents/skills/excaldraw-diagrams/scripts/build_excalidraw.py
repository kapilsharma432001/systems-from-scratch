#!/usr/bin/env python3
"""Build a conservative native Excalidraw v2 scene from an explicit JSON spec.

The builder has no third-party dependencies. It deliberately handles layout as
data instead of trying to guess a graph layout; see references/spec-format.md.
"""

from __future__ import annotations

import argparse
import base64
import hashlib
import json
import math
import mimetypes
import sys
import textwrap
from pathlib import Path
from typing import Any, Iterable


INK = "#1e1e1e"
WHITE = "#ffffff"

PALETTE: dict[str, dict[str, str]] = {
    "primary": {"fill": "#dbe4ff", "stroke": "#364fc7", "text": INK},
    "secondary": {"fill": "#e5dbff", "stroke": "#7048e8", "text": INK},
    "success": {"fill": "#d3f9d8", "stroke": "#2b8a3e", "text": INK},
    "warning": {"fill": "#fff3bf", "stroke": "#e67700", "text": INK},
    "danger": {"fill": "#ffe3e3", "stroke": "#c92a2a", "text": INK},
    "data": {"fill": "#e3fafc", "stroke": "#0b7285", "text": INK},
    "neutral": {"fill": "#f1f3f5", "stroke": "#495057", "text": INK},
    "muted": {"fill": "transparent", "stroke": "#868e96", "text": "#495057"},
    "ink": {"fill": INK, "stroke": INK, "text": INK},
    "dashed": {"fill": "transparent", "stroke": "#868e96", "text": "#495057"},
}

SHAPE_TYPES = {"rectangle", "ellipse", "diamond"}
IMAGE_MIMES = {
    "image/png",
    "image/jpeg",
    "image/webp",
    "image/gif",
    "image/bmp",
    "image/svg+xml",
}
SIDE_FIXED_POINT = {
    "left": [0.0, 0.5],
    "right": [1.0, 0.5],
    "top": [0.5, 0.0],
    "bottom": [0.5, 1.0],
}


def stable_int(value: str, salt: str = "") -> int:
    digest = hashlib.sha256(f"{salt}:{value}".encode("utf-8")).digest()
    return int.from_bytes(digest[:4], "big") % 2_147_483_646 + 1


def is_finite_number(value: Any) -> bool:
    return isinstance(value, (int, float)) and not isinstance(value, bool) and math.isfinite(value)


def pairwise(values: list[list[float]]) -> Iterable[tuple[list[float], list[float]]]:
    return zip(values, values[1:])


class SceneBuilder:
    def __init__(self, spec: dict[str, Any], spec_path: Path) -> None:
        self.spec = spec
        self.spec_path = spec_path
        canvas = spec.get("canvas", {})
        defaults = spec.get("defaults", {})
        self.grid = canvas.get("gridSize", 20)
        if self.grid is None:
            self.grid = 0
        if not is_finite_number(self.grid) or self.grid < 0:
            raise ValueError("canvas.gridSize must be null or a non-negative number")
        self.snap_enabled = bool(spec.get("snapToGrid", True)) and self.grid > 0
        self.default_font = int(defaults.get("fontFamily", 5))
        self.default_font_size = float(defaults.get("fontSize", 20))
        self.default_line_height = float(defaults.get("lineHeight", 1.25))
        self.default_roughness = float(defaults.get("roughness", 1))
        self.default_stroke_width = float(defaults.get("strokeWidth", 2))
        self.default_fill_style = str(defaults.get("fillStyle", "solid"))
        self.default_edge_route = str(defaults.get("edgeRoute", "straight"))
        if self.default_edge_route not in {"straight", "orthogonal"}:
            raise ValueError("defaults.edgeRoute must be 'straight' or 'orthogonal'")
        self.default_edge_roundness = defaults.get("edgeRoundness")
        if self.default_edge_roundness is not None and not isinstance(self.default_edge_roundness, dict):
            raise ValueError("defaults.edgeRoundness must be null or an Excalidraw roundness object")
        self.default_edge_roughness = float(defaults.get("edgeRoughness", 0))
        if not 0 <= self.default_edge_roughness <= 2:
            raise ValueError("defaults.edgeRoughness must be between 0 and 2")
        self.files: dict[str, dict[str, Any]] = {}
        self.used_ids: set[str] = set()
        self.by_id: dict[str, dict[str, Any]] = {}
        self.node_boxes: dict[str, tuple[float, float, float, float]] = {}
        self.node_frame: dict[str, str | None] = {}
        self.layers: dict[str, list[dict[str, Any]]] = {
            "edges": [],
            "nodes": [],
            "labels": [],
            "annotations": [],
            "frames": [],
        }

    def snap(self, value: float) -> float:
        if not self.snap_enabled:
            return round(float(value), 2)
        return round(round(float(value) / self.grid) * self.grid, 2)

    def require_id(self, raw: Any, context: str) -> str:
        if not isinstance(raw, str) or not raw.strip():
            raise ValueError(f"{context} requires a non-empty string id")
        element_id = raw.strip()
        if element_id in self.used_ids:
            raise ValueError(f"duplicate element id: {element_id}")
        self.used_ids.add(element_id)
        return element_id

    def reserve_generated_id(self, preferred: str) -> str:
        candidate = preferred
        suffix = 2
        while candidate in self.used_ids:
            candidate = f"{preferred}-{suffix}"
            suffix += 1
        self.used_ids.add(candidate)
        return candidate

    def number(self, item: dict[str, Any], key: str, default: float | None = None) -> float:
        value = item.get(key, default)
        if not is_finite_number(value):
            raise ValueError(f"{item.get('id', 'element')}.{key} must be a finite number")
        return float(value)

    def style(self, item: dict[str, Any], default_role: str = "neutral") -> dict[str, str]:
        role = str(item.get("style", default_role))
        if role not in PALETTE:
            raise ValueError(f"unknown semantic style '{role}' on {item.get('id', 'element')}")
        return PALETTE[role]

    def base(
        self,
        element_id: str,
        element_type: str,
        x: float,
        y: float,
        width: float,
        height: float,
        item: dict[str, Any],
        *,
        default_role: str = "neutral",
        default_roundness: dict[str, int] | None = None,
    ) -> dict[str, Any]:
        role = self.style(item, default_role)
        element = {
            "id": element_id,
            "type": element_type,
            "x": round(x, 2),
            "y": round(y, 2),
            "width": round(width, 2),
            "height": round(height, 2),
            "angle": float(item.get("angle", 0)),
            "strokeColor": item.get("strokeColor", role["stroke"]),
            "backgroundColor": item.get("backgroundColor", role["fill"]),
            "fillStyle": item.get("fillStyle", self.default_fill_style),
            "strokeWidth": float(item.get("strokeWidth", self.default_stroke_width)),
            "strokeStyle": item.get("strokeStyle", "dashed" if item.get("style") == "dashed" else "solid"),
            "roughness": float(item.get("roughness", self.default_roughness)),
            "opacity": float(item.get("opacity", 100)),
            "groupIds": list(item.get("groupIds", [])),
            "frameId": item.get("frameId"),
            "index": None,
            "roundness": item.get("roundness", default_roundness),
            "seed": stable_int(element_id, "seed"),
            "version": 1,
            "versionNonce": stable_int(element_id, "nonce"),
            "isDeleted": False,
            "boundElements": [],
            "updated": 0,
            "link": item.get("link"),
            "locked": bool(item.get("locked", False)),
        }
        if "customData" in item:
            element["customData"] = item["customData"]
        return element

    @staticmethod
    def font_width_factor(font_family: int, text: str) -> float:
        if any(ord(char) >= 0x2E80 for char in text):
            return 1.0
        if font_family in {3, 8}:
            return 0.62
        if font_family in {6, 9, 10}:
            return 0.55
        return 0.58

    def wrap_text(self, value: str, font_size: float, max_width: float, font_family: int) -> str:
        factor = self.font_width_factor(font_family, value)
        max_chars = max(1, int(max_width / max(font_size * factor, 1)))
        result: list[str] = []
        for paragraph in value.splitlines() or [""]:
            if not paragraph:
                result.append("")
                continue
            lines = textwrap.wrap(
                paragraph,
                width=max_chars,
                break_long_words=True,
                break_on_hyphens=True,
                replace_whitespace=False,
                drop_whitespace=True,
            )
            result.extend(lines or [""])
        return "\n".join(result)

    def measure_text(self, value: str, font_size: float, font_family: int, line_height: float) -> tuple[float, float]:
        lines = value.splitlines() or [""]
        factor = self.font_width_factor(font_family, value)
        width = max(1.0, max(len(line) for line in lines) * font_size * factor)
        height = max(1.0, len(lines) * font_size * line_height)
        return round(width, 2), round(height, 2)

    def make_text(
        self,
        element_id: str,
        value: str,
        x: float,
        y: float,
        item: dict[str, Any],
        *,
        width_limit: float | None = None,
        height_limit: float | None = None,
        container_id: str | None = None,
        frame_id: str | None = None,
        default_role: str = "neutral",
    ) -> dict[str, Any]:
        if not isinstance(value, str) or not value.strip():
            raise ValueError(f"text element {element_id} requires non-empty text")
        role = self.style(item, default_role)
        font_family = int(item.get("fontFamily", self.default_font))
        font_size = float(item.get("fontSize", self.default_font_size))
        min_font_size = float(item.get("minFontSize", 12))
        line_height = float(item.get("lineHeight", self.default_line_height))
        original = value
        while True:
            rendered = self.wrap_text(original, font_size, width_limit, font_family) if width_limit else original
            text_width, text_height = self.measure_text(rendered, font_size, font_family, line_height)
            if (width_limit is None or text_width <= width_limit + 0.5) and (
                height_limit is None or text_height <= height_limit + 0.5
            ):
                break
            font_size -= 1
            if font_size < min_font_size:
                raise ValueError(
                    f"text '{original}' does not fit its container; enlarge the node or shorten the label"
                )

        text_item = dict(item)
        text_item["style"] = item.get("style", default_role)
        text_item["backgroundColor"] = "transparent"
        text_item["strokeColor"] = item.get("textColor", role["text"])
        text_item["strokeWidth"] = item.get("textStrokeWidth", 1)
        text_item["roughness"] = item.get("textRoughness", item.get("roughness", self.default_roughness))
        text_item["roundness"] = None
        text_item["frameId"] = frame_id
        text = self.base(element_id, "text", x, y, text_width, text_height, text_item, default_role=default_role)
        text.update(
            {
                "text": rendered,
                "fontSize": round(font_size, 2),
                "fontFamily": font_family,
                "textAlign": item.get("textAlign", "center" if container_id else "left"),
                "verticalAlign": item.get("verticalAlign", "middle" if container_id else "top"),
                "containerId": container_id,
                "originalText": original,
                "autoResize": True,
                "lineHeight": line_height,
            }
        )
        return text

    def add_bound_reference(self, target_id: str, bound_id: str, bound_type: str) -> None:
        target = self.by_id[target_id]
        refs = target.setdefault("boundElements", [])
        if not any(ref.get("id") == bound_id for ref in refs):
            refs.append({"id": bound_id, "type": bound_type})

    def build_frames(self) -> None:
        for raw in self.spec.get("frames", []):
            if not isinstance(raw, dict):
                raise ValueError("each frame must be an object")
            frame_id = self.require_id(raw.get("id"), "frame")
            x = self.snap(self.number(raw, "x"))
            y = self.snap(self.number(raw, "y"))
            width = self.snap(self.number(raw, "width"))
            height = self.snap(self.number(raw, "height"))
            if width <= 0 or height <= 0:
                raise ValueError(f"frame {frame_id} must have positive width and height")
            item = dict(raw)
            item["frameId"] = raw.get("parentFrameId")
            item.setdefault("style", "muted")
            item.setdefault("backgroundColor", "transparent")
            item.setdefault("roughness", 0)
            frame = self.base(frame_id, "frame", x, y, width, height, item, default_role="muted")
            frame["name"] = raw.get("name")
            self.by_id[frame_id] = frame
            self.node_boxes[frame_id] = (x, y, width, height)
            self.node_frame[frame_id] = item.get("frameId")
            self.layers["frames"].append(frame)

    def build_shape_node(self, raw: dict[str, Any], node_type: str, *, layer: str = "nodes") -> None:
        node_id = self.require_id(raw.get("id"), "node")
        x = self.snap(self.number(raw, "x"))
        y = self.snap(self.number(raw, "y"))
        width = self.snap(self.number(raw, "width", 200))
        height = self.snap(self.number(raw, "height", 100))
        if width <= 0 or height <= 0:
            raise ValueError(f"node {node_id} must have positive width and height")
        roundness = {"type": 3} if node_type == "rectangle" else ({"type": 2} if node_type == "diamond" else None)
        node = self.base(node_id, node_type, x, y, width, height, raw, default_roundness=roundness)
        self.by_id[node_id] = node
        self.node_boxes[node_id] = (x, y, width, height)
        self.node_frame[node_id] = raw.get("frameId")
        self.layers[layer].append(node)

        label = raw.get("label")
        if label is not None:
            label_id = self.reserve_generated_id(str(raw.get("labelId", f"{node_id}__label")))
            padding = float(raw.get("padding", 16))
            text = self.make_text(
                label_id,
                str(label),
                0,
                0,
                raw,
                width_limit=max(1, width - 2 * padding),
                height_limit=max(1, height - 2 * padding),
                container_id=node_id,
                frame_id=raw.get("frameId"),
            )
            if text["textAlign"] == "left":
                text["x"] = round(x + padding, 2)
            elif text["textAlign"] == "right":
                text["x"] = round(x + width - padding - text["width"], 2)
            else:
                text["x"] = round(x + (width - text["width"]) / 2, 2)
            if text["verticalAlign"] == "top":
                text["y"] = round(y + padding, 2)
            elif text["verticalAlign"] == "bottom":
                text["y"] = round(y + height - padding - text["height"], 2)
            else:
                text["y"] = round(y + (height - text["height"]) / 2, 2)
            self.by_id[label_id] = text
            self.add_bound_reference(node_id, label_id, "text")
            self.layers["labels"].append(text)

    def build_text_node(self, raw: dict[str, Any], *, layer: str = "annotations") -> None:
        text_id = self.require_id(raw.get("id"), "text")
        x = self.snap(self.number(raw, "x"))
        y = self.snap(self.number(raw, "y"))
        value = raw.get("text", raw.get("label"))
        width_limit = raw.get("width")
        if width_limit is not None:
            width_limit = self.number(raw, "width")
        item = dict(raw)
        item.setdefault("style", "muted")
        custom = dict(item.get("customData", {}))
        custom.setdefault("role", "annotation")
        item["customData"] = custom
        text = self.make_text(
            text_id,
            str(value) if value is not None else "",
            x,
            y,
            item,
            width_limit=width_limit,
            frame_id=raw.get("frameId"),
            default_role=item["style"],
        )
        self.by_id[text_id] = text
        self.node_boxes[text_id] = (text["x"], text["y"], text["width"], text["height"])
        self.node_frame[text_id] = raw.get("frameId")
        self.layers[layer].append(text)

    def build_image_node(self, raw: dict[str, Any], *, layer: str = "nodes") -> None:
        node_id = self.require_id(raw.get("id"), "image")
        x = self.snap(self.number(raw, "x"))
        y = self.snap(self.number(raw, "y"))
        width = self.snap(self.number(raw, "width"))
        height = self.snap(self.number(raw, "height"))
        if width <= 0 or height <= 0:
            raise ValueError(f"image {node_id} must have positive width and height")
        raw_path = raw.get("path")
        if not isinstance(raw_path, str) or not raw_path:
            raise ValueError(f"image {node_id} requires path")
        image_path = Path(raw_path).expanduser()
        if not image_path.is_absolute():
            image_path = (self.spec_path.parent / image_path).resolve()
        data = image_path.read_bytes()
        mime_type = mimetypes.guess_type(image_path.name)[0]
        if mime_type not in IMAGE_MIMES:
            raise ValueError(f"unsupported image MIME type for {image_path}: {mime_type}")
        file_id = hashlib.sha256(data).hexdigest()[:40]
        self.files[file_id] = {
            "id": file_id,
            "mimeType": mime_type,
            "dataURL": f"data:{mime_type};base64,{base64.b64encode(data).decode('ascii')}",
            "created": 0,
            "lastRetrieved": 0,
        }
        item = dict(raw)
        item.setdefault("backgroundColor", "transparent")
        image = self.base(node_id, "image", x, y, width, height, item, default_roundness={"type": 3})
        image.update({"fileId": file_id, "status": "saved", "scale": [1, 1], "crop": None})
        self.by_id[node_id] = image
        self.node_boxes[node_id] = (x, y, width, height)
        self.node_frame[node_id] = raw.get("frameId")
        self.layers[layer].append(image)

        if raw.get("label"):
            group_ids = image["groupIds"]
            if not group_ids:
                group_ids.append(self.reserve_generated_id(f"{node_id}__group"))
            label_id = self.reserve_generated_id(str(raw.get("labelId", f"{node_id}__label")))
            label_item = dict(raw)
            label_item["groupIds"] = list(group_ids)
            label_item.setdefault("textAlign", "center")
            text = self.make_text(
                label_id,
                str(raw["label"]),
                x,
                y + height + 12,
                label_item,
                width_limit=max(width, 120),
                frame_id=raw.get("frameId"),
            )
            text["x"] = round(x + (width - text["width"]) / 2, 2)
            self.by_id[label_id] = text
            self.layers["labels"].append(text)

    def build_badge(self, raw: dict[str, Any], *, layer: str = "annotations") -> None:
        item = dict(raw)
        item["type"] = "ellipse"
        item.setdefault("width", 32)
        item.setdefault("height", 32)
        item.setdefault("style", "ink")
        item.setdefault("fontSize", 16)
        item.setdefault("padding", 4)
        item.setdefault("textColor", WHITE)
        item["label"] = str(raw.get("label", raw.get("text", "")))
        self.build_shape_node(item, "ellipse", layer=layer)

    def build_nodes(self) -> None:
        for raw in self.spec.get("nodes", []):
            self.build_node(raw, "nodes")
        for raw in self.spec.get("annotations", []):
            self.build_node(raw, "annotations")

    def build_node(self, raw: Any, layer: str) -> None:
        if not isinstance(raw, dict):
            raise ValueError("each node or annotation must be an object")
        node_type = str(raw.get("type", "rectangle"))
        if node_type in SHAPE_TYPES:
            self.build_shape_node(raw, node_type, layer=layer)
        elif node_type == "text":
            self.build_text_node(raw, layer=layer)
        elif node_type == "badge":
            self.build_badge(raw, layer=layer)
        elif node_type == "image":
            self.build_image_node(raw, layer=layer)
        else:
            raise ValueError(f"unsupported node type: {node_type}")

    @staticmethod
    def center(box: tuple[float, float, float, float]) -> tuple[float, float]:
        x, y, width, height = box
        return x + width / 2, y + height / 2

    @staticmethod
    def choose_sides(
        source: tuple[float, float, float, float], target: tuple[float, float, float, float]
    ) -> tuple[str, str]:
        sx, sy = SceneBuilder.center(source)
        tx, ty = SceneBuilder.center(target)
        if abs(tx - sx) >= abs(ty - sy):
            return ("right", "left") if tx >= sx else ("left", "right")
        return ("bottom", "top") if ty >= sy else ("top", "bottom")

    @staticmethod
    def anchor(box: tuple[float, float, float, float], side: str, gap: float) -> list[float]:
        x, y, width, height = box
        if side == "left":
            return [x - gap, y + height / 2]
        if side == "right":
            return [x + width + gap, y + height / 2]
        if side == "top":
            return [x + width / 2, y - gap]
        if side == "bottom":
            return [x + width / 2, y + height + gap]
        raise ValueError(f"unknown connector side: {side}")

    def default_route(self, start: list[float], end: list[float], start_side: str, route: str) -> list[list[float]]:
        if route == "straight" or (abs(start[0] - end[0]) < 0.5 or abs(start[1] - end[1]) < 0.5):
            return [start, end]
        if start_side in {"left", "right"}:
            mid_x = self.snap((start[0] + end[0]) / 2)
            return [start, [mid_x, start[1]], [mid_x, end[1]], end]
        mid_y = self.snap((start[1] + end[1]) / 2)
        return [start, [start[0], mid_y], [end[0], mid_y], end]

    @staticmethod
    def dedupe_points(points: list[list[float]]) -> list[list[float]]:
        result: list[list[float]] = []
        for point in points:
            normalized = [round(float(point[0]), 2), round(float(point[1]), 2)]
            if not result or normalized != result[-1]:
                result.append(normalized)
        return result

    @staticmethod
    def path_midpoint(points: list[list[float]]) -> tuple[float, float]:
        lengths = [math.dist(first, second) for first, second in pairwise(points)]
        total = sum(lengths)
        if total == 0:
            return points[0][0], points[0][1]
        target = total / 2
        travelled = 0.0
        for (first, second), segment in zip(pairwise(points), lengths):
            if travelled + segment >= target:
                ratio = (target - travelled) / segment if segment else 0
                return (
                    first[0] + (second[0] - first[0]) * ratio,
                    first[1] + (second[1] - first[1]) * ratio,
                )
            travelled += segment
        return points[-1][0], points[-1][1]

    def build_edges(self) -> None:
        for raw in self.spec.get("edges", []):
            if not isinstance(raw, dict):
                raise ValueError("each edge must be an object")
            edge_id = self.require_id(raw.get("id"), "edge")
            source_id = raw.get("from")
            target_id = raw.get("to")
            if source_id not in self.node_boxes:
                raise ValueError(f"edge {edge_id} has unknown source: {source_id}")
            if target_id not in self.node_boxes:
                raise ValueError(f"edge {edge_id} has unknown target: {target_id}")
            auto_start, auto_end = self.choose_sides(self.node_boxes[source_id], self.node_boxes[target_id])
            start_side = str(raw.get("startSide", auto_start))
            end_side = str(raw.get("endSide", auto_end))
            if start_side not in SIDE_FIXED_POINT or end_side not in SIDE_FIXED_POINT:
                raise ValueError(f"edge {edge_id} uses an invalid connector side")
            gap = float(raw.get("gap", 8))
            start = self.anchor(self.node_boxes[source_id], start_side, gap)
            end = self.anchor(self.node_boxes[target_id], end_side, gap)
            route = str(raw.get("route", self.default_edge_route))
            if route not in {"straight", "orthogonal"}:
                raise ValueError(f"edge {edge_id}.route must be 'straight' or 'orthogonal'")
            waypoints = raw.get("waypoints")
            if waypoints is None:
                points = self.default_route(start, end, start_side, route)
            else:
                if not isinstance(waypoints, list):
                    raise ValueError(f"edge {edge_id}.waypoints must be an array")
                routed: list[list[float]] = []
                for point in waypoints:
                    if not isinstance(point, list) or len(point) != 2 or not all(is_finite_number(v) for v in point):
                        raise ValueError(f"edge {edge_id} contains an invalid waypoint")
                    routed.append([self.snap(point[0]), self.snap(point[1])])
                points = [start, *routed, end]
            points = self.dedupe_points(points)
            if len(points) < 2:
                raise ValueError(f"edge {edge_id} has fewer than two distinct points")

            xs = [point[0] for point in points]
            ys = [point[1] for point in points]
            role = self.style(raw, "neutral")
            edge_frame = raw.get("frameId")
            if edge_frame is None and self.node_frame.get(source_id) == self.node_frame.get(target_id):
                edge_frame = self.node_frame.get(source_id)
            item = dict(raw)
            item["frameId"] = edge_frame
            item.setdefault("backgroundColor", "transparent")
            item.setdefault("strokeColor", role["stroke"])
            item.setdefault("fillStyle", "solid")
            item.setdefault("strokeStyle", "dashed" if raw.get("style") == "dashed" else "solid")
            item.setdefault("roughness", self.default_edge_roughness)
            item.setdefault("roundness", self.default_edge_roundness)
            edge = self.base(
                edge_id,
                "arrow",
                points[0][0],
                points[0][1],
                max(xs) - min(xs),
                max(ys) - min(ys),
                item,
                default_role="neutral",
                default_roundness=self.default_edge_roundness,
            )
            edge.update(
                {
                    "points": [[round(x - points[0][0], 2), round(y - points[0][1], 2)] for x, y in points],
                    "startBinding": {
                        "elementId": source_id,
                        "fixedPoint": SIDE_FIXED_POINT[start_side],
                        "mode": raw.get("bindMode", "orbit"),
                    },
                    "endBinding": {
                        "elementId": target_id,
                        "fixedPoint": SIDE_FIXED_POINT[end_side],
                        "mode": raw.get("bindMode", "orbit"),
                    },
                    "startArrowhead": raw.get("startArrowhead"),
                    "endArrowhead": raw.get("endArrowhead", "arrow"),
                    "elbowed": bool(raw.get("elbowed", False)),
                }
            )
            self.by_id[edge_id] = edge
            self.add_bound_reference(source_id, edge_id, "arrow")
            self.add_bound_reference(target_id, edge_id, "arrow")
            self.layers["edges"].append(edge)

            label = raw.get("label")
            if label is not None:
                label_id = self.reserve_generated_id(str(raw.get("labelId", f"{edge_id}__label")))
                center_x, center_y = self.path_midpoint(points)
                label_item = dict(raw)
                label_item.setdefault("fontSize", 14)
                label_item.setdefault("fontFamily", self.default_font)
                label_item.setdefault("textColor", raw.get("labelColor", role["stroke"]))
                label_item.setdefault("textAlign", "center")
                label_item.setdefault("verticalAlign", "middle")
                max_width = float(raw.get("labelWidth", 220))
                text = self.make_text(
                    label_id,
                    str(label),
                    0,
                    0,
                    label_item,
                    width_limit=max_width,
                    container_id=edge_id,
                    frame_id=edge_frame,
                )
                text["x"] = round(center_x - text["width"] / 2, 2)
                text["y"] = round(center_y - text["height"] / 2, 2)
                self.by_id[label_id] = text
                self.add_bound_reference(edge_id, label_id, "text")
                self.layers["labels"].append(text)

    def validate_frame_references(self) -> None:
        frame_ids = {frame["id"] for frame in self.layers["frames"]}
        for element in self.by_id.values():
            frame_id = element.get("frameId")
            if frame_id is not None and frame_id not in frame_ids:
                raise ValueError(f"element {element['id']} references unknown frame {frame_id}")

    def build(self) -> dict[str, Any]:
        if not isinstance(self.spec.get("nodes", []), list):
            raise ValueError("nodes must be an array")
        if not isinstance(self.spec.get("edges", []), list):
            raise ValueError("edges must be an array")
        if not isinstance(self.spec.get("frames", []), list):
            raise ValueError("frames must be an array")
        if not isinstance(self.spec.get("annotations", []), list):
            raise ValueError("annotations must be an array")

        self.build_frames()
        self.build_nodes()
        self.build_edges()
        self.validate_frame_references()

        # Children precede their frames; arrows precede nodes so node fills mask
        # endpoint strokes. Bound labels are kept above their containers.
        elements = [
            *self.layers["edges"],
            *self.layers["nodes"],
            *self.layers["annotations"],
            *self.layers["labels"],
            *self.layers["frames"],
        ]
        canvas = self.spec.get("canvas", {})
        return {
            "type": "excalidraw",
            "version": 2,
            "source": self.spec.get("source", "https://excalidraw.com"),
            "elements": elements,
            "appState": {
                "gridSize": self.grid or None,
                "gridStep": int(canvas.get("gridStep", 5)),
                "gridModeEnabled": bool(canvas.get("gridModeEnabled", False)),
                "viewBackgroundColor": canvas.get("background", WHITE),
                "currentItemFontFamily": self.default_font,
            },
            "files": self.files,
        }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("spec", type=Path, help="JSON diagram specification")
    parser.add_argument("output", type=Path, help="Output .excalidraw path")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        with args.spec.open("r", encoding="utf-8") as handle:
            spec = json.load(handle)
        if not isinstance(spec, dict):
            raise ValueError("the diagram specification must be a JSON object")
        scene = SceneBuilder(spec, args.spec.resolve()).build()
        args.output.parent.mkdir(parents=True, exist_ok=True)
        with args.output.open("w", encoding="utf-8") as handle:
            json.dump(scene, handle, ensure_ascii=False, indent=2)
            handle.write("\n")
    except (OSError, json.JSONDecodeError, ValueError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print(
        f"Wrote {args.output} ({len(scene['elements'])} elements, "
        f"{len(scene['files'])} embedded files)"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
