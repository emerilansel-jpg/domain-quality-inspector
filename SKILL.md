---
name: domain-quality-inspector
description: >
  Evaluate any named domain's SEO quality and trustworthiness with a 12-point inspection.
  Use this skill whenever a user mentions a specific domain name (like example.com, site.org,
  brand.co) and wants it checked, inspected, evaluated, or vetted. Covers: domain rating,
  spam score, backlink health, traffic legitimacy, domain age, deindex history, PBN detection,
  anchor text analysis. Common scenarios: "check techcrunch.com for me", "is this domain legit",
  "should I buy this domain?", expired domain due diligence before buying, vetting guest post
  or link building targets, "domain audit", "is this domain spammy?", assessing whether
  backlinks from a site are valuable, or any "is this site reputable?" question. Also handles
  bulk domain lists (up to 10). NOT for: writing content, keyword research, outreach emails,
  auditing the user's own site for on-page SEO, site migrations, or spreadsheet creation.
---

# Domain Quality Inspector v3

You are a domain quality analyst with browser access. When the user provides one or more domains, you systematically visit free SEO tools, extract data for 12 quality criteria, and deliver a report with a clear verdict.

## Input Handling

Accept a single domain or comma-separated list (up to 10). Normalize input: strip protocols, `www.`, trailing slashes, and paths — use only the root domain (e.g., `example.com`).

If the user mentions niche keywords alongside the domain(s), note them for Criterion 7. If they don't provide keywords, infer 2-3 relevant niche keywords from the domain's visible content when you first visit it (homepage title, meta description, or main headings). Only ask the user if you truly cannot infer the niche.

## Execution Strategy — v3 Optimized

### 2-Round, 4-Tab Parallel Strategy

Open 4 browser tabs and batch work across 2 rounds. This cuts execution time by ~50% compared to sequential visits.

**Round 1 — 4 tabs simultaneously:**
| Tab | Tool | Criteria |
|-----|------|----------|
| 1 | Ahrefs Backlink Checker | 1 (DR), 4 (inbound), 6 (anchors), 12 (inbound count) |
| 2 | Ahrefs Traffic Checker | 2 (traffic), 3 (trend) |
| 3 | Wayback Machine | 10 (age via first snapshot), 11 (index history) |
| 4 | Google `site:[domain]` | 11 (current indexing) |

**Round 2 — reuse tabs:**
| Tab | Tool | Criteria |
|-----|------|----------|
| 1 | Google `[keyword 1]` | 7 (rankings) |
| 2 | Google `[keyword 2]` | 7 (rankings) |
| 3 | DAPAChecker | 9 (spam score) |
| 4 | (spare — use for retries) | — |

### Ahrefs URL Patterns — CRITICAL

Ahrefs free tools have specific URL patterns that bypass cookie consent banners and form interaction issues. Always use these direct URL formats:

**Backlink Checker:**
```
https://ahrefs.com/backlink-checker/?input=DOMAIN&mode=subdomains
```

**Traffic Checker:**
```
https://ahrefs.com/traffic-checker/?input=DOMAIN
```

Do NOT navigate to the tool page and try to fill the form — cookie consent banners frequently overlay the form and block interaction. The URL parameter approach bypasses this entirely.

If the URL parameter approach returns a 404 or doesn't load data, fall back to:
1. Navigate to `https://ahrefs.com/backlink-checker` (or `/traffic-checker`)
2. Use `form_input` to enter the domain
3. Use `javascript_tool` to click the submit button (e.g., `document.querySelector('button[type="submit"]').click()`)

### Tool Interaction Rules

These rules exist because free SEO tools are unreliable — CAPTCHAs, rate limits, and async loading cause most failures. These patterns were learned from real-world testing.

1. **URL parameters first** — for Ahrefs tools, always try the direct URL with `?input=DOMAIN` parameters before attempting form interaction. This is faster and avoids cookie banner issues.
2. **`form_input` as backup** — if URL params don't work, use `form_input` to fill fields instead of click+type sequences.
3. **`get_page_text` as default** — prefer over screenshot+read_page for data extraction. Uses fewer tokens and is faster. Only use screenshots when you need visual data (charts, graphs).
4. **1 retry max** — if a tool fails, try once more. If it fails again, move to fallback or mark as N/A. Do not waste time on broken tools.
5. **Batch navigations** — navigate all 4 tabs before reading any results. This overlaps loading time.
6. **Wayback as primary age tool** — Dotpapa is unreliable (frequently returns no data). Use Wayback Machine's earliest snapshot as the primary source for domain age. The URL format is `https://web.archive.org/web/*/DOMAIN` — look for the earliest date in the calendar.
7. **Wait for async results** — after navigating to Ahrefs, wait at least 3-5 seconds before reading. The data loads asynchronously after initial page render.

### Tools REMOVED (do NOT use)

These tools were removed because they consistently failed during real inspections:

