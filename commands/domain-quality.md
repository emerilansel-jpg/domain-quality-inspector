---
description: Run a 12-point domain quality inspection
argument-hint: "<domain or comma-separated domains>"
---

# Domain Quality Inspection

Run the full 12-point SEO quality inspection on the domain(s) provided in $ARGUMENTS.

## Instructions

1. Read the skill instructions from `SKILL.md` in this skill's directory
2. Parse the domain(s) from $ARGUMENTS â normalize them (strip protocols, www, paths)
3. If no domain was provided, ask the user for one
4. Execute the 12-point inspection following the skill's tool batching strategy
5. Use Ahrefs URL parameters (`?input=DOMAIN`) to bypass cookie banners
6. Use Wayback Machine for domain age (Dotpapa is unreliable)
7. Copy `scripts/generate_pdf_report.py` to a writable directory before running
8. Try PDF delivery first; if it fails, fall back to HTML, then in-chat format
9. For multiple domains, produce a single combined report with comparison table
10. Save a markdown backup as `[domain]-inspection-[date].md`
11. Always write in English unless user specifies otherwise
