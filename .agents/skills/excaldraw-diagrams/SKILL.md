---
name: excaldraw-diagrams
description: Create, reconstruct, edit, and visually verify polished native Excalidraw diagrams from text, notes, sketches, screenshots, or existing scenes. Use when the requested artifact must be an editable `.excalidraw` file. Do not use for draw.io, Mermaid-only, or bitmap-only deliverables.
---

# Excaldraw Diagrams

Create a native, editable Excalidraw scene whose topology is correct, whose visual hierarchy is deliberate, and whose final render has been inspected. The `.excalidraw` file is the source artifact; a PNG or SVG is only a preview.

## Choose the operating mode

- **Text to diagram:** derive a semantic graph from requirements, prose, or code.
- **Sketch conversion:** preserve the source's topology and intent while regularizing geometry.
- **Reference reconstruction:** match the reference's zones, reading order, relative emphasis, and visual rhythm before decorative detail.
- **Existing-scene edit:** preserve unaffected element IDs, bindings, groups, frames, styling, and user changes.

For reference reconstruction, fidelity order is: topology, grouping, reading order, labels, routing, relative scale, then decoration.

## Read the relevant references

- Read [file-format.md](references/file-format.md) before creating or directly editing scene JSON.
- Read [spec-format.md](references/spec-format.md) when using `scripts/build_excalidraw.py`.
- Read [visual-style.md](references/visual-style.md) for every new diagram or material restyle.
- Read [layout-patterns.md](references/layout-patterns.md) for the selected diagram family.
- Read [rendering-and-qa.md](references/rendering-and-qa.md) before exporting or claiming visual quality.

## Required workflow

1. Inspect all supplied sources. For an existing `.excalidraw` file, inventory frames, nodes, labels, arrows, bindings, groups, embedded files, and scene bounds before changing it.
2. Write a compact semantic plan containing:
   - actors and nodes;
   - real boundaries or phases;
   - directed relationships and data carried;
   - branches, joins, loops, and failure paths;
   - sequence numbers when order matters;
   - facts that are explicit, safely inferred, ambiguous, or merely suggested.
3. Resolve only ambiguities that materially change topology. Keep assumptions visible when they are useful to the reader.
4. Select a layout pattern. Place related services so ordinary relationships can use direct pairwise arrows; reserve connector corridors only for real fan-out, retry, feedback, or cross-zone paths.
5. Create editable native elements. Prefer the official `ExcalidrawElementSkeleton` conversion API when a compatible browser package is already available. Otherwise use the included dependency-free builder for conservative version-2 scene JSON:

   ```bash
   python3 scripts/build_excalidraw.py diagram-spec.json output.excalidraw
   ```

6. Validate the native artifact:

   ```bash
   python3 scripts/validate_excalidraw.py --strict output.excalidraw
   ```

7. Open or render the file with Excalidraw itself or its official export APIs. Inspect the actual render at fit-to-content and at readable zoom.
8. Repair clipped text, unintended overlaps, connector crossings, weak contrast, inconsistent spacing, or ambiguous ordering. Revalidate and rerender after every material change.

## Non-negotiable quality rules

- Do not substitute Mermaid, a screenshot, or a flattened SVG for the editable `.excalidraw` artifact.
- Use frames only for real semantic boundaries, phases, lanes, or deployment zones.
- Keep connectors off nodes, text, badges, and icons except at their intended endpoints.
- Bind arrows to stable element IDs and keep reciprocal `boundElements` references valid.
- Keep bound text linked through `containerId`; do not simulate a labeled node with unrelated floating text.
- Connect two steps or services with one direct, unrounded arrow by default. If an obstacle requires routing, use one clean orthogonal dogleg. Do not add loops, swoops, shared decorative trunks, or extra bends to an ordinary pairwise relationship.
- Use a complex or curved route only for a real retry, feedback, return, or unavoidable cross-zone path. Mark that exception explicitly in the builder spec and verify it in the rendered scene.
- Keep a primary reading direction. Make feedback paths visibly secondary.
- Limit the palette and typography. Color encodes roles or states; it is not decoration.
- Use native primitives for ordinary shapes. Embed an image only when the source icon or artwork is necessary, licensed for the use, and stored in the scene's `files` map.
- Preserve user-authored wording unless the task explicitly includes editing it. Correct only requested typos or formatting issues.
- Never claim that a diagram is visually verified from JSON validation alone.

## Output contract

Return:

- the editable `.excalidraw` file;
- an inspected PNG or SVG preview when rendering is available;
- a short note describing the diagram's reading order, any meaningful assumptions, and any QA limitation;
- validation results, distinguishing blocking errors from reviewed warnings.
