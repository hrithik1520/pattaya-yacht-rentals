// Shared header/footer + floating WhatsApp button, injected on every page.
const WHATSAPP_NUMBER = "919284644226";

// Builds a WhatsApp deep link. On a yacht or destination detail page, the message
// automatically includes that page's name and URL so the chat opens with context.
function buildWhatsAppLink() {
  const path = window.location.pathname;
  const url = window.location.href;
  let message = "Hi! I'd like to enquire about a private yacht charter.";

  const yachtMatch = path.match(/\/yachts\/([^/]+)\/?$/);
  const destMatch = path.match(/\/destinations\/([^/]+)\/?$/);

  if (yachtMatch && typeof getYacht === "function") {
    const y = getYacht(yachtMatch[1]);
    if (y) message = `Hi! I'm interested in the ${y.name} (${y.type}) — ${url}. Could you share current availability and pricing?`;
  } else if (destMatch && typeof getDestination === "function") {
    const d = getDestination(destMatch[1]);
    if (d) message = `Hi! I'd like to plan a charter to ${d.name} — ${url}. Could you suggest a suitable yacht?`;
  }

  return `https://wa.me/${WHATSAPP_NUMBER}?text=${encodeURIComponent(message)}`;
}

function whatsAppIconSvg() {
  return `<svg width="28" height="28" viewBox="0 0 32 32" fill="currentColor" aria-hidden="true"><path d="M16.004 3C9.377 3 4 8.377 4 15.004c0 2.393.7 4.62 1.902 6.492L4 29l7.69-1.87a11.94 11.94 0 0 0 4.314.8h.001C22.63 27.93 28 22.554 28 15.926 28 9.298 22.63 3.92 16.004 3.92zm0 0"/><path fill="#fff" d="M22.5 19.07c-.35-.176-2.07-1.02-2.39-1.137-.32-.117-.553-.176-.786.176-.233.35-.9 1.137-1.104 1.37-.203.234-.406.263-.756.088-.35-.176-1.48-.545-2.82-1.74-1.043-.93-1.748-2.078-1.953-2.428-.204-.35-.022-.54.154-.714.158-.157.35-.41.525-.615.176-.204.234-.35.35-.585.117-.234.06-.44-.03-.615-.088-.176-.786-1.894-1.078-2.594-.284-.68-.573-.588-.786-.6-.203-.01-.437-.012-.67-.012-.234 0-.615.088-.937.44-.322.35-1.23 1.202-1.23 2.93 0 1.73 1.26 3.4 1.435 3.635.176.234 2.478 3.784 6.005 5.307.84.363 1.494.58 2.005.742.842.267 1.608.23 2.213.14.675-.1 2.07-.845 2.362-1.66.292-.816.292-1.516.204-1.66-.088-.146-.32-.234-.67-.41z"/></svg>`;
}

function siteHeader(active) {
  const link = (href, label, key) =>
    `<a href="${href}" class="nav-link ${active === key ? "text-teal font-semibold" : ""}">${label}</a>`;
  return `
  <header class="sticky top-0 z-40 bg-cream/95 backdrop-blur border-b border-navy/10">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 flex items-center justify-between h-16">
      <a href="/" class="font-serif text-xl text-navy tracking-tight">Pattaya <span class="text-coral">Yacht</span> Rentals</a>
      <nav class="hidden md:flex items-center gap-6 text-sm text-navy/80">
        ${link("/yachts/", "Yachts", "yachts")}
        ${link("/day-charters/", "Day Charters", "day-charters")}
        ${link("/destinations/", "Destinations", "destinations")}
        ${link("/prices/", "Prices & Planning", "prices")}
        ${link("/about/", "About", "about")}
        ${link("/contact/", "Contact", "contact")}
      </nav>
      <div class="hidden md:block">
        <a href="/yachts/" class="btn-primary">Find my yacht</a>
      </div>
      <button id="menuBtn" class="md:hidden text-navy" aria-label="Open menu" aria-expanded="false">
        <svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M4 6h16M4 12h16M4 18h16"/></svg>
      </button>
    </div>
    <div id="mobileMenu" class="md:hidden border-t border-navy/10 bg-cream">
      <div class="mobile-menu-inner">
        <div class="px-4 py-4 space-y-3 text-navy/90">
          ${link("/yachts/", "Yachts", "yachts")}
          <div class="block"></div>
          ${link("/day-charters/", "Day Charters", "day-charters")}
          <div class="block"></div>
          ${link("/destinations/", "Destinations", "destinations")}
          <div class="block"></div>
          ${link("/prices/", "Prices & Planning", "prices")}
          <div class="block"></div>
          ${link("/about/", "About", "about")}
          <div class="block"></div>
          ${link("/faq/", "FAQ", "faq")}
          <div class="block"></div>
          ${link("/contact/", "Contact", "contact")}
        </div>
      </div>
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
          <li><a href="/yachts/" class="hover:text-white">All yachts</a></li>
          <li><a href="/day-charters/" class="hover:text-white">Day Charters</a></li>
          <li><a href="/destinations/" class="hover:text-white">Destinations</a></li>
          <li><a href="/prices/" class="hover:text-white">Prices & planning</a></li>
        </ul>
      </div>
      <div>
        <p class="text-sm font-semibold uppercase tracking-wide text-coral mb-3">Company</p>
        <ul class="space-y-2 text-sm text-cream/80">
          <li><a href="/about/" class="hover:text-white">About</a></li>
          <li><a href="/faq/" class="hover:text-white">FAQ</a></li>
          <li><a href="/booking-terms/" class="hover:text-white">Booking terms</a></li>
          <li><a href="/privacy-policy/" class="hover:text-white">Privacy policy</a></li>
        </ul>
      </div>
      <div>
        <p class="text-sm font-semibold uppercase tracking-wide text-coral mb-3">Contact</p>
        <ul class="space-y-2 text-sm text-cream/80">
          <li><a href="${buildWhatsAppLink()}" target="_blank" rel="noopener" class="hover:text-white">WhatsApp: +91 92846 44226</a></li>
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
  <div id="mobileActionBar" class="fixed bottom-0 inset-x-0 z-40 md:hidden bg-navy/95 backdrop-blur border-t border-cream/10 flex">
    <a href="/contact/" class="flex-1 text-center py-3.5 text-coral font-semibold text-sm">Get a quote</a>
  </div>
  <div class="h-14 md:hidden"></div>
  <a id="floatingWaBtn" target="_blank" rel="noopener" aria-label="Chat with us on WhatsApp"
     class="flex fixed bottom-20 right-4 md:bottom-6 md:right-6 z-40 w-14 h-14 rounded-full items-center justify-center shadow-lg transition hover:scale-105 active:scale-95"
     style="background:#25D366;color:#fff;">
    ${whatsAppIconSvg()}
  </a>`;
}

function mountLayout(active) {
  document.getElementById("site-header").innerHTML = siteHeader(active);
  document.getElementById("site-footer").innerHTML = siteFooter();
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

  document.getElementById("floatingWaBtn").href = buildWhatsAppLink();
}
