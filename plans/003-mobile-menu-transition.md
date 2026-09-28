# 003 — Animate the mobile hamburger menu open/close

- **Status**: DONE
- **Commit**: 7e915e1
- **Severity**: HIGH
- **Category**: Missed opportunity / state teleport (audit category 8)
- **Estimated scope**: 2 files (`js/layout.js`, `css/style.css`)

## Problem

`js/layout.js` renders the mobile navigation drop-down and its toggle button. Opening/closing it is a single `classList.toggle("hidden")` call — an instant `display:none ↔ display:block` snap with zero transition. This is the first interactive element most mobile visitors touch on the site (every page has a sticky header with this hamburger button below the `md` breakpoint), so an instant, jarring open feels cheap on a "dark-luxury" branded site that is otherwise carefully designed.

Current code, `js/layout.js:47-51` (header markup):

```html
<button id="menuBtn" class="md:hidden text-navy" aria-label="Open menu">
  <svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M4 6h16M4 12h16M4 18h16"/></svg>
</button>
</div>
<div id="mobileMenu" class="hidden md:hidden border-t border-navy/10 bg-cream px-4 py-4 space-y-3 text-navy/90">
```

Current code, `js/layout.js:123-125` (`mountLayout` function):

```js
const menuBtn = document.getElementById("menuBtn");
const mobileMenu = document.getElementById("mobileMenu");
menuBtn.addEventListener("click", () => mobileMenu.classList.toggle("hidden"));
```

## Target

**Note: this section reflects the actual final code after execution surfaced two issues with the originally-written target (see `plans/README.md` "Execution notes" for what went wrong and why). The code below is correct and verified; an earlier draft of this plan specified an unscoped `#mobileMenu { display: grid }` rule and single-level padding, both of which had real bugs.**

Replace the `hidden` class toggle with a height+opacity transition driven by a `data-open` attribute, plus a CSS rule that animates `grid-template-rows` (the standard technique for animating to/from an unknown content height without hardcoding pixel values — the audit explicitly calls out `translate` percentages and similar unknown-size-safe techniques over hardcoded pixel offsets).

The grid/transition rule must be scoped inside `@media (max-width: 767.98px)` — an unscoped `#mobileMenu { display: grid }` is an ID selector and will always beat Tailwind's `.md:hidden { display: none }` class selector regardless of source order, breaking desktop. Padding must live two levels deep (not on the direct grid item) — `overflow:hidden` only clips a box's overflowing *content*, not its own padding, so a padded grid item can never fully collapse to 0 even with `min-height:0`.

```css
/* target: append to css/style.css */
@media (max-width: 767.98px) {
  #mobileMenu {
    display: grid;
    grid-template-rows: 0fr;
    transition: grid-template-rows 200ms cubic-bezier(0.23, 1, 0.32, 1);
  }
  #mobileMenu[data-open] {
    grid-template-rows: 1fr;
  }
}
#mobileMenu > .mobile-menu-inner {
  overflow: hidden;
  min-height: 0;
}

@media (prefers-reduced-motion: reduce) {
  #mobileMenu { transition: none; }
}
```

```html
<!-- target: js/layout.js header markup, replacing the mobileMenu div's opening tag -->
<div id="mobileMenu" class="md:hidden border-t border-navy/10 bg-cream">
  <div class="mobile-menu-inner">
    <div class="px-4 py-4 space-y-3 text-navy/90">
      ${link("/yachts.html", "Yachts", "yachts")}
      <div class="block"></div>
      ${link("/experiences/index.html", "Experiences", "experiences")}
      <div class="block"></div>
      ${link("/destinations/index.html", "Destinations", "destinations")}
      <div class="block"></div>
      ${link("/prices.html", "Prices & Planning", "prices")}
      <div class="block"></div>
      ${link("/about.html", "About", "about")}
      <div class="block"></div>
      ${link("/faq.html", "FAQ", "faq")}
      <div class="block"></div>
      ${link("/contact.html", "Contact", "contact")}
    </div>
  </div>
</div>
```

Note: `.mobile-menu-inner` (the direct grid item) carries no padding of its own — padding moved to the innermost wrapper div so the grid item itself has zero intrinsic size and can fully collapse. The `hidden` class is removed from `#mobileMenu`'s initial markup — the closed state is now expressed entirely by `grid-template-rows: 0fr`. `md:hidden` is untouched and still correctly hides the whole mobile menu on desktop widths regardless of open/closed state, since the grid rule no longer competes with it outside the mobile media query.

```js
/* target: js/layout.js mountLayout(), replacing lines 123-125 */
const menuBtn = document.getElementById("menuBtn");
const mobileMenu = document.getElementById("mobileMenu");
menuBtn.addEventListener("click", () => {
  const isOpen = mobileMenu.hasAttribute("data-open");
  if (isOpen) {
    mobileMenu.removeAttribute("data-open");
  } else {
    mobileMenu.setAttribute("data-open", "");
  }
  menuBtn.setAttribute("aria-expanded", String(!isOpen));
});
```

Also update the button's initial markup to include `aria-expanded="false"` for accessibility (it currently has none):

```html
<!-- target: js/layout.js, menuBtn button tag -->
<button id="menuBtn" class="md:hidden text-navy" aria-label="Open menu" aria-expanded="false">
```

## Repo conventions to follow

