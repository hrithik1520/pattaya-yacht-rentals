// Real Phuket destinations served by the operator (yacht-charters-phuket.com), based at Ao Po Grand Marina, Phuket.
const DESTINATIONS = [
  {
    slug: "phi-phi-island",
    name: "Phi Phi Island",
    tagline: "Limestone cliffs, Maya Bay and postcard lagoons.",
    intro: "Phi Phi is the destination most guests ask for first — dramatic limestone cliffs rising straight out of turquoise water, with Maya Bay, Pileh Lagoon and Monkey Beach all within reach on a full-day charter from Phuket.",
    goodFor: "Full-day charters, swimming and snorkeling stops, groups wanting the classic Phuket island day.",
    travelTime: "Around 1.5–2 hours each way by yacht from Ao Po Grand Marina, depending on vessel speed.",
  },
  {
    slug: "phang-nga-bay",
    name: "Phang Nga Bay",
    tagline: "Limestone karsts, sea caves and James Bond Island.",
    intro: "Phang Nga Bay is known for its dramatic limestone karst formations rising from calm, sheltered water — including Khao Phing Kan (James Bond Island) and hidden lagoons reachable by canoe.",
    goodFor: "Calmer water, scenic cruising, families and guests who prefer sheltered bays over open sea.",
    travelTime: "Around 1–1.5 hours each way from Ao Po Grand Marina, on the same side of Phuket as the marina.",
  },
  {
    slug: "koh-hong",
    name: "Koh Hong (Hong Island)",
    tagline: "A hidden lagoon inside a limestone island.",
    intro: "Hong Island means \"room\" in Thai — named for the enclosed lagoon at its center, accessible by canoe or on foot at low tide. Clear water and a quieter setting than the busier islands.",
    goodFor: "A relaxed half or full day, swimming, and a quieter alternative to Phi Phi.",
    travelTime: "Around 1 hour each way from Ao Po Grand Marina.",
  },
  {
    slug: "krabi",
    name: "Krabi",
    tagline: "Railay's cliffs and Krabi's beaches by private boat.",
    intro: "A charter toward Krabi brings you to dramatic cliff scenery around Railay Beach and the coastline near Ao Nang, reachable across open water from Phuket.",
    goodFor: "Longer full-day or overnight charters; groups wanting a change of scenery from the Phuket-side islands.",
    travelTime: "Typically 2+ hours each way depending on vessel and sea conditions — best suited to a full day.",
  },
  {
    slug: "similan-islands",
    name: "Similan Islands",
    tagline: "Some of Thailand's clearest water, for a full-day or overnight trip.",
    intro: "The Similans are a marine national park north of Phuket, known for granite boulder islands and exceptional visibility — a longer-range trip best suited to faster yachts or an overnight charter.",
    goodFor: "Snorkeling and diving-focused groups; overnight or long full-day charters on suitable vessels.",
    travelTime: "Several hours each way — seasonal (typically open November to April) and weather-dependent.",
  },
  {
    slug: "racha-islands",
    name: "Racha Islands",
    tagline: "Close to Phuket, with some of the clearest inshore water.",
    intro: "Racha Yai and Racha Noi sit south of Phuket and are a popular half-day or full-day option for swimming and snorkeling without the longer transit of the Similans.",
    goodFor: "Half-day charters, swimming and snorkeling, groups short on time.",
    travelTime: "Distance depends on departure marina — confirmed per vessel and route.",
  },
  {
    slug: "khai-islands",
    name: "Khai Islands",
    tagline: "Small, sandy islands close to shore.",
    intro: "The Khai Islands (Khai Nai, Khai Nok and Khai Nui) are small sandbar-fringed islands, a straightforward stop for swimming and a shorter charter.",
    goodFor: "Shorter charters and families with children.",
    travelTime: "Confirmed per vessel and departure point.",
  },
  {
    slug: "coral-island",
    name: "Coral Island (Koh Hae)",
    tagline: "A short hop from Phuket with watersports options.",
    intro: "Coral Island sits just off Phuket's southern coast — a quick, easy stop for swimming, snorkeling and optional watersports on a shorter charter.",
    goodFor: "Half-day trips and guests who want an easy, close-to-shore option.",
    travelTime: "One of the shortest crossings from Phuket's southern marinas.",
  },
  {
    slug: "lipe-island",
    name: "Koh Lipe",
    tagline: "A further-range destination for multi-day charters.",
    intro: "Koh Lipe lies well south of Phuket, close to the Malaysian border — realistically a multi-day or overnight charter destination rather than a single-day trip.",
    goodFor: "Extended or overnight charters on suitable long-range vessels.",
    travelTime: "A multi-hour crossing — confirmed per vessel; not a same-day round trip from Phuket.",
  },
];

function getDestinations() { return DESTINATIONS; }
function getDestination(slug) { return DESTINATIONS.find(d => d.slug === slug); }