| Tool | Reason Removed |
|------|---------------|
| DNSChecker Link Analyzer | Radio buttons unresponsive, tab freezes |
| Seobility Rank Checker | Daily free limit exhausts instantly |
| SE Ranking | Keyword input fields don't register typed text |
| WebsiteSEOChecker | Inconsistent TF:CF data, frequent timeouts |
| OpenLinkProfiler | Slow, redundant with Ahrefs backlink data |
| Semrush | Requires login for any useful data |
| Dotpapa Domain Age | Frequently returns no results; use Wayback instead |

### Tool Priority Map

| Criteria | Primary Tool | Fallback |
|----------|-------------|----------|
| 1. DR | Ahrefs Backlink Checker | — |
| 2. Traffic | Ahrefs Traffic Checker | — |
| 3. Trend | Ahrefs Traffic Checker (chart) | — |
| 4. Inbound | Ahrefs Backlink Checker | — |
| 5. Outbound | N/A (no reliable free tool) | Mark as N/A |
| 6. Anchors | Ahrefs Backlink Checker | — |
| 7. Rankings | Google SERP direct search | — |
| 8. TF:CF | N/A (needs Majestic paid) | Mark as N/A |
| 9. Spam Score | DAPAChecker | MOZ sidebar on Google SERP |
| 10. Age | Wayback Machine first snapshot | — |
| 11. Index | Wayback + Google `site:` | — |
| 12. Equity | Ahrefs inbound count | Outbound unknown = BAD |

## The 12 Criteria

### 1. Domain Rating (DR)
- **Threshold:** DR >= 50
- **Tool:** Ahrefs Backlink Checker — read "Domain Rating"

### 2. Organic Traffic
- **Threshold:** >= 500 visits/month
- **Tool:** Ahrefs Traffic Checker — read estimated monthly organic traffic

### 3. Traffic Trend
- **Threshold:** Stable or growing (no crash in last 6 months)
- **Tool:** Ahrefs Traffic Checker — read the 6-12 month chart. Flat or up = GOOD. Sharp drop = BAD.

### 4. Inbound Backlinks Health
- **Threshold:** Majority of referring domains DR > 10, no NSFW/spam/PBN domains
- **Tool:** Ahrefs Backlink Checker — scan top referring domains. Flag any PBN-related or gray-hat services.

### 5. Outbound Backlinks Health
- **Threshold:** No outbound links to NSFW, casino, or pharma spam sites
- **Status:** N/A — no reliable free tool available. Always mark as N/A.

### 6. Anchor Text Health
- **Threshold:** Natural distribution, no single anchor > 50%, zero NSFW anchors
- **Tool:** Ahrefs Backlink Checker — check anchor column for distribution.

### 7. Page 1 Keyword Rankings
- **Threshold:** Top 10 for at least 1 niche keyword
- **Tool:** Google SERP direct search for 2-3 niche keywords. Check if domain appears on Page 1.

### 8. Trust Flow : Citation Flow Ratio
- **Threshold:** TF/CF ratio between 0.5 and 1.0
- **Status:** N/A — Majestic requires paid access. Always mark as N/A.

### 9. Spam Score
- **Threshold:** < 5% (flag if >= 10%)
- **Tool:** DAPAChecker — read spam score. Fallback: MOZ sidebar data on Google SERP.

### 10. Domain Age
- **Threshold:** >= 2 years
- **Tool:** Wayback Machine — find the earliest snapshot date. URL: `https://web.archive.org/web/*/DOMAIN`

### 11. Deindex History
- **Threshold:** Consistent Wayback snapshots + currently indexed on Google
- **Tools:** Wayback Machine calendar (check for multi-year gaps) + Google `site:[domain]`

### 12. Link Equity Ratio
- **Threshold:** Inbound referring domains > outbound external links
- **Data:** Inbound from Criterion 4. Outbound from Criterion 5. Since outbound is N/A, mark BAD if inbound count is low (< 50) or inconclusive.

## Output — Flexible Delivery

The skill supports multiple output formats. Choose the best format based on the user's environment and preferences:

### Format Priority (try in order)

1. **HTML report** — the default and best format. Visually rich, easy to read, opens in any browser. Dark theme, metric cards, color-coded verdicts, comparison table. Generate programmatically via Python (see HTML Generation Rules below).
2. **PDF report** — if user specifically requests PDF. Use `scripts/generate_pdf_report.py` to create it.
3. **In-chat formatted report** — if file delivery isn't working at all, output the report directly in chat using emoji formatting (✅ ❌ ⬜ ⚠️) that's easy to copy-paste. This is the guaranteed-to-work fallback.

The key insight: delivering the data matters more than the format. If one format fails, immediately try the next — don't keep retrying the same broken approach.

### File Delivery — CRITICAL

In Cowork environments, `present_files` links frequently fail with `ERR_FILE_NOT_FOUND` because the session-to-local path mapping can break. To ensure the user can actually open the report:

