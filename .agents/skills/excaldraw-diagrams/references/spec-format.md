# Builder Specification

`scripts/build_excalidraw.py` converts a compact, explicit layout specification into a native `.excalidraw` file. It intentionally does not guess a large graph layout. Plan coordinates and connector corridors first.

## Command

```bash
python3 scripts/build_excalidraw.py diagram-spec.json diagram.excalidraw
python3 scripts/validate_excalidraw.py --strict diagram.excalidraw
```

## Minimal example

```json
{
  "canvas": { "background": "#ffffff", "gridSize": 20 },
  "defaults": {
    "fontFamily": 5,
    "fontSize": 20,
    "roughness": 1,
    "edgeRoute": "straight",
    "edgeRoundness": null,
    "edgeRoughness": 0
  },
  "frames": [
    { "id": "backend", "name": "BACKEND", "x": 380, "y": 100, "width": 720, "height": 360 }
  ],
  "nodes": [
    { "id": "user", "type": "ellipse", "label": "User", "x": 80, "y": 210, "width": 140, "height": 80, "style": "neutral" },
    { "id": "api", "type": "rectangle", "label": "API", "x": 460, "y": 200, "width": 180, "height": 100, "style": "primary", "frameId": "backend" },
    { "id": "worker", "type": "rectangle", "label": "Worker", "x": 820, "y": 200, "width": 180, "height": 100, "style": "success", "frameId": "backend" }
  ],
  "edges": [
    { "id": "request", "from": "user", "to": "api", "label": "request", "startSide": "right", "endSide": "left" },
    { "id": "dispatch", "from": "api", "to": "worker", "label": "job", "startSide": "right", "endSide": "left", "frameId": "backend" }
  ],
  "annotations": [
    { "id": "title", "type": "text", "text": "Request Processing", "x": 60, "y": 30, "fontSize": 36, "style": "ink" }
  ]
}
```

Coordinates and edge waypoints are absolute scene coordinates. The builder snaps generated geometry to the configured grid unless `snapToGrid` is false.

Connector defaults are intentionally plain: `edgeRoute` is `straight`, `edgeRoundness` is `null`, and `edgeRoughness` is `0`. Override them only when the diagram's meaning requires a different route.

## Frames

Required: `id`, `x`, `y`, `width`, `height`.

Optional: `name`, `strokeColor`, `backgroundColor`, `strokeWidth`, `strokeStyle`, `roughness`, `groupIds`, `parentFrameId`, `customData`.

Assign a node or edge to a frame with `frameId`. Keep the element's complete geometry within the frame.

## Nodes and annotations

Supported `type` values:

- `rectangle`, `ellipse`, `diamond` for ordinary nodes;
- `badge` for compact sequence markers;
- `text` for titles and annotations;
- `image` for embedded PNG, JPEG, WebP, GIF, BMP, or SVG files.

Common fields:

- required: `id`, `type`, `x`, `y`;
- shapes/images: `width`, `height`;
- labeled shapes: `label`;
- text: `text`;
- semantic style: `style`;
- overrides: `strokeColor`, `backgroundColor`, `fillStyle`, `strokeWidth`, `strokeStyle`, `roughness`, `opacity`, `roundness`;
- text overrides: `fontSize`, `fontFamily`, `textColor`, `textAlign`, `verticalAlign`, `padding`, `lineHeight`;
- relationships: `frameId`, `groupIds`;
- metadata: `link`, `locked`, `customData`.

An image additionally requires `path`. Its bytes are embedded into the top-level `files` map. Use only authorized and appropriately licensed images.

Set `customData.allowOverlap` only for a deliberate overlay such as a corner badge. Do not use it to silence accidental collisions.

## Edges

Required: `id`, `from`, `to`.

Optional:

- `label`;
- `startSide` and `endSide`: `left`, `right`, `top`, or `bottom`;
- `waypoints`: absolute `[x, y]` corridor points between the endpoints;
- `route`: `straight` (default) or `orthogonal`;
- `startArrowhead` and `endArrowhead`;
- `strokeColor`, `strokeWidth`, `strokeStyle`, `roughness`, `opacity`;
- `style`: `primary`, `secondary`, `success`, `warning`, `danger`, `data`, `neutral`, `muted`, or `dashed`;
- `gap`: endpoint distance from the bound node;
- `frameId`, `groupIds`, `bindMode`, `customData`.

Omit `waypoints` for an ordinary service-to-service relationship; the builder then creates one direct arrow. Use `route: "orthogonal"` for a simple midpoint dogleg when a straight line is unsuitable. Supply explicit waypoints only for fan-out, fan-in, retry, feedback, cross-zone routing, or avoiding a third node.

Keep a normal connector to three segments or fewer. When a genuinely complex path needs more than three segments, set `customData.allowComplexRoute: true`. When a multi-segment connector intentionally uses rounded corners, set `customData.allowCurvedRoute: true`; otherwise keep `roundness: null`.

## Built-in semantic styles

| Role | Intended use |
|---|---|
| `primary` | principal service or main path |
| `secondary` | supporting subsystem |
| `success` | completed/output state |
| `warning` | decision, review, or attention |
| `danger` | failure or rejection |
| `data` | storage, index, or data product |
| `neutral` | ordinary component |
| `muted` | secondary annotation or connector |
| `ink` | title or strong monochrome element |
| `dashed` | conditional/asynchronous connector |

Keep role meaning consistent within one diagram. Prefer role styles over one-off colors.
