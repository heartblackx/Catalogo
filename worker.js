const SUPABASE_REST = "https://cisiancuphdkybkddwmq.supabase.co/rest/v1/web_analytics_events";
const SUPABASE_ANON_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImNpc2lhbmN1cGhka3lia2Rkd21xIiwicm9sZSI6ImFub24iLCJpYXQiOjE3ODc2MDU0NjcsImV4cCI6MjEwMzE4MTQ2N30.Mvn7MCGYGuSAE3PfTV312AvRfV1wEJjnvZglrEw9Ozg";

const BOT_RE = /bot|crawler|spider|slurp|bingpreview|facebookexternalhit|whatsapp|telegrambot|discordbot|headless|preview|monitor|uptime/i;

function clip(value, max = 200) {
  if (value == null) return null;
  return String(value).slice(0, max);
}

function cookieValue(request, name) {
  const raw = request.headers.get("cookie") || "";
  const parts = raw.split(";");
  for (const part of parts) {
    const [key, ...rest] = part.trim().split("=");
    if (key === name) return decodeURIComponent(rest.join("="));
  }
  return null;
}

function deviceFromUA(ua) {
  if (/ipad|tablet|kindle|silk/i.test(ua)) return "tablet";
  if (/mobi|android|iphone|ipod/i.test(ua)) return "mobile";
  return "desktop";
}

function referrerHost(request) {
  const raw = request.headers.get("referer") || "";
  if (!raw) return null;
  try { return new URL(raw).hostname.toLowerCase(); } catch { return null; }
}

function classifySource(url, refHost) {
  const utm = (url.searchParams.get("utm_source") || "").trim().toLowerCase();
  if (utm) return clip(utm, 80);
  if (!refHost) return "direct";
  if (refHost === url.hostname.toLowerCase()) return "internal";
  if (/(^|\.)facebook\.com$|(^|\.)fb\.com$|(^|\.)messenger\.com$/.test(refHost)) return "facebook";
  if (/(^|\.)instagram\.com$/.test(refHost)) return "instagram";
  if (/(^|\.)tiktok\.com$/.test(refHost)) return "tiktok";
  if (/(^|\.)youtube\.com$|(^|\.)youtu\.be$/.test(refHost)) return "youtube";
  if (/(^|\.)google\./.test(refHost)) return "google";
  if (/(^|\.)bing\.com$/.test(refHost)) return "bing";
  if (/(^|\.)duckduckgo\.com$/.test(refHost)) return "duckduckgo";
  if (/(^|\.)yahoo\./.test(refHost)) return "yahoo";
  return "referral";
}

async function recordPageView(request, visitorId, sessionId, isBot) {
  try {
    const url = new URL(request.url);
    const ua = request.headers.get("user-agent") || "";
    const refHost = referrerHost(request);
    const cf = request.cf || {};
    const lang = (request.headers.get("accept-language") || "").split(",")[0].trim();

    const event = {
      event_type: "page_view",
      visitor_id: isBot ? null : visitorId,
      session_id: isBot ? null : sessionId,
      host: clip(url.hostname.toLowerCase(), 255),
      path: clip(url.pathname || "/", 1000),
      referrer_host: clip(refHost, 255),
      source: classifySource(url, refHost),
      utm_source: clip(url.searchParams.get("utm_source"), 120),
      utm_medium: clip(url.searchParams.get("utm_medium"), 120),
      utm_campaign: clip(url.searchParams.get("utm_campaign"), 200),
      utm_content: clip(url.searchParams.get("utm_content"), 200),
      utm_term: clip(url.searchParams.get("utm_term"), 200),
      country: clip(cf.country, 80),
      region: clip(cf.region, 120),
      city: clip(cf.city, 120),
      device: deviceFromUA(ua),
      language: clip(lang, 40),
      is_bot: isBot,
      metadata: {
        colo: clip(cf.colo, 20),
        timezone: clip(cf.timezone, 80)
      }
    };

    await fetch(SUPABASE_REST, {
      method: "POST",
      headers: {
        "apikey": SUPABASE_ANON_KEY,
        "Authorization": `Bearer ${SUPABASE_ANON_KEY}`,
        "Content-Type": "application/json",
        "Prefer": "return=minimal"
      },
      body: JSON.stringify(event)
    });
  } catch (_) {
    // Analytics must never interfere with the catalog experience.
  }
}

export default {
  async fetch(request, env, ctx) {
    const response = await env.ASSETS.fetch(request);

    const methodOk = request.method === "GET";
    const destination = request.headers.get("sec-fetch-dest") || "";
    const acceptsHtml = (request.headers.get("accept") || "").includes("text/html");
    const contentType = response.headers.get("content-type") || "";
    const isDocument = destination === "document" || acceptsHtml;
    const isHtml = contentType.includes("text/html");

    if (!methodOk || !isDocument || !isHtml || response.status >= 400) {
      return response;
    }

    const ua = request.headers.get("user-agent") || "";
    const isBot = BOT_RE.test(ua);
    let visitorId = cookieValue(request, "ii_vid");
    let sessionId = cookieValue(request, "ii_sid");

    if (!isBot) {
      if (!visitorId) visitorId = crypto.randomUUID();
      if (!sessionId) sessionId = crypto.randomUUID();
    }

    ctx.waitUntil(recordPageView(request, visitorId, sessionId, isBot));

    if (isBot) return response;

    const headers = new Headers(response.headers);
    headers.append("Set-Cookie", `ii_vid=${encodeURIComponent(visitorId)}; Max-Age=31536000; Path=/; HttpOnly; Secure; SameSite=Lax`);
    headers.append("Set-Cookie", `ii_sid=${encodeURIComponent(sessionId)}; Max-Age=1800; Path=/; HttpOnly; Secure; SameSite=Lax`);

    return new Response(response.body, {
      status: response.status,
      statusText: response.statusText,
      headers
    });
  }
};