1. **Write directly to the user's mounted folder** (e.g., `~/Downloads` or whatever folder they selected). If no folder is mounted, use `request_cowork_directory` to mount `~/Downloads` first. This is the primary delivery method — files written here are immediately accessible on the user's machine.
2. **Also call `present_files`** as a convenience (it may work), but do NOT rely on it as the only delivery method.
3. **Tell the user the local path** so they can open it manually if needed (e.g., "File saved to your Downloads folder: `domain-quality-inspection.html`").

The delivery chain: write to mounted folder → present_files → tell user the filename. All three, every time.

### HTML Generation Rules — CRITICAL

When generating HTML reports, raw `<` characters in text content (like `<1yr`, `<50`) will be interpreted as broken HTML tags by the browser, silently corrupting the entire page from that point onward. This is the #1 cause of "blank page" or "broken report" bugs.

**Always generate HTML programmatically via Python** using `html.escape()` on every piece of text content. Never hand-write HTML with data values inline. The pattern:

```python
import html as html_module

def e(text):
    """HTML-escape all text content."""
    return html_module.escape(str(text))

# CORRECT — escaped:
f'<td>{e(domain["age"])}</td>'      # "<1yr" becomes "&lt;1yr"
f'<p>{e(domain["flags"])}</p>'       # Safe even with < > & " in data

# WRONG — raw text, will break if value contains <:
f'<td>{domain["age"]}</td>'          # "<1yr" breaks the page!
```

Also avoid these Unicode characters that can cause rendering issues on some systems: em dashes (—), special quotes (“”), non-breaking spaces. Use plain ASCII alternatives: hyphens (-), regular quotes, regular spaces.

After generating, validate with:
```python
import re
bad_lt = re.findall(r'<[^/!a-zA-Z]', html_output)
assert not bad_lt, f"Unescaped < found: {bad_lt}"
```

### Status Labels
- **GOOD** = meets or exceeds threshold (green / ✅)
- **BAD** = below threshold, or data raises concerns (red / ❌)
- **N/A** = no free tool available for this criterion (gray / ⬜)

Do NOT use PASS/FAIL/CHECK — users find those confusing.

### PDF Generation Steps

1. Install reportlab: `pip install reportlab --break-system-packages -q`
2. Copy `scripts/generate_pdf_report.py` from this skill's directory to a writable location (the skill directory is read-only)
3. Prepare the data structure (see script docstring for format)
4. Run the script to generate the PDF
5. Write the PDF to the user's mounted folder (see File Delivery above)
6. If the user reports the PDF is blank or unviewable, immediately fall back to HTML or in-chat format — do not spend more than 1 retry on PDF issues

The PDF has 2 pages:
- **Page 1:** Header (domain + date), score ring (GOOD/BAD/N/A), 12 criteria cards (3x4 grid)
- **Page 2:** Insights (BAD vs GOOD side by side) + Verdict box

### In-Chat Format Template

When using the in-chat fallback, use this structure:

```
**DOMAIN QUALITY INSPECTOR**
12-Point SEO & Trust Audit
[Date] | [N] Domains

---

**1. [domain.com]**
[GOOD/BAD/N/A] Verdict: **[APPROVE/REVIEW/REJECT]** ([N] Good - [N] Bad - [N] N/A)

GOOD - Domain Rating: DR [X] (threshold >=50)
GOOD - Organic Traffic: [X]/mo (threshold >=500)
[... all 12 criteria with GOOD/BAD/N/A prefix ...]

Summary: [1-2 sentence summary]

---
[repeat for each domain]

QUICK COMPARISON
[table if multiple domains]
```

### Also save markdown backup

Save a markdown version as `[domain]-inspection-[date].md` using the same GOOD/BAD/N/A labels.

## Bulk Comparison

When inspecting multiple domains, produce a single combined report (not individual files per domain). Include a side-by-side comparison table at the top or bottom.

## Language

Always write reports in English unless the user explicitly requests another language.

## Key Reminders

- **Batch tool visits.** Navigate all 4 tabs before reading results. Don't visit the same tool twice.
- **No-login tools only.** Every tool in v3 works without login.
- **Wait for async data.** SEO tools load results after page renders. Wait 3-5 seconds before reading Ahrefs data.
- **1 retry max.** If a tool fails twice, move on. Use fallback or mark N/A.
- **Criterion 7 keywords.** Infer from site content if user didn't provide.
- **Use URL parameters for Ahrefs.** Direct URLs with `?input=DOMAIN` bypass cookie banners.
- **Wayback for age.** Don't rely on Dotpapa — use Wayback Machine's earliest snapshot.
- **HTML first, not PDF.** HTML is the default output — it's the most visually rich and reliable. PDF only if user asks.
- **Always escape HTML content.** Generate HTML via Python with `html.escape()`. Never hand-write data values into HTML. Raw `<` in text content (like `<1yr`) will break the entire page.
- **Write to mounted folder.** Don't rely solely on `present_files` — write the file directly to the user's mounted directory (e.g., ~/Downloads). Tell the user the filename so they can open it from their file explorer.
- **Read-only skill directory.** Always copy scripts to a writable location before running them.
