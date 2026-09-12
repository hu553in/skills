---
name: anti-slop-design
description: >-
  Design or review interface visual identity and polish, avoiding generic AI-template styling. Use
  for visual design, rendered UI audits, or requests for a distinctive, less generic interface.
---

# Anti-slop design

Make the interface specific to its product, content, and audience. Removing familiar visual tells is
not a design direction, and novelty alone is not an improvement.

## Scope and design intent

- User decisions and repository constraints take precedence over stylistic defaults. Preserve
  existing designs, frameworks, accessible primitives, and explicit no-visual-change contracts. Do
  not turn a small edit into a visual overhaul, dependency migration, or design-system rewrite.
- Ground visual choices in the affected product, real content, assets, and existing tokens. Consult
  design contracts, theme docs, or registry configuration when the change touches their decisions;
  resolve drift only within scope and report it otherwise.
- For marketing, editorial, and brand surfaces, a coherent palette, type voice, focal artifact,
  atmosphere, and composition can carry identity. Use only what the brief needs.
- For product, admin, and dense workflow UI, prioritize information architecture, state, data,
  navigation, and useful interactions. Do not force heroes, scenery, giant type, or decorative
  artifacts into task surfaces. Familiar controls and consistent repeated structures are valid.
- Treat inspiration as design-language direction, not content or layout to copy. This does not
  override a user's request to implement a supplied design faithfully.

## References on demand

Load only the reference sections needed for the current decision; no reference is a prerequisite for
every edit.

- [Anti-pattern catalog](references/anti-patterns.md): specific visual tells and corrections when
  designing or reviewing affected typography, color, layout, content, or motion. A requested full
  anti-slop audit covers the catalog across its declared surfaces, not the entire product.
- [Premium patterns and exceptions](references/premium-patterns.md): when choosing a new visual
  direction, judging a context-dependent exception, changing a design contract, or evaluating a
  component foundation. The signature formula and toolkit list are options, not requirements.
- [Implementation recipes and verification](references/implementation-recipes.md): when affected
  work involves clipping, comparison alignment, centering, shadows, image blending, glass, motion,
  or a rendered-verification checklist. Adapt recipes to the existing platform.

## Implementation boundaries

- Reuse semantic tokens and accessible components. Consolidate repeated overrides at their shared
  source only when that change is in scope. Preserve parallel token and behavior contracts across
  supported themes.
- Named libraries are examples, not reasons to install dependencies. Keep the working primitive
  base, framework, styling system, and registry settings. Do not inject global Tailwind into a
  mature non-Tailwind project for one block.
- Use supplied or verified marks and data. Never fabricate customer proof, testimonials, metrics, or
  third-party identities. Create a first-party identity when the brief requires one. Label prototype
  data as sample and represent the actual product truthfully.
- Preserve authorization boundaries: sensitive content and metadata must not be delivered merely to
  hide them on the client. Visual changes must retain accessible semantics, focus behavior,
  contrast, and meaningful state and recovery guidance.
- Rendered content must remain visible if animation never starts or finishes. Preserve static or
  server-rendered fallbacks where available and support reduced motion.
- Implement in-scope controls; static mockup elements must not masquerade as working controls.

## Completion and verification

For rendered changes, inspect the actual affected interface at representative supported viewports,
themes, and states. Exercise changed interactions with applicable pointer, keyboard, or touch input;
include affected uses of shared primitives. Check relevant layout, contrast, focus, content
visibility, motion fallbacks, and runtime errors. Use existing platform tooling and screenshots
where available; do not add dependencies or tests solely to satisfy this skill.

Match verification to the change: a local spacing fix needs rendered geometry checks, not a full
interaction audit. A full UI audit covers every declared surface and its applicable criteria. For
non-rendered changes, use checks of the affected contract. If the interface cannot run, inspect
available renders and code and state what remains unverified.

Compare the result against relevant anti-patterns and their exceptions. Complete authorized in-scope
fixes and recheck affected behavior; revisit cleared areas only for new evidence. Reviews remain
read-only unless fixes are requested. Stop when the requested scope is covered, not when every
optional premium technique has been added.

Report substantive changes or findings, actual rendered checks and interactions tested, and any
remaining limitations. Do not claim checks passed when they did not run.
