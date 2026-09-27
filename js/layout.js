// Shared header/footer + sticky mobile action bar, injected on every page.
function siteHeader(active) {
  const link = (href, label, key) =>
    `<a href="${href}" class="nav-link ${active === key ? "text-teal font-semibold" : ""}">${label}</a>`;
  return `
  <header class="sticky top-0 z-40 bg-cream/95 backdrop-blur border-b border-navy/10">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 flex items-center justify-between h-16">
      <a href="/index.html" class="font-serif text-xl text-navy tracking-tight">Pattaya <span class="text-coral">Yacht</span> Rentals</a>
      <nav class="hidden md:flex items-center gap-6 text-sm text-navy/80">
        ${link("/yachts.html", "Yachts", "yachts")}
        ${link("/experiences/index.html", "Experiences", "experiences")}
        ${link("/destinations/index.html", "Destinations", "destinations")}
        ${link("/prices.html", "Prices & Planning", "prices")}
        ${link("/about.html", "About", "about")}
        ${link("/contact.html", "Contact", "contact")}
      </nav>
      <div class="hidden md:block">
        <a href="/yachts.html" class="btn-primary">Find my yacht</a>
      </div>
      <button id="menuBtn" class="md:hidden text-navy" aria-label="Open menu">
        <svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M4 6h16M4 12h16M4 18h16"/></svg>
      </button>
    </div>
    <div id="mobileMenu" class="hidden md:hidden border-t border-navy/10 bg-cream px-4 py-4 space-y-3 text-navy/90">
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
  </header>`;
}

function siteFooter() {
  return `
  <footer class="bg-navy text-cream mt-24">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-14 grid gap-10 sm:grid-cols-2 lg:grid-cols-4">
      <div>
        <p class="font-serif text-lg mb-3">Pattaya Yacht Rentals</p>
        <p class="text-sm text-cream/70">Private day charters around Pattaya, planned around your group. Enquiries confirmed by our team before booking.</p>
      </div>
      <div>
        <p class="text-sm font-semibold uppercase tracking-wide text-coral mb-3">Explore</p>
        <ul class="space-y-2 text-sm text-cream/80">
          <li><a href="/yachts.html" class="hover:text-white">All yachts</a></li>
          <li><a href="/experiences/index.html" class="hover:text-white">Experiences</a></li>
          <li><a href="/destinations/index.html" class="hover:text-white">Destinations</a></li>
          <li><a href="/prices.html" class="hover:text-white">Prices & planning</a></li>
        </ul>
      </div>
      <div>
        <p class="text-sm font-semibold uppercase tracking-wide text-coral mb-3">Company</p>
        <ul class="space-y-2 text-sm text-cream/80">
          <li><a href="/about.html" class="hover:text-white">About</a></li>
          <li><a href="/faq.html" class="hover:text-white">FAQ</a></li>
          <li><a href="/booking-terms.html" class="hover:text-white">Booking terms</a></li>
          <li><a href="/privacy-policy.html" class="hover:text-white">Privacy policy</a></li>
        </ul>
      </div>
      <div>
        <p class="text-sm font-semibold uppercase tracking-wide text-coral mb-3">Contact</p>
        <ul class="space-y-2 text-sm text-cream/80">
          <li><a href="https://wa.me/66653159096" target="_blank" rel="noopener" class="hover:text-white">WhatsApp: +66 65 315 9096</a></li>
          <li><a href="tel:+66653159096" class="hover:text-white">Call: +66 65 315 9096</a></li>
          <li><a href="mailto:info@yacht-charters-phuket.com" class="hover:text-white">Email: info@yacht-charters-phuket.com</a></li>
          <li>Ao Po Grand Marina, Phuket 83110</li>
        </ul>
      </div>
    </div>
    <div class="border-t border-cream/10 py-5 text-center text-xs text-cream/50">
      &copy; 2026 Pattaya Yacht Rentals. Rates and availability are confirmed by our team before booking.
    </div>
  </footer>
  <div class="fixed bottom-0 inset-x-0 z-40 md:hidden bg-navy/95 backdrop-blur border-t border-cream/10 flex">
    <a href="https://wa.me/66653159096" target="_blank" rel="noopener" class="flex-1 text-center py-3 text-cream font-semibold text-sm border-r border-cream/10">WhatsApp</a>
    <a href="/contact.html" class="flex-1 text-center py-3 text-coral font-semibold text-sm">Get a quote</a>
  </div>
  <div class="h-14 md:hidden"></div>`;
}

function mountLayout(active) {
  document.getElementById("site-header").innerHTML = siteHeader(active);
  document.getElementById("site-footer").innerHTML = siteFooter();
  const menuBtn = document.getElementById("menuBtn");
  const mobileMenu = document.getElementById("mobileMenu");
  menuBtn.addEventListener("click", () => mobileMenu.classList.toggle("hidden"));
}
