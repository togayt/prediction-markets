/**
 * Daily check: Has the UK changed ILR qualifying period from 5 to 10 years?
 *
 * Fetches the official gov.uk settlement guidance page and looks for any
 * mention of a 10-year qualifying period replacing the standard 5-year rule.
 * Exits with code 1 and prints a summary if a potential change is detected,
 * so the GitHub Actions workflow can open an issue automatically.
 */

const SOURCES = [
  {
    label: "gov.uk – Indefinite leave to remain (overview)",
    url: "https://www.gov.uk/indefinite-leave-to-remain",
  },
  {
    label: "gov.uk – Settlement: long residence",
    url: "https://www.gov.uk/long-residence",
  },
  {
    label: "gov.uk – Skilled Worker visa: settlement",
    url: "https://www.gov.uk/skilled-worker-visa/settlement",
  },
];

// Phrases that suggest the 10-year change has been enacted or officially announced
const CHANGE_SIGNALS = [
  /10[\s-]year.{0,60}(qualifying|settlement|ilr|indefinite leave)/gi,
  /qualifying period.{0,30}10 years/gi,
  /settlement.{0,40}10[\s-]year/gi,
  /indefinite leave.{0,40}10[\s-]year/gi,
  /increased?.{0,30}(5|five).{0,30}(10|ten).{0,20}year/gi,
  /changed?.{0,30}qualifying period/gi,
];

// Phrases that confirm the existing 5-year rule (baseline — expected)
const BASELINE_SIGNALS = [
  /5[\s-]year.{0,60}(qualifying|settlement|ilr|indefinite leave)/gi,
  /qualifying period.{0,30}5 years/gi,
  /settlement.{0,40}5[\s-]year/gi,
];

async function fetchText(url) {
  const res = await fetch(url, {
    headers: { "User-Agent": "prediction-markets-monitor/1.0 (policy-change-check)" },
    signal: AbortSignal.timeout(15_000),
  });
  if (!res.ok) throw new Error(`HTTP ${res.status} for ${url}`);
  return res.text();
}

function stripHtml(html) {
  return html
    .replace(/<script[\s\S]*?<\/script>/gi, " ")
    .replace(/<style[\s\S]*?<\/style>/gi, " ")
    .replace(/<[^>]+>/g, " ")
    .replace(/\s+/g, " ")
    .trim();
}

function findMatches(text, patterns) {
  const hits = [];
  for (const pattern of patterns) {
    const re = new RegExp(pattern.source, pattern.flags);
    let m;
    while ((m = re.exec(text)) !== null) {
      hits.push(m[0].slice(0, 120));
    }
  }
  return hits;
}

async function checkSource({ label, url }) {
  let html;
  try {
    html = await fetchText(url);
  } catch (err) {
    return { label, url, error: err.message, changeSignals: [], baselineSignals: [] };
  }
  const text = stripHtml(html);
  return {
    label,
    url,
    error: null,
    changeSignals: findMatches(text, CHANGE_SIGNALS),
    baselineSignals: findMatches(text, BASELINE_SIGNALS),
  };
}

async function main() {
  console.log(`\n=== UK ILR Qualifying Period Monitor ===`);
  console.log(`Run date: ${new Date().toISOString()}\n`);

  const results = await Promise.all(SOURCES.map(checkSource));

  let changeDetected = false;
  const report = [];

  for (const r of results) {
    report.push(`## ${r.label}`);
    report.push(`URL: ${r.url}`);

    if (r.error) {
      report.push(`ERROR: ${r.error}`);
      report.push("");
      continue;
    }

    if (r.changeSignals.length > 0) {
      changeDetected = true;
      report.push(`⚠️  CHANGE SIGNALS FOUND (${r.changeSignals.length}):`);
      r.changeSignals.forEach(s => report.push(`  - "${s}"`));
    } else {
      report.push(`✅ No 10-year change signals found.`);
    }

    if (r.baselineSignals.length > 0) {
      report.push(`📋 Baseline (5-year) signals still present (${r.baselineSignals.length}):`);
      r.baselineSignals.slice(0, 3).forEach(s => report.push(`  - "${s}"`));
    } else {
      report.push(`❓ No 5-year baseline signals found — page content may have changed significantly.`);
      // Absence of the 5-year baseline is itself a weak change signal
      changeDetected = true;
    }

    report.push("");
  }

  const summary = report.join("\n");
  console.log(summary);

  // Write machine-readable output for the workflow step
  const output = {
    runDate: new Date().toISOString(),
    changeDetected,
    sources: results.map(r => ({
      label: r.label,
      url: r.url,
      hasError: !!r.error,
      changeSignals: r.changeSignals.length,
      baselineSignals: r.baselineSignals.length,
    })),
  };

  process.stdout.write(`\n::set-output::${JSON.stringify(output)}\n`);

  if (changeDetected) {
    console.error(
      "\n🚨 POTENTIAL ILR POLICY CHANGE DETECTED — manual review required.\n" +
      "Check the signals above and verify against official gov.uk announcements."
    );
    process.exit(1); // Non-zero exit signals the workflow to open an issue
  } else {
    console.log("\n✅ No ILR qualifying period change detected. Still 5 years as of this run.");
    process.exit(0);
  }
}

main().catch(err => {
  console.error("Unhandled error:", err);
  process.exit(2);
});
