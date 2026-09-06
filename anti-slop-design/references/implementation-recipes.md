# Implementation recipes and verification

Use the applicable sections for fragile effects and rendered verification within the requested
scope.

## Contents

- [Visible content](#content-must-be-visible-by-default) | [Clear every cut](#clear-every-cut) |
  [Align parallel columns](#align-parallel-columns) | [Center precisely](#center-precisely)
- [Cast shadows as light](#cast-shadows-as-light) |
  [Feather a full-bleed image](#feather-a-full-bleed-image-into-the-page) |
  [Build liquid glass](#build-liquid-glass-deliberately) | [Animate fills](#animate-fills-cleanly)
- [Rendered verification matrix](#rendered-verification-matrix)

## Content must be visible by default

- Render text and controls in their normal visible state before animation code runs.
- Never make opacity 0 or an off-screen transform the only pre-animation state.
- Treat CSS view timelines, IntersectionObserver, hydration, Motion initial states, throttled tabs,
  screenshot tooling, and unsupported engines as conditions in which animation may never start.
- Animate already-visible properties or affordances: hover state, marquee, rotating mark, sliding
  tab indicator, count, or subtle parallax.
- If an entrance effect is required, make the never-started state fully readable. For
  server-rendered or static content, keep the no-JavaScript state readable too. A client-only app
  may require JavaScript to render, but animation must never be the reason rendered content stays
  hidden.
- Gate nonessential motion with prefers-reduced-motion.

## Clear every cut

For every clip-path, notch, overflow hidden, fixed height, mask, or overlapping section:

1. Measure how much visible area the cut removes.
2. Pad live content clear by more than that amount.
3. Keep continuing content on the layer that stays visible.
4. Zoom into every affected edge and corner and inspect it pixel by pixel.
5. Check headline caps, descenders, focus rings, controls, shadows, and translated states.

## Align parallel columns

- Give comparison cards equal height.
- Put title, price, description, list, and action into shared row tracks or reserve equivalent
  vertical space.
- Keep a missing value's slot instead of collapsing it.
- Anchor every action to the bottom.
- Test with the longest realistic copy, translated copy, and narrow widths.

## Center precisely

- Verify mathematical and optical centering at high zoom.
- In SVG, text-anchor middle only solves the horizontal axis. Use dominant-baseline central or a
  measured dy for vertical placement.
- Account for stroke, padding, rotation, glyph sidebearings, and the difference between bounding box
  and optical center.
- Inspect buttons, pills, circles, tiles, badges, logo marks, icons, numbers, and strike lines.

## Cast shadows as light

- Prefer tonal elevation or a self-colored edge when depth works without shadow.
- When needed, use a tight, low-offset, small-blur, directional shadow from one source.
- Tint it toward the surface or element rather than using a large black bloom.
- Delete duplicate offset boxes and blurred copies of the element.
- The falloff must be seamless. If the shadow outline can be traced, fix or remove it.

## Feather a full-bleed image into the page

For an image intended to blend into the page, remove accidental seams without losing the subject or
distorting the composition. The source used the following recipe for one specimen; the measurements
and technique are examples, not universal requirements:

1. **Mask the image itself**: The reference used mask-image with a vertical gradient to reveal the
   page surface through the edges.
2. **Tune the fade**: The reference faded roughly 30 percent at each end with at least 10 stops and
   kept an opaque middle around 31 percent through 65 percent. Use only the stops and fade length
   the actual image needs.
3. **Preserve the subject**: The reference used about 116vh to accommodate its fades. Size the
   section for the current content and viewport instead of copying that height.
4. **Match the adjoining surfaces**: The reference revealed one continuous page color through both
   edges. Make each edge blend into its actual adjoining surface.

Keep any text-legibility scrim local to the text and fade it back to transparent before both image
edges. A partial-opacity scrim ending at the section boundary creates a new hard band. Use a strong,
controlled text shadow for the remaining legibility when appropriate.

## Build liquid glass deliberately

The following reference values describe two glass-button variants over a real photographic backdrop.
Translate them to the platform rather than copying blindly. Geist and the blue/cyan values belong to
that measured specimen; they are not type or palette recommendations. Substitute the current design
system and re-tune the material.

Shared base:

- Label and icon: #FFFFFF at 100 percent.
- Type: Geist Medium, size 20.
- Icon-label gap: 8.
- Padding: 20 horizontal and 14 vertical.
- Edge strokes: two hairlines at 20 percent opacity, one #22BBFD and one #FFFFFF.
- Top inner highlight: #FFFFFF at 20 percent, y offset 1, blur 32.
- Drop shadow: #2575FF at 6 percent, y offset 3, blur 3.

| Property        |   Thin |  Thick |
| --------------- | -----: | -----: |
| Fill #2575FF    |   100% |    50% |
| Light angle     | -45deg | -50deg |
| Light intensity |     80 |     60 |
| Refraction      |     80 |     64 |
| Depth           |      2 |     44 |
| Dispersion      |     40 |     67 |
| Frost           |      6 |      2 |
| Splay           |      0 |     20 |

Meanings:

- Light angle and intensity control specular direction and strength.
- Refraction controls backdrop bending.
- Depth controls apparent glass thickness.
- Dispersion controls the chromatic split at edges.
- Frost controls blur.
- Splay controls how far refraction extends past the shape.

CSS approximation:

- Use backdrop-filter blur plus saturate and contrast for frost and lensing.
- Use an inset white shadow for the top gloss.
- Layer the two low-opacity edge strokes.
- Use one tight, fill-colored drop shadow.
- Approximate dispersion with a 1px cyan/magenta edge offset or a thin conic edge gradient.
- An SVG feDisplacementMap can distort a supplied source graphic, but do not assume it can refract
  an arbitrary live backdrop across browsers. Verify the real capture path and fall back to honest
  blur, gloss, and edge treatment when it cannot.

Do not use glass over a flat field. Inspect for blur banding, leaked shadow, resting halo, clipped
glow, and hover or press state pops.

## Animate fills cleanly

- Animate a clip or width/height with stable caps instead of scaling a rounded shape.
- Fill the complete track.
- Use smooth, intentional easing with no stutter.
- Verify intermediate frames, not only start and end.

## Rendered verification matrix

Before delivery, run the actual interface. Cover every in-scope surface and representative affected
uses of shared primitives with the applicable checks below; do not invent unsupported form factors,
themes, or states. Verify against a fresh or cache-busted load; a cached page shows stale styling
and falsifies the check in both directions.

### Viewports

- Representative wide desktop.
- Narrow desktop or tablet.
- Smallest supported mobile width and a short mobile height with browser chrome. Verify dynamic
  viewport sizing, safe-area insets, and overlay collision behavior where they apply.
- Every supported theme or color scheme on each in-scope surface, including transition and
  no-animation fallbacks when applicable.
- Long and short content, zoomed text, and translated copy when available.

### Geometry

- First viewport is deliberate: expressive pages own the fold, while task surfaces expose useful
  orientation, state, and workflow without decorative height.
- Normal copy has consistent gutters.
- Headlines and controls are not clipped.
- All intended centers are mathematically and optically correct.
- Parallel columns share row baselines and bottom-aligned actions.
- Overlaps, masks, notches, and fixed heights clear live content.

### Color and material

- Text and control labels have strong contrast.
- Semantic tokens preserve contrast and surface hierarchy across every theme; no accidental
  mode-specific hardcodes leak into shared components.
- Adjacent sections form one coherent surface or one intentional break.
- Gradients do not band.
- Grain stays behind readable content.
- Shadows fade seamlessly from one light source.
- Glass has a meaningful backdrop and no blur, leak, halo, or transition defects.
- Images intended to blend into the page have no accidental edge seams; deliberately framed crops
  may end hard.

### Interaction

- Activate every in-scope button, tab, toggle, accordion, slider, link, and form control on the
  affected surface. Confirm the expected state change, navigation, submission, cancellation, or
  recovery, not merely a visual response.
- Test pointer, keyboard, touch, focus-visible, hover, active, disabled, loading, success, and error
  states where applicable.
- Confirm controls keep semantic names, roles, state announcements, logical focus order, and usable
  touch targets after visual customization.
- Inspect the accessibility tree or use a screen reader for changed controls when tooling is
  available.
- Confirm dialogs, sheets, menus, popovers, and lightboxes place initial focus, trap it only when
  modal, support expected dismissal keys, and restore focus on close.
- Disable motion and confirm rendered content remains visible. For server-rendered or static
  surfaces, also disable JavaScript; for client-only apps, verify the loading shell and confirm no
  post-mount animation can strand content hidden.
- Enable reduced motion and confirm nonessential effects stop.
- Confirm critical information and actions do not depend only on hover; tooltips are supplementary.
- Check console or runtime errors and layout shifts.

### Anti-template gate

- Compare every screen against [anti-patterns.md](anti-patterns.md).
- Look for compounds: default hero plus icon-card row plus pricing plus FAQ plus CTA slab plus
  standard footer.
- For marketing, editorial, and brand surfaces, confirm the palette, type voice, signature artifact,
  atmosphere, silhouette, nav treatment, real specifics, and interaction or motion language belong
  to one world.
- For product and admin surfaces, confirm the token system, information architecture, state model,
  data display, navigation, and interaction conventions belong to one operational world. Do not
  require scenery or a decorative artifact.
- Ask whether identity-bearing choices could be reskinned for an unrelated product. If yes, revise
  them within the authorized scope, or report them in an audit. Preserve familiar task primitives
  and intentional design-system consistency.
- Confirm the result is not merely clean. It must contain a brief-specific point of view and at
  least one authored decision appropriate to its surface.
