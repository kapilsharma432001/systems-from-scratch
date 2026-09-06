# Native Excalidraw Format

Use this reference when creating or editing `.excalidraw` scene JSON.

## Source of truth

Excalidraw files are plaintext JSON. The official envelope is documented in the [JSON schema guide](https://docs.excalidraw.com/docs/codebase/json-schema). The guide is intentionally small; use the current [element type definitions](https://github.com/excalidraw/excalidraw/blob/master/packages/element/src/types.ts) and [constants](https://github.com/excalidraw/excalidraw/blob/master/packages/common/src/constants.ts) when a field has changed.

```json
{
  "type": "excalidraw",
  "version": 2,
  "source": "https://excalidraw.com",
  "elements": [],
  "appState": {
    "gridSize": 20,
    "viewBackgroundColor": "#ffffff"
  },
  "files": {}
}
```

The file format is not the clipboard format. Do not write `type: "excalidraw/clipboard"` for a saved scene.

## Generation paths

### Official skeleton conversion

When a compatible `@excalidraw/excalidraw` browser package is already available, prefer [`convertToExcalidrawElements`](https://docs.excalidraw.com/docs/@excalidraw/excalidraw/api/excalidraw-element-skeleton). It expands simplified skeletons, binds labels, and creates reciprocal arrow bindings.

- The API is beta. Pin the package version used by the project.
- Use stable IDs and `regenerateIds: false` when bindings or future edits depend on them.
- Wait for `document.fonts.ready` before conversion. Text metrics affect wrapping and arrow routing.
- Serialize the converted scene with the API exposed by the installed package; current typings/source take precedence over older documentation signatures.

### Dependency-free native builder

Use `scripts/build_excalidraw.py` when the official browser package is unavailable. It emits conservative version-2 native elements and current fixed-point bindings. Validate and then load the output in Excalidraw so its restore path can normalize the scene.

## Full element invariants

A full element normally carries:

- identity and geometry: `id`, `type`, `x`, `y`, `width`, `height`, `angle`;
- style: `strokeColor`, `backgroundColor`, `fillStyle`, `strokeWidth`, `strokeStyle`, `roughness`, `opacity`, `roundness`;
- lifecycle/order: `seed`, `version`, `versionNonce`, `index`, `isDeleted`, `updated`;
- relationships: `groupIds`, `frameId`, `boundElements`;
- metadata: `link`, `locked`, and optional `customData`.

Keep IDs unique and stable during edits. Preserve unknown fields unless there is evidence that they are invalid.

## Text and labeled containers

A native text element needs `text`, `originalText`, `fontSize`, `fontFamily`, `textAlign`, `verticalAlign`, `containerId`, `autoResize`, and `lineHeight` in addition to the base fields.

For a labeled shape:

- the text element's `containerId` points to the shape;
- the shape's `boundElements` contains `{ "id": "<text-id>", "type": "text" }`;
- both elements use the same `frameId` and compatible group membership;
- the text bounds remain inside the container with visible padding.

Do not use a floating text element merely placed over a node when it should move and resize with that node.

## Arrow bindings

Current arrow bindings use stable target IDs and fixed points:

```json
{
  "startBinding": {
    "elementId": "producer",
    "fixedPoint": [1, 0.5],
    "mode": "orbit"
  },
  "endBinding": {
    "elementId": "consumer",
    "fixedPoint": [0, 0.5],
    "mode": "orbit"
  }
}
```

The bound shapes must each contain a reciprocal arrow reference in `boundElements`. Existing scenes may use legacy `focus` and `gap` binding fields; preserve them during a small edit unless the scene is deliberately restored or migrated by the official API.

Arrow `points` are relative to the arrow's `x` and `y`. Use explicit waypoints for important routing. An arrow label is a text element whose `containerId` is the arrow ID, and the arrow reciprocally references that text.

## Frames and groups

- `frameId` assigns a child to a frame. It is not a visual approximation of containment.
- In native scene order, frame children should precede their frame element. See the official [frames guide](https://docs.excalidraw.com/docs/codebase/frames).
- `groupIds` are ordered deepest group first. Apply the same group ID to every element in a composite symbol.
- Use groups for components that should move together; use frames for semantic zones and lanes.

## Embedded images

An image element references `fileId`; the top-level `files` object stores the corresponding data URL and MIME type. Never write an unresolved filesystem path into the scene.

```json
{
  "files": {
    "stable-file-id": {
      "id": "stable-file-id",
      "mimeType": "image/svg+xml",
      "dataURL": "data:image/svg+xml;base64,...",
      "created": 0,
      "lastRetrieved": 0
    }
  }
}
```

Use native vector elements for reusable library items where practical. The official [library repository](https://github.com/excalidraw/excalidraw-libraries) recommends grouping multi-element items so they behave as a single unit.

## Safe existing-scene edits

Before editing, record element counts, scene bounds, IDs, deleted elements, frames, groups, bindings, and embedded files. Change only the targeted elements. Do not regenerate every ID or remove deleted elements as a side effect of a small visual correction.
