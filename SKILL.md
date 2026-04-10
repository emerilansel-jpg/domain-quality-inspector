---
name: domain-quality-inspector
description: >
  Evaluate any named domain's SEO quality and trustworthiness with a 12-point inspection.
  Use this skill whenever a user mentions a specific domain name (like example.com, site.org,
  brand.co) and wants it checked, inspected, evaluated, or vetted. Covers: domain rating,
  spam score, backlink health, traffic legitimacy, domain age, deindex history, PBN detection,
  anchor text analysis.
---

# Domain Quality Inspector v3

See the full SKILL.md in the releases section for complete instructions. This file is a summary.

This skill provides a 12-point SEO domain quality inspection using free tools (Ahrefs, Wayback Machine, Google SERP).

## Criteria

1. Domain Rating (DR >= 50)
2. Organic Traffic (>= 500/mo)
3. Traffic Trend (stable/growing)
4. Inbound Backlinks Health
5. Outbound Links (N/A)
6. Anchor Text Health
7. Page 1 Rankings
8. TF:CF Ratio (N/A)
9. Spam Score (< 5%)
10. Domain Age (>= 2 years)
11. Deindex History
12. Link Equity Ratio

## Output Formats

1. PDF report (primary)
2. HTML report (fallback)
3. In-chat emoji format (guaranteed fallback)

## Installation

Download the `.skill` file from Releases and install in Claude Code / Cowork.
