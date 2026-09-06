# Visual Style

The target is recognizably Excalidraw—human and approachable—without looking careless.

## Select one visual voice

- **Technical:** `roughness: 0`, solid fill, 2 px strokes, Nunito (`fontFamily: 6`). Use for dense architecture, data models, and compliance diagrams.
- **Native sketch:** `roughness: 1`, solid or restrained hachure fill, 2 px strokes, Excalifont (`fontFamily: 5`). Use for explanatory flows, teaching, ideation, and product concepts.
- Do not mix technical and sketch voices arbitrarily. A deliberate hand-drawn annotation may be the single exception.

Current official constants define standard font sizes `16`, `20`, `28`, and `36`, adaptive rounded rectangles as `{ "type": 3 }`, and roughness levels `0`, `1`, and `2`. See the official [constants source](https://github.com/excalidraw/excalidraw/blob/master/packages/common/src/constants.ts).

## Palette

Use dark ink `#1e1e1e` on white `#ffffff`. Pick at most four semantic accent families plus neutral gray.

| Role | Fill | Stroke |
|---|---|---|
| Primary | `#dbe4ff` | `#364fc7` |
| Secondary | `#e5dbff` | `#7048e8` |
| Success | `#d3f9d8` | `#2b8a3e` |
| Warning | `#fff3bf` | `#e67700` |
| Danger | `#ffe3e3` | `#c92a2a` |
| Data | `#e3fafc` | `#0b7285` |
| Neutral | `#f1f3f5` | `#495057` |
| Muted | transparent | `#868e96` |

Color must convey a repeated role, path, state, or ownership boundary. Avoid rainbow diagrams.

## Typography

- Title: 28–36 px.
- Section/frame name: 20–24 px or the native frame label.
- Node label: 16–20 px.
- Connector label and annotation: 14–16 px.
- Use no more than two font families.
- Use explicit line breaks to create balanced labels. Prefer short nouns and verbs over paragraphs inside nodes.
- Maintain at least 12 px internal padding; use 16–24 px for multi-line nodes.

## Shape and spacing system

- Work on a 20 px grid.
- Typical node: 180–240 px wide and 80–120 px tall.
- Decision diamond: at least 160 × 120 px.
- Compact badge: 28–36 px.
- Gap between peers: at least 60 px; use 80–120 px when an arrow label occupies the corridor.
- Frame padding: at least 40 px around children and 28 px below the frame name.
- Canvas margin: at least 60 px.
- Keep peer nodes the same size unless their importance or content genuinely differs.

## Connectors

- An ordinary relationship is one arrow from one source service to one destination service. Prefer a direct straight line and place the nodes so that line is easy to read.
- If a direct line would hit another element, use one clean orthogonal dogleg. Reposition nodes before adding more bends.
- Keep connector corners unrounded by default. Do not turn multi-segment paths into loops, waves, hooks, or decorative swoops.
- Reserve multi-bend outer corridors for genuine retry, feedback, response, or cross-zone paths, and keep them visually secondary.
- Keep at least 20 px clearance from unrelated nodes and labels.
- Use one primary direction. Place feedback, retry, or exception paths around the outer edge.
- Put labels on the longest clear segment, not at a bend or arrowhead.
- Use solid arrows for primary synchronous flow. Use dashed arrows only when the dash means something stated in a legend, such as asynchronous, conditional, optional, or control flow.
- Avoid bidirectional arrows when two separately labeled directions would be clearer.
- Crossings are a layout problem. Move nodes or use one simple dogleg before considering a more complex route.

## Frames, titles, and annotations

- Use frames for actual phases, lanes, teams, trust zones, deployment boundaries, or grouped subsystems.
- Put a single clear title above the content, left aligned with the first frame or node.
- Keep explanatory notes outside the main route. Use muted ink and smaller text.
- A legend is needed only when color, dash, badges, or abbreviations encode meaning that is not self-evident.

## Sequence badges

Use numbered badges when the reader must distinguish order. Keep them consistent, place them near the action they number, and use suffixes such as `4a` and `4b` only for real branches. A badge may overlap a node corner only when it remains legible and is marked as an intentional overlap in the spec.

## Icons and artwork

- Prefer native primitives and text for generic concepts.
- Use a verified library element or embedded image when a recognizable product/service icon materially improves comprehension.
- Do not invent a logo or approximate a proprietary service icon.
- Keep icon scale consistent, preserve its aspect ratio, and add a plain text service label.
- Record the icon source and license when it did not come from the user.

## Reference reconstruction

Match the source's macro layout and whitespace before fine styling. Preserve meaningful asymmetry. Do not force a dense reference into a simplistic equal grid if its grouping and emphasis would be lost.
