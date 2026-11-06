// Lead capture for the homepage form. The browser never learns where a lead
// lands, and a bot post dies at the edge.

const CAPTURE_URL = "https://phail.ai/api/interest";
const MAX_BODY = 16 * 1024;
// The first and the last arrival of the visitor, as theme/positronic/static/js/attribution.js names them.
const TOUCH_FIELDS = ["utm_source", "utm_medium", "utm_campaign", "utm_content", "utm_term", "referrer", "landing_page", "at"];
const ARRIVAL_FIELDS = ["first", "last"].flatMap((which) => TOUCH_FIELDS.map((field) => `${which}_${field}`));

const text = (value, max) => (typeof value === "string" ? value.trim().slice(0, max) : "");
// The ticked answers to "How did you hear about us?"; phail.ai checks each one against its list.
const MAX_HEARD_FROM = 7;
const texts = (value, max) => (Array.isArray(value) ? value.map((item) => text(item, max)).filter(Boolean).slice(0, MAX_HEARD_FROM) : []);

// The path of the page that sent the form, as the request's Referer names it.
function refererPage(request) {
  try {
    return new URL(request.headers.get("referer") || "").pathname;
  } catch {
    return "";
  }
}

const json = (body, status = 200) =>
  new Response(JSON.stringify(body), {
    status,
    headers: { "content-type": "application/json" },
  });

export async function onRequestPost({ request }) {
  const raw = await request.text();
  if (raw.length > MAX_BODY) return json({ error: "Request too large" }, 413);

  let data;
  try {
    data = JSON.parse(raw || "{}");
  } catch {
    return json({ error: "Invalid JSON" }, 400);
  }

  // The hidden field is filled by bots only. Answer them as if it worked.
  if ((data.company || "").trim()) return json({ ok: true });

  const email = (data.email || "").trim();
  if (!email.includes("@") || !email.includes(".") || email.length > 320) {
    return json({ error: "A valid email is required" }, 400);
  }

  const lead = {
    email,
    note: text(data.note, 2000),
    source: "positronic-home",
    heard_from: texts(data.heard_from, 64),
    heard_from_detail: text(data.heard_from_detail, 200),
    page: refererPage(request),
  };
  for (const field of ARRIVAL_FIELDS) lead[field] = text(data[field], field.endsWith("referrer") ? 500 : 200);

  const upstream = await fetch(CAPTURE_URL, {
    method: "POST",
    headers: { "content-type": "application/json" },
    body: JSON.stringify(lead),
  });
  if (!upstream.ok) return json({ error: "Could not record that" }, 502);
  return json({ ok: true });
}

export const onRequest = () => json({ error: "Method not allowed" }, 405);
