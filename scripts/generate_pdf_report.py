"""
Domain Quality Inspector â PDF Report Generator

Usage:
    from generate_pdf_report import generate_report

    data = [
        # (id, name, value, sub_text, source, status)
        # status: "good", "bad", or "na"
        (1, "Domain Rating", "DR 11", "Threshold >= 50. Very weak.", "Ahrefs", "bad"),
        (2, "Organic Traffic", "5 /mo", "Threshold >= 500/mo.", "Ahrefs", "bad"),
        # ... all 12 criteria
    ]

    bad_items = ["DR 11 - min threshold 50", ...]
    good_items = ["Domain ~11 years old - mature", ...]
    verdict_text = "4 GOOD vs 6 BAD. Main asset: ..."

    generate_report(
        domain="example.com",
        date_str="April 10, 2026",
        data=data,
        bad_items=bad_items,
        good_items=good_items,
        verdict_text=verdict_text,
        output_path="/path/to/output.pdf"
    )
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib.colors import HexColor
from reportlab.pdfgen import canvas

W, H = A4

# Colors
BG = HexColor("#09090b")
CARD_BG = HexColor("#18181b")
CARD_BORDER = HexColor("#27272a")
WHITE = HexColor("#ffffff")
GRAY = HexColor("#a1a1aa")
DIM = HexColor("#71717a")
GREEN = HexColor("#22c55e")
RED = HexColor("#ef4444")
NA_GRAY = HexColor("#6b7280")
AMBER = HexColor("#f59e0b")

STATUS_COLORS = {"good": GREEN, "bad": RED, "na": NA_GRAY}
STATUS_BG = {"good": HexColor("#0a2e14"), "bad": HexColor("#2e0a0a"), "na": HexColor("#1a1a1f")}
STATUS_LABELS = {"good": "GOOD", "bad": "BAD", "na": "N/A"}


def _rounded_rect(c, x, y, w, h, r, fill=None, stroke=None):
    p = c.beginPath()
    p.moveTo(x + r, y)
    p.lineTo(x + w - r, y)
    p.arcTo(x + w - r, y, x + w, y + r, r)
    p.lineTo(x + w, y + h - r)
    p.arcTo(x + w, y + h - r, x + w - r, y + h, r)
    p.lineTo(x + r, y + h)
    p.arcTo(x + r, y + h, x, y + h - r, r)
    p.lineTo(x, y + r)
    p.arcTo(x, y + r, x + r, y, r)
    p.close()
    if fill:
        c.setFillColor(fill)
    if stroke:
        c.setStrokeColor(stroke)
        c.drawPath(p, fill=1, stroke=1)
    else:
        c.drawPath(p, fill=1, stroke=0)


def _badge(c, x, y, text, status):
    tw = c.stringWidth(text, "Helvetica-Bold", 8) + 12
    _rounded_rect(c, x, y - 4, tw, 14, 7, fill=STATUS_BG[status])
    c.setFillColor(STATUS_COLORS[status])
    c.setFont("Helvetica-Bold", 8)
    c.drawString(x + 6, y, text)


def _card(c, x, y, item, card_w=170, card_h=88):
    idx, name, value, sub, src, status = item

    _rounded_rect(c, x, y, card_w, card_h, 6, fill=CARD_BG)

    # Left accent
    c.setFillColor(STATUS_COLORS[status])
    c.rect(x, y + 6, 3, card_h - 12, fill=1, stroke=0)

    # Title
    c.setFillColor(GRAY)
    c.setFont("Helvetica", 7)
    c.drawString(x + 10, y + card_h - 14, f"{idx}. {name.upper()}")

    # Badge
    _badge(c, x + card_w - 45, y + card_h - 16, STATUS_LABELS[status], status)

    # Value
    c.setFillColor(WHITE)
    c.setFont("Helvetica-Bold", 16)
    val_display = value if len(value) < 12 else value[:11] + ".."
    c.drawString(x + 10, y + card_h - 36, val_display)

    # Sub text
    c.setFillColor(GRAY)
    c.setFont("Helvetica", 6.5)
    if len(sub) > 45:
        c.drawString(x + 10, y + card_h - 50, sub[:45])
        c.drawString(x + 10, y + card_h - 59, sub[45:90])
    else:
        c.drawString(x + 10, y + card_h - 50, sub)

    # Source
    c.setFillColor(DIM)
    c.setFont("Helvetica", 5.5)
    c.drawString(x + 10, y + 6, src)


def _score_circle(c, cx, cy, r, good, bad, na, total):
    c.setStrokeColor(CARD_BORDER)
    c.setLineWidth(7)
    c.circle(cx, cy, r, fill=0, stroke=1)

    good_angle = (good / total) * 360
    bad_angle = (bad / total) * 360
    na_angle = (na / total) * 360

    if good_angle > 0:
        c.setStrokeColor(GREEN)
        c.setLineWidth(7)
        p = c.beginPath()
        p.arc(cx - r, cy - r, cx + r, cy + r, 90, good_angle)
        c.drawPath(p, fill=0, stroke=1)

    if bad_angle > 0:
        c.setStrokeColor(RED)
        c.setLineWidth(7)
        p2 = c.beginPath()
        p2.arc(cx - r, cy - r, cx + r, cy + r, 90 + good_angle, bad_angle)
        c.drawPath(p2, fill=0, stroke=1)

    if na_angle > 0:
        c.setStrokeColor(NA_GRAY)
        c.setLineWidth(7)
        p3 = c.beginPath()
        p3.arc(cx - r, cy - r, cx + r, cy + r, 90 + good_angle + bad_angle, na_angle)
        c.drawPath(p3, fill=0, stroke=1)

    # Center text
    c.setFillColor(WHITE)
    c.setFont("Helvetica-Bold", 22)
    c.drawCentredString(cx, cy + 2, str(good))
    c.setFillColor(DIM)
    c.setFont("Helvetica", 9)
    c.drawCentredString(cx, cy - 10, f"/ {total}")
    c.setFillColor(AMBER)
    c.setFont("Helvetica-Bold", 7)

    verdict_label = "APPROVE" if good >= 8 else ("REJECT" if good <= 3 else "REVIEW")
    c.drawCentredString(cx, cy - 20, verdict_label)


def generate_report(domain, date_str, data, bad_items, good_items, verdict_text, output_path):
    """Generate a 2-page PDF report for a domain inspection."""
    c = canvas.Canvas(output_path, pagesize=A4)

    good = sum(1 for d in data if d[5] == "good")
    bad = sum(1 for d in data if d[5] == "bad")
    na = sum(1 for d in data if d[5] == "na")

    # === PAGE 1 ===
    c.setFillColor(BG)
    c.rect(0, 0, W, H, fill=1, stroke=0)

    # Title
    c.setFillColor(WHITE)
    c.setFont("Helvetica-Bold", 22)
    c.drawCentredString(W / 2, H - 40, "Domain Quality Inspector")
    c.setFillColor(DIM)
    c.setFont("Helvetica", 13)
    c.drawCentredString(W / 2, H - 58, domain)
    c.setFillColor(HexColor("#3f3f46"))
    c.setFont("Helvetica", 9)
    c.drawCentredString(W / 2, H - 72, date_str)

    # Score circle
    _score_circle(c, W / 2 - 50, H - 112, 25, good, bad, na, 12)

    # Legend
    lx = W / 2 + 15
    ly = H - 98
    for label, color, count in [("GOOD", GREEN, good), ("BAD", RED, bad), ("N/A", NA_GRAY, na)]:
        c.setFillColor(color)
        c.circle(lx, ly + 3, 4, fill=1, stroke=0)
        c.setFillColor(WHITE)
        c.setFont("Helvetica-Bold", 9)
        c.drawString(lx + 9, ly, f"{count} {label}")
        ly -= 15

    # Cards grid
    margin_x = 28
    card_w = (W - 2 * margin_x - 20) / 3
    card_h = 88
    gap = 10
    start_y = H - 155

    for i, item in enumerate(data):
        col = i % 3
        row = i // 3
        x = margin_x + col * (card_w + gap)
        y = start_y - row * (card_h + gap)
        _card(c, x, y, item, card_w, card_h)

    # === PAGE 2 ===
    c.showPage()
    c.setFillColor(BG)
    c.rect(0, 0, W, H, fill=1, stroke=0)

    c.setFillColor(WHITE)
    c.setFont("Helvetica-Bold", 18)
    c.drawCentredString(W / 2, H - 40, "Insights")

    # BAD box
    bx = 28
    bw = (W - 66) / 2
    bh = 50 + len(bad_items) * 22
    by = H - 70 - bh
    _rounded_rect(c, bx, by, bw, bh, 8, fill=CARD_BG)

    c.setFillColor(RED)
    c.setFont("Helvetica-Bold", 13)
    c.drawString(bx + 14, by + bh - 22, f"BAD ({bad})")

    c.setFont("Helvetica", 9)
    yy = by + bh - 44
    for item in bad_items:
        c.setFillColor(RED)
        c.circle(bx + 18, yy + 3, 2.5, fill=1, stroke=0)
        c.setFillColor(HexColor("#d4d4d8"))
        c.drawString(bx + 26, yy, item[:60])
        yy -= 20

    # GOOD box
    gx = bx + bw + 10
    gh = 50 + len(good_items) * 22
    gy = H - 70 - gh
    _rounded_rect(c, gx, gy, bw, gh, 8, fill=CARD_BG)

    c.setFillColor(GREEN)
    c.setFont("Helvetica-Bold", 13)
    c.drawString(gx + 14, gy + gh - 22, f"GOOD ({good})")

    c.setFont("Helvetica", 9)
    yy = gy + gh - 44
    for item in good_items:
        c.setFillColor(GREEN)
        c.circle(gx + 18, yy + 3, 2.5, fill=1, stroke=0)
        c.setFillColor(HexColor("#d4d4d8"))
        c.drawString(gx + 26, yy, item[:60])
        yy -= 20

    # Verdict box
    min_y = min(by, gy)
    vy = min_y - 80
    vw = W - 56
    vh = 60
    _rounded_rect(c, 28, vy, vw, vh, 8, fill=HexColor("#1c1c1f"), stroke=CARD_BORDER)

    verdict_label = "APPROVE" if good >= 8 else ("REJECT" if good <= 3 else "REVIEW FURTHER")
    c.setFillColor(AMBER)
    c.setFont("Helvetica-Bold", 12)
    c.drawString(42, vy + vh - 18, f"Verdict: {verdict_label}")

    c.setFillColor(GRAY)
    c.setFont("Helvetica", 8)
    # Wrap verdict text
    words = verdict_text.split()
    lines = []
    line = ""
    for w in words:
        if c.stringWidth(line + " " + w, "Helvetica", 8) > vw - 30:
            lines.append(line)
            line = w
        else:
            line = (line + " " + w).strip()
    if line:
        lines.append(line)

    ty = vy + vh - 34
    for ln in lines[:3]:
        c.drawString(42, ty, ln)
        ty -= 12

    c.save()
    return output_path


# CLI usage
if __name__ == "__main__":
    import sys
    print("This script is meant to be imported. See docstring for usage.")
    print(f"Output: generate_report(domain, date, data, bad_items, good_items, verdict, path)")

