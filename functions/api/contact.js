// Lead capture for the homepage form. The browser never learns where a lead
// lands, and a bot post dies at the edge.

const CAPTURE_URL = "https://phail.ai/api/interest";
const MAX_BODY = 16 * 1024;
const UTM_TAGS = ["utm_source", "utm_medium", "utm_campaign", "utm_term", "utm_content"];

const text = (value, max) => (typeof value === "string" ? value.trim().slice(0, max) : "");

// The page that sent the form, and the UTM tags in its address, as the request's Referer names them.
function formPage(request) {
  const tags = { page: "" };
  for (const tag of UTM_TAGS) tags[tag] = "";
  let url;
  try {
    url = new URL(request.headers.get("referer") || "");
  } catch {
    return tags;
  }
  tags.page = url.pathname;
  for (const tag of UTM_TAGS) tags[tag] = (url.searchParams.get(tag) || "").slice(0, 200);
  return tags;
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
    heard_from: text(data.heard_from, 64),
    heard_from_detail: text(data.heard_from_detail, 200),
    referrer: text(data.referrer, 500),
    ...formPage(request),
  };

  const upstream = await fetch(CAPTURE_URL, {
    method: "POST",
    headers: { "content-type": "application/json" },
    body: JSON.stringify(lead),
  });
  if (!upstream.ok) return json({ error: "Could not record that" }, 502);
  return json({ ok: true });
}

export const onRequest = () => json({ error: "Method not allowed" }, 405);