- Motion in this codebase lives in plain CSS in `css/style.css`, appended as new rule blocks at the end of the file (see how `.hero-full`, `.marquee`, `.dark-card` were each added as a new block) — follow that placement convention, don't scatter the new rule elsewhere.
- Reduced-motion handling: this repo's one existing example is `css/style.css`'s marquee rule (`@media (prefers-reduced-motion: reduce) { .marquee-track { animation: none; } }`) — follow the same direct-media-query-in-CSS pattern shown in Target above, not a JS `matchMedia` branch.
- Use `cubic-bezier(0.23, 1, 0.32, 1)` as the ease-out curve, matching plans 001/002 — the goal across all three plans is to converge the whole site on one strong ease-out curve instead of bare `ease`.

## Steps

1. In `js/layout.js`, find the `siteHeader()` function's returned template string. Locate the `<div id="mobileMenu" class="hidden md:hidden border-t border-navy/10 bg-cream px-4 py-4 space-y-3 text-navy/90">` opening tag (currently line 51) and the matching closing `</div>` (currently line 38, immediately before `</header>`).
2. Change that div's class from `"hidden md:hidden border-t border-navy/10 bg-cream px-4 py-4 space-y-3 text-navy/90"` to `"md:hidden border-t border-navy/10 bg-cream"` (drop `hidden`, drop the padding/spacing/text-color utilities — those move to the new inner wrapper).
3. Wrap the six `${link(...)}` calls and their five `<div class="block"></div>` separators in a new `<div class="mobile-menu-inner px-4 py-4 space-y-3 text-navy/90">...</div>` — i.e. add that opening div immediately after the `#mobileMenu` opening tag, and its closing `</div>` immediately before `#mobileMenu`'s own closing `</div>`.
4. In `js/layout.js`, find the `menuBtn` button tag (currently line 47: `<button id="menuBtn" class="md:hidden text-navy" aria-label="Open menu">`) and add `aria-expanded="false"` to it.
5. In `css/style.css`, append the `#mobileMenu` / `#mobileMenu > .mobile-menu-inner` / `#mobileMenu[data-open]` rule block (including the `prefers-reduced-motion` override) shown in Target, to the end of the file.
6. In `js/layout.js`'s `mountLayout()` function, replace the single-line `menuBtn.addEventListener("click", () => mobileMenu.classList.toggle("hidden"));` (currently line 125) with the `data-open`/`aria-expanded` toggle logic shown in Target.
7. Rebuild the compiled Tailwind stylesheet: run `./node_modules/.bin/tailwindcss -i ./css/tailwind-input.css -o ./css/tailwind.css --minify` from the project root, since step 2 removes Tailwind utility classes (`px-4 py-4 space-y-3 text-navy/90`) from one element and adds them to another — the compiled CSS output doesn't need to change since the same utility classes are still used somewhere in the scanned content, but rebuild anyway for consistency and to catch any issue immediately.

## Boundaries

- Do NOT change any of the six nav links' hrefs, labels, or the `link()` helper function itself — only the wrapping markup around them.
- Do NOT change `siteFooter()` or any other function in `js/layout.js` — scope is `siteHeader()` and `mountLayout()` only.
- Do NOT change desktop nav behavior — `md:hidden` must continue to fully hide this menu (open or closed) at the `md` breakpoint and above; verify this explicitly in the feel check below.
- Do NOT add a JS animation library — this is a CSS `grid-template-rows` transition plus a plain attribute toggle, no dependencies.
- If the current code at any cited line doesn't match what's quoted above (drift since commit `7e915e1`), STOP and report instead of improvising.

## Verification

- **Mechanical**: run `node check_console.js` from the project root after the change (requires the local server running: `python3 -m http.server 8080` in a separate terminal first) and confirm it still reports "Total issues: 0" across all checked pages — this catches any JS syntax error or broken selector introduced by the rewrite.
- **Feel check**: open `http://localhost:8080/index.html` in a browser resized to mobile width (or Chrome's device toolbar, e.g. 375px wide).
  - Click the hamburger icon. Confirm the menu smoothly expands open over ~200ms (grows from zero height) rather than snapping into view instantly.
  - Click it again. Confirm it smoothly collapses shut over ~200ms rather than disappearing instantly.
  - In DevTools Animations panel, set playback to 10% during an open, and confirm the six nav links reveal smoothly as the container grows, without any content jumping or overflowing visibly before the container has expanded to fit it.
  - Resize the viewport to desktop width (≥768px / the `md` breakpoint) with the menu left open, and confirm the mobile menu is still fully hidden (this must not regress — `md:hidden` needs to keep working regardless of the new `data-open` attribute).
  - Toggle `prefers-reduced-motion: reduce` in DevTools' Rendering panel and confirm the menu now opens/closes instantly (no transition) rather than animating — this is one of the few cases where full removal (not just dropping movement) is acceptable, since the "movement" here (height growth) is the entire visual, not a decorative addition to an otherwise-fading element.
  - Tab to the hamburger button with the keyboard and press Enter/Space to confirm it still opens the menu (keyboard accessibility unaffected by the attribute-based rewrite).
- **Done when**: the mobile menu opens and closes with a smooth ~200ms height transition instead of an instant snap, desktop `md:hidden` behavior is unchanged, reduced-motion users get an instant (not animated) toggle, and `check_console.js` reports zero issues.
