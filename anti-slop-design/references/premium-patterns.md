# Premium patterns and exceptions

Premium work is not defined by avoiding techniques. It is defined by specificity, cohesion, craft,
restraint, and a point of view. Many slop techniques have a premium form when they are executed for
one brief instead of copied as defaults.

## Contents

- [The signature formula](#the-signature-formula) |
  [Adapt the signature to the surface](#adapt-the-signature-to-the-surface) |
  [Cohesion and field-tested direction](#cohesion-and-field-tested-direction)
- [Treat the design system as a contract](#treat-the-design-system-as-a-contract) |
  [Type selection](#type-selection) | [Premium forms](#premium-forms-of-common-techniques) |
  [Product-as-artifact exception](#product-as-artifact-exception)
- [Professional with a heartbeat](#professional-with-a-heartbeat) |
  [Component foundations](#component-foundations)

## The signature formula

For expressive surfaces, build a coherent direction from the applicable parts of:

1. **One signature artifact**: Decide the custom, high-effort focal object first. Use a crafted SVG
   scene, authored illustration, detailed product artifact, character, texture, render, or prepared
   image that could not belong to another brand.
2. **Atmosphere**: Compose a background environment with depth and mood instead of a flat fill.
3. **Layered depth**: Establish foreground copy, a midground focal object, and a background scene.
   Let at least one element cross a layer boundary when it supports the concept.
4. **A real product artifact when product UI is shown**: Populate it with truthful copy, data,
   controls, states, and details. Empty placeholder boxes are not product proof.
5. **Characterful display type**: Let the signature line carry personality. Keep body copy quiet.
6. **One bespoke silhouette**: Use one unmistakable notch, chamfer, bracket, cut, torn edge, receipt
   edge, or other invented geometry instead of ten decorated rectangles.
7. **Treated navigation when present**: Make its placement, containment, scale, and marks part of
   the visual system, not a default row bolted on top.
8. **Real specificity**: Use supplied real names, product data, company marks, content, and
   vocabulary. When they are unavailable, use clearly labeled, domain-plausible sample content and
   omit customer proof.

In compact form:

signature artifact + atmosphere + layered depth + character type + bespoke silhouette + treated
nav + real specifics

Missing a brief-specific signature cannot be rescued by clean spacing. Clean is the floor.

## Adapt the signature to the surface

Treat the formula as a marketing and brand composition model, not a demand for decorative heroes
everywhere.

- On marketing and editorial surfaces, the signature may be a scene, object, expressive type
  composition, or atmospheric hero.
- On product and admin surfaces, the signature may be exceptional information architecture, a
  command workflow, a data visualization language, a spatial model, or a highly tuned interaction.
- Keep dense task UI fast, legible, and operationally calm. Do not add scenery, giant type, glass,
  or ornamental motion merely to prove the interface is distinctive.

## Cohesion and field-tested direction

Let these source field notes outrank optional premium moves when they conflict.

- Pick one visual world and make every element serve it.
- Hold one disciplined palette. A monochrome or tightly related family beats several unrelated
  accents.
- Use one type voice: one family across optical sizes and weights, or one character display face
  plus one true neutral.
- Choose one consistent medium for creative imagery, such as cyanotype, riso, pixel art, one
  illustration language, or a painted environment. Creative does not mean stock-style realism.
- Compose sections from the world, not from a recolored block library.
- Keep calm interfaces alive with authored response. On expressive surfaces this often means motion;
  in task UI it may be immediate feedback, direct manipulation, or useful state behavior. Deliberate
  stillness is valid; accidental deadness is not.
- Lift design language from references, never their content.

## Treat the design system as a contract

Treat a useful repository design document as an implementation contract, not a mood board. Derive it
from the product that exists, then keep it aligned with the live tokens, primitives, content model,
and interaction rules.

- State the product's operational north star and classify each surface. Marketing can be scenic;
  routine product, admin, and settings UI should be dense, scannable, calm, and immediately usable.
- Reuse existing primitives and defaults before inventing a control. If the same override appears
  repeatedly within the authorized scope, change the shared default instead of accumulating local
  patches.
- Define colors by semantic role, such as canvas, surface, overlay, text, action, focus, success,
  warning, and destructive. Keep a vivid accent scarce and purposeful. Never use color as the only
  state cue.
- Build one intentional surface ladder. Static structure can rely on tonal steps, borders, rings,
  spacing, and density; reserve shadows for surfaces that actually float. Use a card when
  containment has a real job, such as grouping a repeated item, form, overlay, or framed tool, not
  as the default wrapper for every section. Group inside it with rows, dividers, or fieldsets
  instead of nested cards.
- Make user-relevant state explicit, especially access, visibility, ownership, payment, loading,
  error, and destructive consequences. Keep independent state dimensions separate rather than
  compressing them into one badge or color.
- Treat gated and sensitive content as an authorization boundary. Render only authorized content,
  previews, placeholders, and metadata; do not rely on client-only hiding.
- Give fixed-format controls and repeated content stable dimensions so hover, loading, translated
  copy, and icons do not resize the layout. Test the smallest supported width with both short and
  long content.
- Let real media, identity, data, and workflow detail supply richness in product UI. Do not add
  decoration to compensate for missing content.
- Keep data, filters, status, and actions near the thing they affect. Use the product's vocabulary
  and label actions by their actual result. Empty states should name what is missing and point to
  the next useful action; errors should explain what failed and offer retry or a safe exit.

Use one base design contract plus small theme-specific companion documents when modes genuinely
differ. Keep semantic token names and component behavior parallel across modes; document only the
palette, surface hierarchy, contrast, media, and interaction exceptions. Avoid copying the whole
base contract into each theme file. When authorized work changes the contract, keep machine-readable
design metadata, the human-readable contract, and the live implementation in sync.

## Type selection

- Choose type by rendered fit to the brief, not by reputation or trend. View candidates before
  deciding.
- Prefer a properly licensed character face when identity depends on type, and self-host it only
  when the license permits and the project benefits. Foundries and free font catalogs are sources to
  explore, not approved shortlists. Verify the exact family, files, webfont license, language
  coverage, and current availability before use.
- Do not treat a non-Google catalog as automatically distinctive. Once-popular startup grotesques
  can become defaults too. Render candidates in the real copy before choosing.
- A system UI stack is a legitimate neutral body. Inter can also work as a quiet workhorse when it
  does not carry the identity.
- A signature serif, one italic word, or one accent word can work only when the face is genuinely
  brief-specific, the headline is controlled, and the move is not the repeated house style.

## Premium forms of common techniques

- **Liquid glass**: Use over a rich backdrop worth refracting. Include a clean gloss lip, subtle
  edge dispersion, tuned frost, inner light, and tight tinted shadow. No banding, leak, halo, or
  interaction pop. See [implementation-recipes.md](implementation-recipes.md).
- **Tonal elevation**: Shift a surface slightly from the background, use a low-opacity self-colored
  1px edge, and add a soft top inner highlight. Let the edge be felt rather than drawn.
- **Bespoke geometry**: Turn a plain accent edge into a specific notch, chamfer, bracket, kick, or
  custom connector.
- **Bare icons**: Place marks directly on the surface with intentional weight and spacing.
- **Custom iconography**: Draw a consistent house set with its own construction, stroke, corners,
  and grid for identity-bearing marks. Keep familiar action glyphs recognizable in task UI; do not
  sacrifice comprehension merely to make every control bespoke.
- **Authored micro-interactions**: Write motion for the specific element. Tune easing and keep
  shadows tight. A custom line may travel through invented geometry, but do not fall back to a
  generic underline wipe.
- **Considered light**: Choose color, direction, and falloff. A warm volumetric rake or single beam
  can work; an automatic radial bloom cannot.
- **Premium grain**: Use very low-opacity film or Perlin noise to texture a surface and remove
  banding. Keep it behind readable content.
- **Full-page composition**: Treat the viewport as one frame with confident scale, negative space,
  oversized type, and shapes that are deliberately larger than timid defaults.
- **Real logo wall**: Use only marks the product can honestly claim, in one quiet color and even
  optical size.
- **Blueprint or canvas detail**: A few ruler ticks, crop marks, guides, or an actual technical
  drawing can evoke craft. A precise, localized textured micro-grid can work. Full-page graph paper
  cannot.
- **Inset island**: A detached section with breathing room on all sides can be strong when it is a
  rare, brief-specific object, not the default closing CTA.
- **Crafted SVG**: Correct proportions, layered detail, authored color, and intentional light make a
  custom SVG premium. Rounded placeholder shapes do not.
- **Grainy gradient**: Dither large color transitions so they feel physical and do not band.
- **Scroll-authored motion**: Use subtle, fast scroll-linked change or parallax on already-visible
  content. Honor reduced motion and preserve the static fallback.
- **Oversized footer wordmark**: Compose it with deliberate case, tracking, texture, and alignment.
  Keep glyphs whole except for intentional edge bleed, place it above the background texture, and
  anchor it flush to the bottom with no accidental gap.
- **Full-bleed atmospheric hero**: Let one photographic, painted, rendered, SVG, or prepared scene
  own the entire hero. The background is the art, not a flat fill with a glow.
- **Animated character field**: Low-contrast glyphs can form a data or security atmosphere when the
  field truly drifts or reacts, stays behind content, and respects reduced motion.
- **Gradient-filled custom mark**: A tiny multi-stop gradient inside one crafted SVG icon can read
  like an enamel jewel. Keep it rare and contained.
- **Bespoke arrow**: An up-right or otherwise specific arrow with system-matched stroke and corners
  can replace the stock horizontal CTA arrow.
- **Premium glass CTA**: A glossy glass action earns its place only over an atmospheric backdrop and
  only after blur, gloss, edge, and shadow are seamless.

## Product-as-artifact exception

A faux app window is slop when it is generic, empty, or unrelated. A detailed, fully populated,
working representation of the real product can be the signature artifact. Use real controls, copy,
diffs, states, and data. Do not create a dashboard for a product that is actually a file or another
non-dashboard object.

## Professional with a heartbeat

Sparse, correct, well-typed work can still be unfinished. On expressive surfaces, add a few authored
creative moments. On product and admin surfaces, the heartbeat may instead be a crisp state
transition, direct manipulation, useful data behavior, or another interaction that improves the
task:

- responsive nav behavior;
- a signature object that drifts, reacts, or changes with scroll;
- crafted hover states;
- a precise state or data transition that clarifies cause and effect;
- kinetic type or a precisely aligned animated mark;
- a textured footer composition;
- visible-by-default scroll-linked movement.

Do not use every premium move. Choose the smallest set that reinforces one system. Using serif,
ASCII field, glass, gradient icons, and a full-bleed scene at once usually creates noise.

## Component foundations

Use the project's existing accessible primitives first. Treat this named list as a dated discovery
aid, not a required stack. Before using any item, re-check its official docs, license and access,
supported framework and primitive base, generated files, and dependencies. If `components.json` or
an equivalent registry config exists, preserve its style and primitive base, framework and language
output, aliases and target paths, CSS setup and prefix, icon and RTL settings, and registry
namespaces unless the task authorizes a change. Resolve and preview the actual namespaced item: a
live registry need not support the configured base or component style. Keep the host project's
working conventions.

- **Motion** (https://motion.dev): The current React package is motion and its React entry point is
  motion/react. Use it when springs, gestures, scroll transforms, numeric transitions, marquees, or
  layout animation justify a runtime library.
- **shadcn/ui** (https://ui.shadcn.com): This is an open-code component distribution system, not a
  conventional component package. As of 2026-07-15, new projects default to Base UI, while Radix
  remains supported. Inspect the existing project base and preserve it; do not migrate a working
  Radix or Base UI project just because the default changed.
- **Base UI** (https://base-ui.com): An unstyled, accessible React primitive library that can work
  with Tailwind, CSS Modules, plain CSS, or CSS-in-JS. Consider it directly when the project needs
  headless primitives rather than shadcn's distributed component layer.
- **Tailark** (https://tailark.com): A shadcn registry for marketing blocks and pages. The catalog
  includes free and paid material; use a block as a structural start, not a finished art direction.
- **motion-primitives** (https://motion-primitives.com): Reusable animated components installed by
  CLI or copied as source. Keep content visible before animation and replace identity-bearing
  defaults that do not fit the product.
- **Kokonut UI** (https://kokonutui.com): Tailwind, shadcn, and Motion components installed through
  a shadcn registry or copied as source.
- **React Bits** (https://reactbits.dev): Animated React components and visual effects available
  through source and registry workflows. Use individual pieces only when their motion supports the
  concept; test static fallback, performance, and reduced-motion behavior.
- **ogimagecn** (https://www.ogimagecn.com): Customizable Open Graph image components built on
  Satori and distributed for shadcn-style use. Treat generated social images as a separate rendered
  surface: verify font loading, text overflow, image constraints, localization, and metadata
  privacy.
- **ReUI** (https://reui.io): A broad shadcn-oriented catalog of components, application patterns,
  data-grid pieces, blocks, and icons. Prefer the narrowest useful piece over a full template.
- **Magic UI** (https://magicui.design): A React, TypeScript, and Tailwind collection of
  marketing-oriented components and effects; many items depend on Motion. Keep content readable
  before animation runs and do not let its effects become the product's identity by default.
- **Dice UI** (https://diceui.com): Composable shadcn registry components for advanced product
  interactions such as data display, media, editing, and drag-and-drop. As of 2026-07-15, its
  component docs are Radix-backed; inspect compatibility before mixing them into a Base UI project.
  Test semantics, keyboard behavior, touch, and edge cases rather than assuming a complex copied
  control is finished.

In Tailwind projects, use compatible items directly when they fit. In non-Tailwind projects, Motion
can work independently; adapt useful structure and behavior into the existing styling system. Never
add global Tailwind to a large existing codebase for one block.

Prebuilt pieces are a head start, not a design pass. Keep accessible behavior and sound structure,
then replace blue-purple gradients, glowy pills, fill-plus-outline button pairs, sun-moon toggles,
tracked caps, and default hero stacks. Audit library output with the same rigor as custom code.
