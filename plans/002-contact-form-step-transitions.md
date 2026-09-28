# 002 — Animate the quote form's step transitions

- **Status**: DONE
- **Commit**: 7e915e1
- **Severity**: HIGH
- **Category**: Missed opportunity / state teleport (audit category 8)
- **Estimated scope**: 1 file (`contact.html`), CSS additions + 3 JS handlers rewritten

## Problem

`contact.html` has a 2-step quote form (the single most commercially important interaction on the entire site — this is how leads are captured) plus a confirmation screen. All three transitions between states are instant `classList.add("hidden")` / `classList.remove("hidden")` swaps with zero motion:

Current code, `contact.html:133-150`:

```js
document.getElementById("toStep2").addEventListener("click", () => {
  document.getElementById("step1").classList.add("hidden");
  document.getElementById("step2").classList.remove("hidden");
  document.getElementById("stepDot1").className = "";
  document.getElementById("stepDot2").className = "text-teal";
});
document.getElementById("backStep1").addEventListener("click", () => {
  document.getElementById("step2").classList.add("hidden");
  document.getElementById("step1").classList.remove("hidden");
  document.getElementById("stepDot1").className = "text-teal";
  document.getElementById("stepDot2").className = "";
});
document.getElementById("quoteForm").addEventListener("submit", (e) => {
  e.preventDefault();
  document.getElementById("quoteForm").classList.add("hidden");
  document.getElementById("refNum").textContent = "#PYR-" + Math.floor(100000 + Math.random()*900000);
  document.getElementById("confirmation").classList.remove("hidden");
});
```

The relevant markup, `contact.html:48-108` (abbreviated — full content unchanged, only the wrapping elements matter for this plan):

```html
<form id="quoteForm">
  <div id="step1" class="space-y-4">
    ... fields ...
    <button type="button" id="toStep2" class="btn-primary w-full">Continue</button>
  </div>

  <div id="step2" class="hidden space-y-4">
    ... fields ...
    <div class="flex gap-3">
      <button type="button" id="backStep1" class="btn-secondary flex-1">Back</button>
      <button type="submit" class="btn-primary flex-1">Request my options</button>
    </div>
  </div>
</form>

<div id="confirmation" class="hidden text-center py-6">
  ...
</div>
```

