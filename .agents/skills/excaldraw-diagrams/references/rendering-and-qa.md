# Rendering and Visual QA

JSON validation proves structural consistency; it does not prove that Excalidraw renders the scene well.

## Preferred render paths

Use the first compatible path already available in the environment:

1. An official Excalidraw MCP/editor surface that can load the scene and return an image.
2. A project-pinned browser build of `@excalidraw/excalidraw`, using `loadFromBlob` or restore utilities and `exportToSvg`/`exportToBlob`.
3. The Excalidraw web app or a trusted Excalidraw editor extension: import the `.excalidraw` file, zoom to fit, and export PNG or SVG.

Do not install a package, extension, or remote connector without authorization. If no faithful renderer is available, deliver the validated native file and state clearly that visual QA remains pending.

Official references:

- [Export utilities](https://docs.excalidraw.com/docs/@excalidraw/excalidraw/api/utils/export)
- [Load and restore utilities](https://docs.excalidraw.com/docs/@excalidraw/excalidraw/api/utils)
- [Programmatic element creation](https://docs.excalidraw.com/docs/@excalidraw/excalidraw/api/excalidraw-element-skeleton)

## Browser-rendering invariants

- Wait for `document.fonts.ready` before converting skeletons or exporting.
- Restore or load the scene before export so invalid references and legacy fields are normalized.
- Export from the same restored scene that was inspected.
- Use a white or explicitly requested background and enough export padding.
- Fit the entire scene once, then inspect dense regions at readable zoom.
- A hand-written JSON-to-SVG approximation is not a faithful Excalidraw render and cannot satisfy visual QA.

## Inspection checklist

### Semantic

- Every required actor, node, store, boundary, branch, join, and response path is present.
- Arrow direction and labels match the intended meaning.
- Sequence badges follow the real execution order.
- Inferred or suggested components are not presented as explicit facts without a note.

### Geometry

- No unrelated nodes overlap.
- No text is clipped, crowded, or outside its container.
- No connector passes through a node, label, badge, or icon.
- Every ordinary connector links exactly two services with a direct line or one simple dogleg; it has no unnecessary loop, swoop, or bend.
- Arrowheads are visible and terminate at the intended side.
- Frame names do not collide with children.
- Parallel items are aligned and evenly spaced.

### Visual system

- Title, frame labels, nodes, and annotations have a clear type hierarchy.
- Palette roles remain consistent and accessible.
- Primary flow dominates; conditional and feedback routes remain secondary.
- Icon sizes and label placement are consistent.
- The diagram remains readable at fit-to-content scale.

### Artifact

- The `.excalidraw` file reopens successfully.
- Text, shapes, connectors, and frames remain individually editable.
- Moving a bound node keeps its label and arrows attached.
- Embedded images resolve from the top-level `files` map.
- The delivered PNG/SVG was generated after the final native-file edit.

Iterate until both `validate_excalidraw.py --strict` and this visual checklist pass. Reviewed warnings are acceptable only when their geometry is intentional and documented.
