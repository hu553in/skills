---
name: anti-slop-design
description: >-
  Design, build, refactor, or review distinctive user interfaces that avoid generic AI-generated
  visual patterns while preserving usability, accessibility, responsiveness, and working
  interactions. Use for web pages, mobile or desktop app screens, product UI, landing pages, design
  systems, components, visual polish, frontend implementation that changes rendered behavior or
  presentation, UI audits, screenshot reviews, or any request to make an interface premium,
  creative, cohesive, less generic, or explicitly free of AI slop.
---

# Anti-slop design

## Operating law

Treat this skill as the default for interface work. Follow it before designing, during
implementation, and again before delivery.

- Obey specific, unambiguous user direction over these defaults.
- Resolve conflicts in this order: user and repository constraints, functional correctness and
  accessibility, brief-specific cohesion and usability, then anti-pattern defaults.
- For a full design or full audit, read all three linked references. For a narrow change or review,
  read the applicable sections and their exceptions; expand coverage if shared effects reach other
  surfaces.
- Tell the user that the anti-slop rules are being applied and state the verification scope.
- If a rule blocks requested work, link and quote it and explain why it applies. Resolve routine
  choices from the brief and existing system without asking for permission already granted.
- Never use the catalog mechanically. Avoiding known tells is only the floor. Make an original,
  brief-specific choice and execute it with craft.

Read:

1. [references/anti-patterns.md](references/anti-patterns.md) for every known slop tell and its
   correction.
2. [references/premium-patterns.md](references/premium-patterns.md) for the signature formula,
   premium alternatives, field notes, and component-library guidance.
3. [references/implementation-recipes.md](references/implementation-recipes.md) for fragile
   implementation details and the final rendered verification checklist.

## Workflow

### 1. Ground the brief

- Read repository instructions and inspect the real product, content, data, brand assets, current
  design system, and supported viewports. If the repository has a design contract, theme companion
  docs, machine-readable design config, or a registry file such as `components.json`, read it before
  making visual decisions and verify it against the live implementation. Treat disagreement as
  contract drift: resolve it only within the authorized scope, otherwise report it.
- Distinguish a creation request from a constrained refactor or audit. Preserve an explicit
  no-visual-change contract.
- Classify the surface before applying the signature formula:
  - For marketing, editorial, and brand surfaces, a focal artifact, atmosphere, and expressive
    composition may carry the identity.
  - For product, admin, and dense workflow UI, let information architecture, interaction, data
    display, and operational clarity carry the identity. Do not force a hero, scenic background,
    oversized wordmark, or decorative artifact into a task surface.
- Treat references as design-language direction only. Do not copy their content, headline,
  composition, or product artifact.
- Identify what the thing actually is. Show a product UI only for a real product UI; show a file,
  object, service, or workflow truthfully when that is the product.

### 2. Decide one world before composing sections

Write down or hold a compact art direction:

- audience and desired feeling;
- one disciplined palette;
- one type voice suited to the surface: a characterful display face plus at most one quiet neutral
  on expressive surfaces, or one disciplined neutral system when product identity comes from
  structure and interaction;
- one scope-appropriate signature: a high-effort artifact or, for task UI and narrow changes, an
  interaction, information structure, or exacting brief-specific detail;
- one atmospheric medium or disciplined surface system when the surface benefits from it;
- one bespoke silhouette, geometry, or information-visualization convention where it helps;
- deliberate navigation or workflow orientation;
- real, specific copy, data, logos, and product content;
- one purposeful interaction language, with motion only where it improves feedback, hierarchy, or
  expression.

Reject identity-bearing or compositional choices that could move unchanged to an unrelated product.
Reusable task primitives may remain familiar; specificity should come from how they support this
product, not novelty for its own sake. Prefer one coherent world over a collection of individually
attractive parts. Scale the direction to the task: for a small component or no-visual-change
refactor, preserve the existing system and perfect an in-scope state, behavior, or detail instead of
manufacturing novelty.

### 3. Compose the surface as a whole

- On marketing, editorial, and brand surfaces, art-direct the first viewport as one frame and
  control exactly what appears at the fold.
- On product, admin, and workflow surfaces, compose the first usable viewport around orientation,
  current state, and the primary task. Do not spend its height manufacturing a hero.
