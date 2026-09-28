# 001 — Add press feedback to primary CTA buttons

- **Status**: DONE
- **Commit**: 7e915e1
- **Severity**: HIGH
- **Category**: Physicality (missing feedback)
- **Estimated scope**: 1 file (`css/style.css`), 3 rule blocks touched

## Problem

`.btn-primary`, `.btn-secondary`, and `.btn-pill-white` — the three button classes used for every primary CTA on the site (Search yachts, Continue, Check availability for my date, Find a yacht, Explore our fleet, etc.) — have `:hover` styles but no `:active` (press) state at all.

This site is a yacht-charter lead-gen site; the majority of real visitors are on touch devices, where `:hover` never fires naturally. Tapping any of these buttons currently gives the user **zero visual confirmation the tap registered** until the page finishes navigating or the JS handler runs. This is exactly the "pressable elements with no press feedback" gap called out in the audit's Physicality category.

Current code, `css/style.css:23-46`:

```css
.btn-primary {
  background: var(--teal);
  color: #fff;
  padding: .6rem 1.25rem;
  border-radius: 999px;
  font-weight: 600;
  font-size: .875rem;
  transition: opacity .15s ease, transform .15s ease;
  display: inline-block;
}
.btn-primary:hover { opacity: .9; transform: translateY(-1px); }

.btn-secondary {
  background: transparent;
  color: var(--navy);
  border: 1.5px solid var(--navy);
  padding: .6rem 1.25rem;
  border-radius: 999px;
  font-weight: 600;
  font-size: .875rem;
  display: inline-block;
  transition: background .15s ease, color .15s ease;
}
.btn-secondary:hover { background: var(--navy); color: #fff; }
```

Current code, `css/style.css:115-127`:

```css
.btn-pill-white {
  background: #fff;
  color: var(--navy);
  padding: .75rem 1.5rem;
  border-radius: 999px;
  font-weight: 600;
  font-size: .875rem;
  display: inline-flex;
  align-items: center;
  gap: .5rem;
  transition: transform .15s ease, box-shadow .15s ease;
}
.btn-pill-white:hover { transform: translateY(-1px); box-shadow: 0 8px 20px rgba(0,0,0,.18); }
```

## Target

Add an `:active` rule to each of the three classes with a subtle press-down scale, per the audit's physicality guidance (`transform: scale(0.97)` on `:active`, kept in the 0.95–0.98 range, `transition: transform 160ms ease-out` — audit calls this out explicitly as the standard press-feedback recipe). Use the literal `cubic-bezier(0.23, 1, 0.32, 1)` curve — this repo has no shared easing token file, so every rule hand-types its curve (see Repo conventions below).

```css
/* target: css/style.css:23-33 */
.btn-primary {
  background: var(--teal);
  color: #fff;
  padding: .6rem 1.25rem;
  border-radius: 999px;
  font-weight: 600;
  font-size: .875rem;
  transition: opacity .15s ease, transform 160ms cubic-bezier(0.23, 1, 0.32, 1);
  display: inline-block;
}
.btn-primary:hover { opacity: .9; transform: translateY(-1px); }
.btn-primary:active { transform: scale(0.97); }
```

```css
/* target: css/style.css:35-46 */
.btn-secondary {
  background: transparent;
  color: var(--navy);
  border: 1.5px solid var(--navy);
  padding: .6rem 1.25rem;
  border-radius: 999px;
  font-weight: 600;
  font-size: .875rem;
  display: inline-block;
  transition: background .15s ease, color .15s ease, transform 160ms cubic-bezier(0.23, 1, 0.32, 1);
}
.btn-secondary:hover { background: var(--navy); color: #fff; }
.btn-secondary:active { transform: scale(0.97); }
```

```css
/* target: css/style.css:115-127 */
.btn-pill-white {
  background: #fff;
  color: var(--navy);
  padding: .75rem 1.5rem;
  border-radius: 999px;
  font-weight: 600;
  font-size: .875rem;
  display: inline-flex;
  align-items: center;
  gap: .5rem;
  transition: transform 160ms cubic-bezier(0.23, 1, 0.32, 1), box-shadow .15s ease;
}
.btn-pill-white:hover { transform: translateY(-1px); box-shadow: 0 8px 20px rgba(0,0,0,.18); }
.btn-pill-white:active { transform: scale(0.97); }
```

Note: `.btn-primary:hover` already sets `transform: translateY(-1px)`. On `:active`, the scale rule below it in the cascade will correctly override the hover transform (CSS applies the last matching rule of equal specificity when both `:hover` and `:active` match, which happens on a tap-and-hold) — no `!important` needed, just keep `:active` declared after `:hover` in source order as shown above.

