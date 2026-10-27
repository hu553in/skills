# Implementation recipes and verification

Use the applicable sections for fragile effects and rendered verification within the requested
scope.

## Contents

- [Visible content](#content-must-be-visible-by-default) | [Clear every cut](#clear-every-cut) |
  [Align parallel columns](#align-parallel-columns) | [Center precisely](#center-precisely)
- [Cast shadows as light](#cast-shadows-as-light) |
  [Feather a full-bleed image](#feather-a-full-bleed-image-into-the-page) |
  [Build liquid glass](#build-liquid-glass-deliberately) | [Animate fills](#animate-fills-cleanly) |
  [Motion cost](#keep-motion-responsive)
- [Rendered verification matrix](#rendered-verification-matrix)
- [Stateful controls](#stateful-controls) | [Data displays](#data-displays) |
  [Media delivery](#media-delivery) |
  [Responsive and theme behavior](#responsive-and-theme-behavior)

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

For affected clip-paths, notches, overflow hiding, fixed heights, masks, or overlaps, keep live
content on the visible layer with padding greater than the removed area. Inspect affected edges,
zooming when needed to resolve clipping of caps, descenders, focus rings, controls, or shadows;
include translated content where supported.

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
distorting the composition. Adapt the technique to the image and layout:

1. **Mask the image itself**: Use mask-image with a vertical gradient to reveal the page surface
   through the edges.
2. **Tune the fade**: Use only the stops and fade length the actual image needs, keeping the subject
   clear and opaque.
3. **Preserve the subject**: Size the section for the current content and viewport, allowing room
   for the fades without cropping important detail.
4. **Match the adjoining surfaces**: Make each edge blend into its actual adjoining surface.

Keep any text-legibility scrim local to the text and fade it back to transparent before both image
edges. A partial-opacity scrim ending at the section boundary creates a new hard band. Use a strong,
controlled text shadow for the remaining legibility when appropriate.

## Build liquid glass deliberately

The following values illustrate two glass-button variants over a photographic backdrop. Translate
them to the platform rather than copying blindly. Geist and the blue/cyan values are examples, not
type or palette recommendations. Substitute the current design system and re-tune the material.

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

For scroll-linked CSS, declare `animation-timeline` and `animation-range` after the `animation`
shorthand, which resets them. Put enhancement behind the relevant feature and reduced-motion checks.
Keep the complete static layout and readable prose available without the enhancement. Use a timeline
on the moving track when a pinned child cannot drive its own progress.

## Keep motion responsive

Name CSS transition properties explicitly instead of using `transition: all`. Prefer `transform` and
`opacity` for frequent motion when they preserve the intended geometry. Dimension changes can still
serve real reflow or the stable-cap fill recipe above. Keep layout and paint work local, inspect
intermediate frames, and check responsiveness under representative load before retaining a costly
effect. Avoid permanent `will-change` on whole classes.

## Stateful controls

Preserve the project's interaction contract while styling the states it actually supports.

- Keep visible labels, native semantics, programmatic names, and field/error associations. A
  placeholder can show a format but cannot replace the label. Use text as well as color for errors
  and disabled explanations. Do not replace the project's validation timing merely for a new look.
- Keep border widths and control geometry stable across hover, focus, invalid, and busy states.
  Reserve an icon or progress slot where it prevents shifts. Error copy may wrap; do not clip it to
  force a fixed height. Focus indication should appear promptly without an animated delay.
- Retain a readable action label during submission and prevent unintended duplicate requests. Show
  success only after the actual operation succeeds. A copied label follows a successful clipboard
  write, and an optimistic change needs failure recovery. Preserve useful input on error.
- Place feedback near the action or content that changed. Announce relevant results without
  announcing every intermediate animation frame or search keystroke. Debounced search must retain
  the latest query's result when requests finish out of order.
- A drag interaction needs an accessible keyboard alternative and clear feedback about the move.
  Menus, tooltips, and overlays must remain usable near viewport edges and outside clipping parents.
  Reuse the existing accessible primitive rather than styling a weaker substitute.

## Data displays

Choose a form that answers the user's question. A single value usually needs a figure with a unit
and qualifier. Bars support magnitude comparisons, lines support change over ordered time, and
tables support exact values or many categories. Avoid adding charts merely to fill a dashboard.
Retain established domain conventions when they improve comprehension.

- Use verified data or explicitly labeled sample data. State relevant units, time range, source, and
  missing values. Do not turn missing data into zero or invent precision, totals, or trends.
- Magnitude bars start at zero. Label a deliberately narrowed axis clearly; do not exaggerate a
  small difference with an unexplained truncated range. Prefer separate panels to an ambiguous
  dual-axis comparison of different units.
- Emphasize the series the task concerns and keep reference material quiet. Keep series meaning
  stable across charts, filters, and themes. Use direct labels, markers, or patterns so color alone
  does not carry identity or state.
- Use tabular numerals where values align. Keep labels and gridlines legible without competing with
  the data. Provide an appropriate textual summary or data table for a visual chart.
- Check long labels, empty and partial series, real date/number formatting, and both supported
  themes. Reuse the project's chart tooling; inline SVG and a new chart library are choices, not
  requirements.

## Media delivery

- Prefer supplied material and actual authorized product captures. Inspect each crop at its
  displayed size. Preserve the real product's meaning; an attractive treatment must not turn a
  stand-in into customer proof or hide an important detail.
- Reserve image dimensions or an aspect ratio to prevent layout shifts. Supply responsive sources
  and a crop appropriate to the layout. Do not lazy-load the initial primary image; defer suitable
  off-screen media. Check that a high-resolution source is actually useful at the rendered size.
- For video, retain a useful poster, playback controls, and captions when needed. Do not autoplay
  audible media. Give persistent nonessential motion a usable pause mechanism and an appropriate
  static or reduced-motion treatment. Use the project's asset and performance budgets.
- Decorative texture must not intercept input, appear as meaningful accessibility content, or reduce
  text contrast. Keep it subordinate to real material and measure the textured result. Avoid
  expensive animated filters or permanent layer promotion without evidence they are needed.

## Responsive and theme behavior

Use existing breakpoints and supported widths. Apply continuous sizing to properties that should
vary continuously and discrete layout changes where the content stops fitting. Use capability
queries for hover and pointer behavior. A narrow viewport does not prove that the input is touch.

Let the surrounding row reflow before squeezing labels into illegibility. Keep useful names and
translated strings intact. Use logical properties and locale-aware formats where the product
supports them. Dense tables need an intentional narrow layout or usable scrolling that retains row
identity, header relationships, and access to actions. Hiding overflow is not a responsive fix.

Treat dark mode as the same semantic system rendered deliberately. Preserve explicit user choices
and the existing system-preference behavior. Recheck surface hierarchy, focus, imagery, and chart
series in each supported mode. Avoid global image inversion and mechanical color inversion. Do not
add a mode switch or a new persistence mechanism without task scope.

## Rendered verification matrix

Use this matrix for rendered changes or audits, selecting checks for the affected behavior and risk.
Cover declared surfaces and representative affected uses of shared primitives; do not expand a local
styling fix into testing every unchanged control. Do not invent unsupported form factors, themes, or
states. Confirm the loaded interface includes the current changes; reload or bypass stale caches
when needed. If it cannot run, report the limits of supplied renders and code review.

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

- Exercise affected buttons, tabs, toggles, accordions, sliders, links, and form controls; for a
  full interaction audit, cover every control in the declared scope. Confirm expected state changes,
  navigation, submission, cancellation, or recovery, not merely a visual response. Use disposable
  fixtures or a safe test environment for mutations; verification does not authorize live payments,
  messages, publication, deletion, or changes to access.
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

- Compare affected screens against relevant entries in [anti-patterns.md](anti-patterns.md); use the
  whole catalog for a requested full audit.
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
- For new visual directions, confirm a brief-specific point of view. For constrained changes,
  preserve the existing direction instead of adding novelty to pass a gate.
