# Anti-pattern catalog

Use this as a complete audit catalog. A listed technique is not universally forbidden, but its
default, copied, uncrafted, or context-free form is slop. User direction wins. Context-specific
premium exceptions are in [premium-patterns.md](premium-patterns.md).

## Contents

- [Core diagnosis](#core-diagnosis) | [Writing and content](#writing-and-content) |
  [Typography](#typography) | [Color and atmosphere](#color-and-atmosphere)
- [Icons, logos, and marks](#icons-logos-and-marks) |
  [Pills, cards, borders, and surfaces](#pills-cards-borders-and-surfaces) |
  [Hero and page skeletons](#hero-and-page-skeletons)
- [Section and component templates](#section-and-component-templates) |
  [Spacing, alignment, and clipping](#spacing-alignment-and-clipping) |
  [Motion and interaction](#motion-and-interaction) | [Final meta-check](#final-meta-check)

## Core diagnosis

- AI slop is generic, low-effort, interchangeable output. The root failure is making no real
  creative decision.
- Recoloring, changing fonts, deleting icons, or mechanically dodging this list does not create a
  point of view.
- Reusing a once-good house style across unrelated briefs is still templating.
- Compounding several acceptable-looking prefab blocks produces a louder failure than any one
  detail.

## Writing and content

- **Em dashes**: Treat habitual em dashes as an AI-writing tell. Prefer a hyphen, colon, or separate
  sentence.
- **Filler copy**: Cut walls of copy, stacked lines, decorative labels, and anything not
  load-bearing.
- **Fake proof**: Never fabricate testimonials, impressive percentages, urgency, customer or partner
  identities, logos, or product data and present them as real. Label prototype content as sample,
  but omit invented social proof entirely.
- **Decorative quotes**: Do not wrap emphasis in giant quote marks or use the centered quote-card
  prefab with quote glyph, avatar, title, and fake metric.
- **Reference copying**: Borrow palette mood, type energy, motion, and composition principles, not a
  reference's headline, content, layout, or product window.

## Typography

- **Default tech fonts**: Do not let Inter, Space Grotesk, Sora, Syne, Archivo, or JetBrains Mono
  carry the brand by reflex.
- **Default editorial fonts**: Avoid automatic Fraunces plus Work Sans, Cormorant Garamond, Bodoni,
  Didot, Playfair, or another high-contrast Didone as instant luxury.
- **The Google rotation**: Do not cycle through Onest, Darker Grotesque, Geologica, Hanken Grotesk,
  Spline Sans, Schibsted Grotesk, Gabarito, Figtree, Quicksand, Bagel Fat One, Baloo, Fredoka,
  Chewy, Lobster, Petrona, Hedvig Letters Serif, Brygada 1918, Young Serif, IBM Plex Mono, Spline
  Sans Mono, or Fragment Mono looking for a safe signature face.
- **Tasteful swaps**: Big Shoulders, Newsreader, Instrument Serif, Bricolage, or another known
  designer fallback is still generic when chosen by reputation rather than the brief.
- **Repeated pairing**: Do not reuse the same display face or serif-plus-clean-sans pairing across
  unrelated sites.
- **Neutral versus signature**: A neutral font may serve body copy or an entire task-focused product
  UI. Neutral typography alone is not an identity; let the brief-specific character come from type,
  structure, interaction, content, or another deliberate source. A louder free font is not
  automatically distinctive.
- **Mono as house voice**: Reserve monospace for genuine data such as code, timestamps, prices, and
  tables. Do not costume eyebrows, captions, buttons, copyright, and all labels in mono.
- **One label treatment everywhere**: Do not put every small string in the same tracked uppercase or
  mono style. Give roles distinct treatments or remove the labels.
- **Kicker habits**: Avoid tiny letterspaced uppercase labels, especially above every heading, with
  a dot or short decorative rule beside them.
- **Gradient headline text**: Do not fill a hero word or whole headline with a multicolor gradient
  by default.
- **Saturated accent word**: Do not strand one bright colored or italic word at the bottom of a
  wrapped headline. Keep headlines to one or two deliberate lines and use at most one coherent,
  tonal emphasis.
- **Cramped display type**: Give large words, numbers, separators, and units air. Avoid crushed
  tracking.
- **Off-center strike**: Measure strike-throughs and cut lines against the actual x-height so they
  cross the glyphs optically at center.
- **Letterspaced serif wordmark**: All-caps Cormorant or another stock serif with wide tracking is
  not a luxury identity.
- **Archivo three-way treatment**: Solid, accent, and outline versions of one sporty all-caps face
  do not become three purposeful type voices.
- **Unreadable text**: Maintain a decisive value gap between text and its background, especially
  inside buttons.

## Color and atmosphere

- **Purple and adjacent-hue gradients**: Purple, blue plus purple, and glowy adjacent-hue gradients
  are the default AI palette. Choose a brief-specific palette.
- **Pastel candy wash**: Avoid page-filling butter-yellow, peach, pink, mint, lavender, sherbet, or
  cream gradients.
- **Candy aurora**: Avoid several blurred, drifting radial blobs combined with opacity and
  mix-blend-mode.
- **Cool blue-charcoal**: The stock dark SaaS base near #0c0e15 with blue panels and lilac accents
  is a non-decision. Warm, neutralize, or choose a specific dark hue.
- **Cream and beige**: Oat-milk editorial backgrounds are now as generic as blue-purple gradients.
- **Slop gray**: Avoid gray-100/200 surfaces near #f3f4f6, #eceef2, or #e7ecf3 as an unchosen page,
  footer, section, or card base.
- **Saturated accent everywhere**: A vivid brand hue sprayed across words, dots, buttons, and labels
  reads as templating. Prefer quiet tonal steps.
- **Background glow**: Do not place a generic radial accent blob in every dark hero or CTA.
- **Centered halo**: A warm color does not rescue a symmetric glow ring behind an object. Use a
  directional source with intentional falloff.
- **Cut-off glow**: Never let a glow hit overflow clipping or a section edge and end in a hard line.
- **Colliding colors**: Do not mix unrelated saturated hues or place good components inside muddy,
  incoherent color envelopes.
- **Hard section seams**: Carry a palette smoothly across adjacent sections unless a deliberate
  floor change is part of the composition. Do not put a gradient on every boundary.
- **Hard image seams**: When a full-bleed image is meant to blend into the page, dissolve it into a
  continuous surface instead of leaving an accidental horizontal band. A deliberately framed crop
  may end hard. Use the exact recipe in [implementation-recipes.md](implementation-recipes.md) for
  the blended case.
- **Banded gradients**: Dither large transitions with subtle grain. Visible bands read as cheap.
- **Grain over content**: Put noise on the substrate, behind text, controls, icons, and product UI.
  A deliberate grain mask on one display word is the narrow exception.

## Icons, logos, and marks

- **Lucide everywhere**: Lucide (https://lucide.dev) is a useful general-purpose line-icon library,
  but its uniform thin-stroke set becomes a giveaway when used as the visual voice of every project.
  Common defaults include Sparkles, Coffee, Dumbbell, Plane, and MapPin. It has no brand logos; use
  official brand assets instead.
- **Icon or logo in a tile**: Do not center a big icon in a soft colored rounded square or circle as
  a hero or feature default, or invent such a container behind a brand, social, or integration mark.
  Prefer the bare official mark with intentional size, color, weight, and spacing; preserve an
  official container when it is part of the supplied asset or brand specification.
- **Gradient logo lockup**: A gradient squircle containing an icon beside a generic geometric
  wordmark is a prefab logo.
- **Gradient initials avatar**: Do not use two letters on a blue-purple gradient circle as
  decorative fake proof. A plain, tokenized initials fallback is valid when it honestly represents a
  user without an image.
- **Redrawn icon-pack glyphs**: Drawing the usual document-check, linked-circles, or shield-tick
  outline yourself does not make it custom. Bespoke iconography needs an invented construction.
- **No icons at all**: Removing all icons is not a solution. Use familiar, accessible action icons
  where they improve product comprehension and brand-specific marks where identity matters.
- **Missing or fake marks**: If real social, integration, or customer logos earn their place, use
  official assets at a consistent quiet size. Otherwise omit them. Never invent them or fill space
  with a generic icon row.
- **Default arrow**: A stock right arrow on every CTA is filler. Draw or choose a glyph whose
  stroke, angle, and corners belong to the system.

## Pills, cards, borders, and surfaces

- **Pill eyebrow**: Avoid the tiny icon-plus-label capsule above the hero as default decoration.
- **Glowy pill button**: Avoid a fully rounded gradient button with blurred shadow or glow.
- **Gradient pill stack**: Gradient plus pill plus icon plus uppercase label in one small element is
  an especially loud tell.
- **Metadata chips everywhere**: Use contained status chips only where containment has meaning, not
  around every category, distance, tag, or noun.
- **Kitchen-sink card**: Do not stack icon tile, category pill, tag pills, divider, price, and glowy
  action into one rounded card.
- **Hairline border on every box**: Faint 1px light outlines and inner highlights on all cards,
  stats, and tiles are default component-kit styling.
- **Accent-bar card**: A plain box with one bright edge, icon, number, and caption is a prefab.
- **Default all-around shadow**: Do not bloom a wide symmetric shadow around every card, button,
  icon, SVG, or animated object.
- **Fake shadow box**: Do not route around the shadow rule with a duplicate offset rectangle.
- **Hard-edged shadow**: If the shadow border can be traced or the element's rounded silhouette is
  visibly repeated behind it, the shadow is a second box, not light.
- **Blurred-copy bloom**: Delete glows that are merely the object's own outline blurred and offset.
- **Inner-glow badge**: A bordered chip glowing from within, or a pulsing status dot with an
  expanding halo, is slop.
- **Botched glass**: Do not ship blur pixelation, banding, leaked shadow, resting halos, or blur and
  shadow that pop during interaction. Flat fields give glass nothing to refract.
- **Unrounded hairline rules**: Do not use square-capped rails, eyebrow ticks, or decorative rules
  as substitute structure. Plain separators remain valid in dense product UI when they clarify real
  grouping; otherwise prefer spacing, hierarchy, or invented geometry.

## Hero and page skeletons

- **Default hero stack**: Eyebrow, headline, subline, primary button, and secondary link stacked in
  the center is a prefab.
- **Split hero or right-panel stack**: Avoid the automatic left-column kicker, headline, subtext,
  actions, and stat row beside a framed image, illustration, product card, or other panel. The
  skeleton remains generic whatever the right-hand panel contains.
- **Hero fold miss**: Compose the first viewport deliberately. Do not let a stray, asymmetric slice
  of the next section peek below a too-short hero.
- **Multi-line staircase headline**: Do not let a display headline wrap into three or four short
  accidental rows.
- **Default CTA pair**: Avoid the medium-radius gradient primary with dark text, glow, and trailing
  arrow beside an outlined ghost secondary. More generally, fill plus outline is a marketing preset
  when used automatically. Functional primary/secondary pairs in forms, dialogs, toolbars, and other
  task UI remain valid when two actions are genuinely required and their semantics are clear.
- **Fake macOS window**: Do not use traffic-light dots and an empty rounded desktop mockup as hero
  filler.
- **Fake code window**: Avoid the dark quickstart.ts panel with traffic lights, purple keywords,
  green strings, gray comments, JetBrains Mono, and a toy SDK call.
- **Crude CSS or SVG illustration**: Rounded-div bar charts, gradient spheres, orbit rings, and mock
  stat cards are placeholders, not authored art.
- **Floating card filler**: Do not layer generic cards that bob, parallax, and lift over a hero.
- **Floating image tag**: Avoid the little icon-plus-weather/info pill pinned to an image corner.
- **Grid background**: Do not lay a faint full-page graph-paper grid behind content, even with a
  radial mask. Blueprint cues earn their place only when specific and crafted.
- **Fixed background sheet**: A position-fixed texture that merely follows the whole scroll,
  including behind the nav, is not a signature. It must react, transform, or be removed.
- **Flat page after hero**: Do not spend all atmosphere on the first screen and place every later
  section on one flat dark or cream fill.

## Section and component templates

- **Label-over-heading opener**: Do not open every section with a small uppercase or mono label
  above a larger heading, whether serif or sans. Vary the structure or remove the label.
- **Big serif statement**: Kicker plus one large serif sentence with a single italic word is a
  repeated philosophy-section prefab.
- **Inset enquiry island**: A rounded closing panel containing kicker, serif headline, subline, and
  form is slop when used as the default ending on every site.
- **Email pill form**: A long pill email field beside a pill action is a repeated signup preset.
- **Image card with overlay caption**: Avoid the portrait image, bottom scrim, uppercase metadata,
  serif name, location, description, and arrow-link stack.
- **Three-tier pricing**: Free, Pro, Enterprise cards with per-month price, check list, CTA, and a
  glowing middle card with MOST POPULAR pill are a fixed template.
- **Ragged comparison grid**: Titles, prices, descriptions, lists, and buttons must align across
  columns regardless of copy length. Hold empty slots and anchor actions to the bottom.
- **Countdown boxes**: Do not fake urgency with DAYS, HRS, MIN, SEC tiles unless a real deadline
  requires a timer.
- **Pre-footer CTA slab**: Avoid a wide rounded blue-purple gradient banner with centered headline,
  no-card byline, and one or two buttons.
- **Numbered rail**: A 01/02/03 process list beside a vertical rule is a prefab.
- **Standard footer**: Big wordmark, tagline, full-width rule, four uppercase-mono link columns,
  another rule, and copyright row is tidy but idea-free.
- **Oversized footer wordmark as checkbox**: Giant text that is off-axis, clipped, fighting another
  gradient, or set in default type is not a signature. Use the crafted version or omit it.
- **Whole SaaS meta-skeleton**: Two-column hero, three icon-tile features, audience tabs, pricing,
  FAQ, CTA slab, and ruled multi-column footer in that order is the Stripe/Linear/Vercel clone.
- **House-style recycling**: Kicker headings, serif statement, image cards, inset form island,
  serif-sans pairing, and giant footer wordmark reused together across briefs is a reskinned theme.

## Spacing, alignment, and clipping

- **Text against edges**: Give ordinary copy generous, consistent gutters. Cropping is reserved for
  deliberate oversized art, not normal text.
- **Content flung apart**: Do not maroon clusters against opposite rims with a dead gulf between
  them. Default to shared axes, balance, and the same grid as surrounding content.
- **Chronic centering miss**: Prove content is mathematically and optically centered in buttons,
  pills, circles, tiles, badges, and SVG shapes.
- **Clear the cut**: Any clip-path, notch, overflow hidden, or fixed height must leave all live text
  and controls fully inside the surviving region with padding greater than the cut.
- **Overlap clipping**: Keep content on the visible layer when sections overlap. Never let a layer
  boundary guillotine continuing text or controls.

## Motion and interaction

- **Card hover lift**: Avoid universal translate-up, all-around shadow bloom, and glowing-border
  hover on every card.
- **Hover boop**: Buttons must not jump upward or scale on hover. Change state without moving the
  control.
- **Underline wipe**: Do not animate link or button underlines growing or traveling in.
- **Botched fill**: Keep line caps stable, fill the entire intended track, and use smooth easing.
  Prefer clip or dimension animation over scaling a rounded shape.
- **Invisible-content trap**: Content is visible before entrance animation runs. Never let CSS view
  timelines, IntersectionObserver, Motion, hydration, or JavaScript completion strand already
  rendered text or controls in a hidden animation state.
- **Decorative floating**: Repetitive bobbing without semantic or compositional purpose is filler.
- **Sun-moon toggle**: The sliding pill between stock sun and moon icons is the default theme
  switch. Choose a product-appropriate control.
- **Active-nav dot**: Use type weight or color for a current item, or a genuine sliding indicator,
  not a stray dot under a link.
- **Dead controls**: Activate every in-scope tab, accordion, slider, toggle, and button on the
  affected surface. Static mockup elements must not masquerade as controls.

## Final meta-check

- Ask whether this font, layout, component stack, or interaction was copied from an unrelated brief
  without a brief-specific reason. If yes, change it. Within one product, preserve intentional
  design-system consistency.
- Ask whether each major choice follows from this brief. If it could be swapped onto another
  product, it is not specific enough.
- Do not use this catalog as a negative-only checklist. An expressive page with no signature,
  atmosphere, purposeful interaction or motion, or point of view is still unfinished. A product
  surface does not need scenery, but it does need a brief-specific operational idea expressed
  through structure, state, data, or interaction.