## Repo conventions to follow

- This codebase has no shared token file for easing — durations/curves are hand-typed per rule in `css/style.css` (e.g. `.15s ease` appears independently in `.nav-link`, `.btn-primary`, `.btn-secondary`). This plan does not introduce a token file either — use the literal `cubic-bezier(0.23, 1, 0.32, 1)` value everywhere it's called for below. Consolidating into a shared `--ease-out` token is a separate, not-yet-planned improvement — do not attempt it here.
- The floating WhatsApp button already does this correctly — treat it as the exemplar: `js/layout.js:114` — `class="... transition hover:scale-105 active:scale-95"` (Tailwind utility classes, `active:scale-95` = `transform: scale(0.95)` on `:active`). The three plain-CSS button classes in `css/style.css` should now match this same press-feedback pattern.

## Steps

1. In `css/style.css`, edit the `.btn-primary` rule (currently lines 23-32) and add `.btn-primary:active { transform: scale(0.97); }` immediately after the existing `.btn-primary:hover` rule (line 33). Update the `transition` line to include `transform 160ms cubic-bezier(0.23, 1, 0.32, 1)` in place of the existing bare `transform .15s ease` (keep `opacity .15s ease` as its own comma-separated term, unchanged).
2. In `css/style.css`, edit the `.btn-secondary` rule (currently lines 35-45) and add `.btn-secondary:active { transform: scale(0.97); }` immediately after the existing `.btn-secondary:hover` rule (line 46). Add `, transform 160ms cubic-bezier(0.23, 1, 0.32, 1)` to the end of the existing `transition` line (line 44) — do not remove the existing `background .15s ease, color .15s ease` terms.
3. In `css/style.css`, edit the `.btn-pill-white` rule (currently lines 115-126) and add `.btn-pill-white:active { transform: scale(0.97); }` immediately after the existing `.btn-pill-white:hover` rule (line 127). Update the `transition` line (line 125) so the `transform` term reads `transform 160ms cubic-bezier(0.23, 1, 0.32, 1)` instead of `transform .15s ease` (keep `box-shadow .15s ease` unchanged).
4. Rebuild the compiled Tailwind stylesheet so the change is reflected in what the browser actually loads: run `./node_modules/.bin/tailwindcss -i ./css/tailwind-input.css -o ./css/tailwind.css --minify` from the project root. (This CSS lives in hand-written `css/style.css`, not in Tailwind's generated output, but rebuilding is harmless and keeps the two files' timestamps consistent — skip this step only if it errors, and report the error instead of improvising a fix.)

## Boundaries

- Do NOT touch any `.html` or `.js` file — this is a CSS-only fix, three rule blocks in `css/style.css`.
- Do NOT change the `:hover` behavior of any of the three classes — only add `:active` rules and extend the existing `transition` shorthand.
- Do NOT introduce a new token file or `--ease-out` CSS custom property as part of this plan. Use the literal `cubic-bezier(0.23, 1, 0.32, 1)` value shown above.
- Do NOT modify the floating WhatsApp button (`js/layout.js:114`) — it already has correct press feedback and is the exemplar, not part of the scope.
- If the current code at any cited line doesn't match what's quoted above (drift since commit `7e915e1`), STOP and report instead of improvising.

## Verification

- **Mechanical**: no build step is required to view changes (static site, no bundler for HTML/JS). Confirm `css/style.css` is valid CSS by opening it in a browser dev tools "Sources" tab with no parse errors, or run `npx stylelint css/style.css` if stylelint is available (it is not currently configured in this repo — skip if it errors with "no config found", don't add a config as part of this plan).
- **Feel check**: open `http://localhost:8080/index.html` (start the site with `python3 -m http.server 8080` from the project root if not already running). For each of the three button styles (e.g. "Explore our fleet" = `.btn-pill-white`, "Find my yacht" in the header = `.btn-primary`, "Plan with us on WhatsApp" = `.btn-secondary`):
  - Click and hold the mouse down on the button without releasing. Confirm it visibly shrinks slightly (scale down) while held, and returns to normal size on release.
  - In Chrome DevTools, open the Animations panel, trigger the press, and set playback to 10% — confirm the scale-down happens smoothly over ~160ms, not instantly.
  - Confirm the hover state (translateY / background change, whichever applies to that button) still works correctly and is not broken by the new `:active` rule.
  - On an actual touch device or Chrome's device-toolbar touch emulation, tap the button and confirm you can see/feel the press state even briefly, unlike before.
- **Done when**: all three button classes shrink to ~97% scale on `:active` with a visible, smooth (not instant) transition, existing hover behavior is unchanged, and no other page layout is affected.
