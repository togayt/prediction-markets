import type { APIRoute } from "astro";
import { SITE_URL } from "../config";

// Add new pages here as you create them.
const routes = [
  "/",
  "/what-is-a-prediction-market",
  "/compare",
  "/guides/how-to-use-kalshi",
  "/guides/affiliate-programs-explained",
  "/about",
  "/how-we-make-money",
];

export const GET: APIRoute = () => {
  const today = new Date().toISOString().split("T")[0];
  const urls = routes
    .map(
      (r) =>
        `  <url><loc>${new URL(r, SITE_URL).href}</loc><lastmod>${today}</lastmod></url>`
    )
    .join("\n");

  const xml = `<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
${urls}
</urlset>`;

  return new Response(xml, {
    headers: { "Content-Type": "application/xml" },
  });
};