- Carry atmosphere through expressive pages and palette or surface continuity through every surface.
- Use foreground, midground, and background when depth supports an expressive concept. Use a clear
  surface and hierarchy ladder when operational clarity matters more.
- Vary section openings and structures on expressive pages. In repeated product structures, keep the
  consistency that makes comparison, navigation, and state recognition faster.
- Keep ordinary text clear of every edge and align repeated or comparable content on a shared grid.
- On expressive surfaces, use few load-bearing words and let hierarchy, space, imagery, and
  interaction carry meaning. In product UI, stay concise without removing instructions, state,
  consequences, or recovery guidance.

### 4. Build with real foundations

- Reuse the project's accessible components and design tokens.
- Prefer tested component primitives over hand-rolled generic controls. Preserve their behavior and
  adapt only in-scope, identity-bearing styling to the existing or chosen visual language.
- When the same local override repeats within the authorized scope, prefer the shared primitive or
  semantic token instead of multiplying one-off classes. Do not broaden a narrow task solely to
  clean up unrelated overrides.
- Keep theme modes on the same semantic token and component contract. Add mode-specific behavior
  only for a real visual difference that tokens cannot express.
- Treat named tools in the references as examples, not dependencies. Inspect the current project and
  current official documentation before choosing a primitive or package. Preserve a working
  primitive base instead of migrating it for fashion.
- Translate CSS- and React-specific recipes to the current platform instead of forcing that stack.
- Do not inject global Tailwind into a mature non-Tailwind project for one block.
- Use supplied or verified marks and data. Never present fabricated customers, partner or
  integration logos, metrics, testimonials, or product data as real. Create a first-party identity
  when the brief requires one, and label prototype data as sample.
- Never let animation initialization or completion determine whether content is visible. Preserve
  the normal server-rendered or static fallback where the architecture provides one, and support
  reduced motion.
- Make every control work. Do not style static mockup elements as interactive controls.

### 5. Verify the rendered result

Run the real interface across representative supported viewports or device classes when a runnable
environment exists. Otherwise inspect the supplied renders and code, and report the verification
limits. For a runnable interface, use platform-appropriate automation and screenshots when
available, and test every in-scope interactive control with actual pointer, keyboard, or touch input
as applicable.

Check:

- no clipping, overflow, accidental seams, or content touching edges;
- mathematical and optical centering;
- aligned comparison rows and bottom-anchored actions;
- readable contrast and clear focus, hover, active, disabled, loading, and error states;
- visible-by-default content with animation disabled, reduced, throttled, or unsupported;
- seamless shadows, glass, gradients, grain, image fades, and section transitions;
- no console errors, dead controls, layout jumps, or broken responsive states.

Use [references/implementation-recipes.md](references/implementation-recipes.md) for exact checks.

### 6. Perform the anti-slop gate

Before calling the work complete:

1. Check the relevant entries in [references/anti-patterns.md](references/anti-patterns.md).
2. Check their context-specific exceptions in
   [references/premium-patterns.md](references/premium-patterns.md).
3. Use [references/implementation-recipes.md](references/implementation-recipes.md) for checks of
   affected geometry, materials, states, and interactions.
4. Compare the rendered UI, not only the code, against every applicable entry.
5. Fix every in-scope violation, including compounded layout tells and incoherence, when the request
   authorizes changes. For an audit or review-only request, report every violation without editing.
6. After a fix, recheck affected criteria and shared dependencies. Repeat cleared checks only for
   new changes, failures, or a specific unresolved concern. Finish after covering the requested
   scope and completing authorized fixes. Report findings in read-only mode and genuine blockers or
   verification limits in either mode. A requested full audit covers the full catalog; a narrow
   change does not require unrelated redesign or repeated full audits.

Do not claim the gate passed unless it actually ran. Report any item that could not be verified and
why.

## Delivery

Report the applicable art direction or audit conclusion, signature decisions, important
implementation changes, viewports and interactions tested, validation performed, and remaining
constraints. Omit categories that do not apply. Keep the report concise, but explicitly confirm the
final anti-slop re-check.

## Source

This skill distills the complete pols.dev anti-slop design law: https://pols.dev/slop.md. The source
snapshot was re-audited on 2026-07-15 at SHA-256
a9e8d49155afba53e2c4621028a2c7bda679dd09841d77bc9c251441d5248ee7. Repetitions are merged,
context-dependent exceptions are preserved, and time-sensitive toolkit claims are corrected against
current official documentation.
