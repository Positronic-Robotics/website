// The "Keep in touch" form in the footer. phail.ai's server holds the one updates list of both sites and its Resend
// key, so the browser never learns either.

const SUBSCRIBE_URL = "https://phail.ai/api/subscribe";
const MAX_BODY = 4 * 1024;

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
  if (!data || typeof data !== "object" || Array.isArray(data)) return json({ error: "Invalid JSON" }, 400);

  // The hidden field is filled by bots only. Answer them as if it worked.
  if (typeof data.company === "string" && data.company.trim()) return json({ ok: true });

  const email = typeof data.email === "string" ? data.email.trim() : "";
  if (!email.includes("@") || !email.includes(".") || email.length > 320) {
    return json({ error: "A valid email is required" }, 400);
  }

  const upstream = await fetch(SUBSCRIBE_URL, {
    method: "POST",
    headers: { "content-type": "application/json" },
    body: JSON.stringify({ email }),
  });
  if (!upstream.ok) return json({ error: "Could not record that" }, upstream.status === 429 ? 429 : 502);
  return json({ ok: true });
}

export const onRequest = () => json({ error: "Method not allowed" }, 405);
