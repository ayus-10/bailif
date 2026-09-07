---
name: vue-vuetify-ui-style
description: House style for building or restyling Vue 3 + Vuetify 3 UI components — clean, flat, information-dense, elegant rather than shiny. Use this whenever writing, reviewing, or redesigning any .vue component, Vuetify markup, or scoped CSS for a Vue project, even if the user just says "build a button/toolbar/card/modal" without mentioning style explicitly. Also use when the user asks to make a UI "look better," fix hover/focus states, adjust colors, spacing, radius, or general polish on an existing Vue component.
---

# Vue/Vuetify UI Style

Role: an expert Vue 3 and Vuetify 3 frontend developer specializing in clean, modern, information-dense UI. The target look is elegant, flat, compact, and well-structured — closer to a polished internal tool (Linear, Notion) than a generic SaaS dashboard kit.

## Core aesthetic principles

- **Flat by default.** No box-shadows, elevations, gradients, or glowing rings used as decoration. Separate elements with structural borders, not shadows.
- **Functional shadows only, and quiet ones.** The one exception is a state that genuinely needs to communicate something — e.g. a valid drag-and-drop target. Even then, use a thin inset border-tint (`box-shadow: inset 0 0 0 0.0625rem rgba(...)`) rather than a soft blurred glow, paired with a faint background tint.
- **High information density, comfortable to scan.** Tight padding where things belong together, generous spacing where separation helps.
- **Precision over decoration.** No gradient shine, no hover "lift" effects, no numbered circle badges unless the content is genuinely a sequence.
- **Elegant, not shiny.** If a hover or focus treatment could be described as "flashy," it's wrong. The bar: does this look intentional and quiet, or like it's trying to impress someone.

## CSS rules

- Avoid `!important`, but don't contort to eliminate it. Prefer fixing specificity by targeting Vuetify's actual internal class structure (e.g. `.v-field--variant-outlined .v-field__outline`) rather than fighting it blind. `!important` is acceptable as a last resort against a Vuetify component's own high-specificity/inline styles — treat it as a signal to double-check the selector first, not a default tool.
- Use `rem` for all sizing (font-size, padding, margins, border-radius, width/height); `%` for relative layouts. Base `16px` = `1rem`.
- No CSS comments inside `<style>` blocks.
- Always `<style scoped>`. Override Vuetify internals via `:deep(.your-custom-class .v-component-class)`.

## Color & theming

Never hardcode raw hex where a theme token exists. Vuetify theme variables are RGB channel triplets, not hex strings — wrap them: `rgb(var(--v-theme-[name], r, g, b))`, or they silently fail and you're just seeing the fallback.

| Purpose                                                   | Token                                                                                                                                                                                              |
| --------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Backgrounds                                               | `rgb(var(--v-theme-surface))` / `rgb(var(--v-theme-surface-variant, 248, 249, 250))`                                                                                                               |
| Borders                                                   | `rgb(var(--v-theme-outline, 225, 228, 232))` / `rgb(var(--v-theme-outline-variant, 234, 236, 240))`                                                                                                |
| Primary action / active-selected state                    | Vuetify default blue `#1976d2` (or `rgb(var(--v-theme-primary))`) — used sparingly: active filters, selected states, badges, the one primary CTA. Never a default hover color on neutral controls. |
| Text (primary)                                            | `rgb(var(--v-theme-on-surface))`                                                                                                                                                                   |
| Text (secondary/labels/descriptions)                      | `rgb(var(--v-theme-text-secondary, 71, 84, 103))` — not `on-surface-variant`, which renders too light                                                                                              |
| Text (quiet/decorative icons, placeholder-weight content) | `rgb(var(--v-theme-text-disabled, 148, 157, 173))`                                                                                                                                                 |

Don't introduce a second accent color (e.g. purple). One accent used narrowly beats two competing accents.

## Typography

- Titles/headers: `0.875rem`, `font-weight: 700`, `letter-spacing: -0.01em`.
- Standard labels/body-adjacent text: `0.8125rem`, `font-weight: 600`.
- Button/control text: `0.8125rem`, `font-weight: 500` — one step lighter than standard labels; 600 reads heavy on compact buttons.
- Subtext/captions/badges: `0.6875rem`–`0.75rem`, `font-weight: 600`–`700`.
- Uppercase meta (rare — only real badges like a visibility tag): add `letter-spacing: 0.05em`. Don't default to uppercase labels.

## Shapes & borders

- Card/container radius: `0.75rem`.
- Input/button radius: `0.5rem`–`0.625rem` (primary CTA can sit at the top of that range).
- Pills/badges (counts, tags): fully round, `border-radius: 999px` — keep badges and buttons in one shape family, don't split radius systems.
- Micro-elements (thin tracks, dividers): `0.125rem`.
- Border thickness: `0.0625rem` solid, standardized.

## Interaction states

- **Hover:** subtle only. A neutral icon/text shifting to the accent color on hover is enough — avoid stacking a background fill _and_ a color change _and_ a border change on the same element at once.
- **Focus:** must be visible for accessibility, but never a glowing halo. For buttons/icon-buttons, a quiet low-opacity ring is fine: `box-shadow: 0 0 0 0.1875rem rgba(25, 118, 210, 0.15)`. For text inputs, prefer shifting the border color/weight itself (muted grey → `on-surface`) over any shadow — reads as sharpening, not lighting up.
- **Ripple:** use `v-ripple` on both `v-btn` and any native `<button>` acting as a button — it works on any element, no reason to skip it on custom buttons.
- **Text selection:** any button or button-like control (including static badges inside a control row) gets `user-select: none; -webkit-user-select: none;`.
- **Drag-and-drop / other functional states:** always show feedback — an unstyled drop zone is a bug, not restraint. Keep it to a faint tint + thin inset border, never a colored glow.

## Vuetify component defaults

**Inputs** (`v-text-field`, `v-select`, `v-textarea`): `variant="outlined"`, `density="compact"`, `hide-details` or `hide-details="auto"`. Target the actual internal parts with `:deep()` — `.v-field__outline`, `.v-field__outline__start`, `.v-field__outline__end`, `.v-field__outline__notch::before`/`::after` — not just the parent `.v-field`, or overrides on the notch/label gap won't apply.

**Buttons** (`v-btn`):

- `variant="flat"` for primary actions, no custom shadow on top.
- `variant="text"` for secondary/icon-only actions.
- Primary CTA: `density="comfortable"`. Everything else: `density="compact"`.
- `text-none` class to prevent uppercase transform.
- For a custom button the framework doesn't cleanly support (e.g. a badge embedded in a button), use a native `<button>` with `v-ripple` and custom CSS rather than forcing `v-btn` to do something it wasn't built for.

**Lists/Navigation** (`v-list`, `v-navigation-drawer`): `elevation="0"`, `density="compact"`, `nav` prop, explicit icon sizes (e.g. `size="1.125rem"`) rather than relying on defaults.