Because `display:none` (what Tailwind's `hidden` class sets) cannot be transitioned, and there's no other motion applied, the step change is an abrupt content swap with nothing communicating "you moved forward" or "you moved back."

## Target

Add a small `.form-step` transition helper to `css/style.css` using `@starting-style` (progressive enhancement — falls back to instant in browsers that don't support it, which is acceptable since it degrades to today's behavior, not a broken one), and rewrite the three JS handlers to toggle a `data-state` attribute plus manage `hidden` on a delay so the transition can play instead of snapping.

```css
/* target: append to css/style.css */
.form-step {
  transition: opacity 200ms cubic-bezier(0.23, 1, 0.32, 1), transform 200ms cubic-bezier(0.23, 1, 0.32, 1);
}
.form-step[data-entering] {
  opacity: 0;
  transform: translateX(12px);
}
.form-step[data-leaving] {
  opacity: 0;
  transform: translateX(-12px);
}

@media (prefers-reduced-motion: reduce) {
  .form-step { transition: opacity 150ms ease; }
  .form-step[data-entering],
  .form-step[data-leaving] { transform: none; }
}
```

Note the reduced-motion override keeps the opacity fade (aids comprehension of the state change) but drops the horizontal movement, per the audit's accessibility rule ("reduced motion means fewer and gentler animations, not zero").

```js
/* target: contact.html, replacing the three handlers at lines 133-150 */
function swapStep(hideEl, showEl, direction) {
  // direction: 1 = forward (step1 -> step2), -1 = backward (step2 -> step1)
  hideEl.setAttribute("data-leaving", "");
  hideEl.style.transform = `translateX(${direction * -12}px)`;
  hideEl.style.opacity = "0";
  setTimeout(() => {
    hideEl.classList.add("hidden");
    hideEl.removeAttribute("data-leaving");
    hideEl.style.transform = "";
    hideEl.style.opacity = "";

    showEl.classList.remove("hidden");
    showEl.style.transform = `translateX(${direction * 12}px)`;
    showEl.style.opacity = "0";
    // force reflow so the browser registers the starting position before transitioning
    showEl.offsetHeight;
    showEl.style.transition = "opacity 200ms cubic-bezier(0.23, 1, 0.32, 1), transform 200ms cubic-bezier(0.23, 1, 0.32, 1)";
    showEl.style.transform = "translateX(0)";
    showEl.style.opacity = "1";
  }, 200);
}

document.getElementById("toStep2").addEventListener("click", () => {
  swapStep(document.getElementById("step1"), document.getElementById("step2"), 1);
  document.getElementById("stepDot1").className = "";
  document.getElementById("stepDot2").className = "text-teal";
});
document.getElementById("backStep1").addEventListener("click", () => {
  swapStep(document.getElementById("step2"), document.getElementById("step1"), -1);
  document.getElementById("stepDot1").className = "text-teal";
  document.getElementById("stepDot2").className = "";
});
document.getElementById("quoteForm").addEventListener("submit", (e) => {
  e.preventDefault();
  swapStep(document.getElementById("quoteForm"), document.getElementById("confirmation"), 1);
  document.getElementById("refNum").textContent = "#PYR-" + Math.floor(100000 + Math.random()*900000);
});
```

This uses inline `style` transitions driven by JS rather than the `.form-step`/`data-entering`/`data-leaving` CSS shown above, because this codebase has no build step or framework to reliably coordinate class-toggle timing with `@starting-style` browser support — inline styles with a `setTimeout` matched to the transition duration is the simplest approach that works in plain vanilla JS without a dependency. **If the executor prefers the `@starting-style` CSS approach instead of inline styles, that is acceptable** as long as the visual result matches (200ms slide + fade, direction-aware, reduced-motion fallback) — but do not ship both approaches at once; pick one.

## Repo conventions to follow

- This site has no animation library or CSS framework beyond Tailwind utilities + hand-written `css/style.css` — motion is done with plain CSS transitions and vanilla JS class/style toggles throughout (see `js/layout.js`'s mobile menu, or the yacht gallery thumbnail swap in `build_pages.py`). Stay consistent with that: no new dependency, no framework.
- Respect `prefers-reduced-motion` — this repo already has one correct example to imitate: `css/style.css:154-156` (the marquee's reduced-motion override, `@media (prefers-reduced-motion: reduce) { .marquee-track { animation: none; } }`). Follow the same pattern (media query directly in `css/style.css`), not a JS-based `matchMedia` check, to stay consistent with the existing code.
- Use `cubic-bezier(0.23, 1, 0.32, 1)` for this ease-out curve — the same curve introduced in plan 001/003 for button feedback, so the whole site converges on one strong ease-out curve rather than several near-identical ones (audit's cohesion category).

## Steps

1. Add the `.form-step` CSS block (or your `@starting-style` equivalent, per the note above) to the end of `css/style.css`, including the `prefers-reduced-motion` override.
2. In `contact.html`, replace the three event listener blocks currently at lines 133-150 with the `swapStep()` helper function and its three call sites, as shown in Target above. Keep the `stepDot1`/`stepDot2` className toggling logic exactly as it is today (unrelated to this fix) — only the hide/show mechanism changes.
3. Rebuild the compiled Tailwind stylesheet: run `./node_modules/.bin/tailwindcss -i ./css/tailwind-input.css -o ./css/tailwind.css --minify` from the project root (harmless if this plan's CSS additions don't use new Tailwind utility classes — run it anyway for consistency, skip only if it errors and report the error).

## Boundaries

- Do NOT change any form field, label, validation, or the `?boat=`/`?experience=`/`?destination=` query-param prefill logic (`contact.html:124-131`) — that logic stays exactly as-is above the handlers you're replacing.
- Do NOT change the reference-number generation logic (`Math.floor(100000 + Math.random()*900000)`) — cosmetic motion only.
- Do NOT add a JS animation library (GSAP, Framer Motion, etc.) — this is a static site with zero dependencies for animation; keep it that way.
- Do NOT change `stepDot1`/`stepDot2` visual logic beyond what's shown — that's a separate, already-working piece of UI (the "Step 1 → Step 2" indicator text color).
- If the current code at any cited line doesn't match what's quoted above (drift since commit `7e915e1`), STOP and report instead of improvising.

## Verification

- **Mechanical**: no build step required for HTML/JS. Open `contact.html` in a browser and confirm no console errors (open DevTools console before interacting). If `node` and `puppeteer-core` are available (they are, per `check_console.js` in the project root), run `node check_console.js` from the project root after the change and confirm it still reports "Total issues: 0".
- **Feel check**: open `http://localhost:8080/contact.html` (start with `python3 -m http.server 8080` from the project root if not running).
  - Fill in step 1 (any values) and click "Continue". Confirm step 1 slides/fades out to the left while step 2 slides/fades in from the right — not an instant swap.
  - Click "Back" on step 2. Confirm the reverse: step 2 exits toward the right, step 1 re-enters from the left.
  - Fill in step 2 completely (all required fields) and click "Request my options". Confirm the form transitions out and the confirmation message transitions in, with the same fade/slide treatment.
  - In Chrome DevTools Animations panel, set playback to 10% during a step change and confirm the slide+fade plays smoothly over ~200ms in each direction — not two separate uncoordinated animations that overlap awkwardly.
  - Toggle `prefers-reduced-motion: reduce` in DevTools' Rendering panel, repeat all three transitions, and confirm they still fade (opacity) but no longer slide horizontally.
  - Rapidly click "Continue" then immediately "Back" (before the first transition finishes) and confirm the UI doesn't end up in a broken state (e.g. both steps visible at once, or neither visible) — if this happens, the `setTimeout`-based approach needs a guard (e.g. disable the buttons during the ~200ms transition window) — add one if you observe this failure.
- **Done when**: all three state changes (step1→step2, step2→step1, form→confirmation) animate with a direction-aware slide+fade instead of an instant snap, reduced-motion users still get a fade without movement, and rapid double-clicking the step buttons doesn't leave the form in a visually broken state.
