"""Render a small documented Markdown subset and verify text/page geometry."""

import re
import sys
from html import escape
from pathlib import Path

from pypdf import PdfReader
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import (
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)


def inline(text):
    """Escape input before applying the supported emphasis syntax."""
    text = escape(text)
    text = re.sub(r"`([^`]+)`", r'<font name="Courier">\1</font>', text)
    return re.sub(r"\*\*([^*]+)\*\*", r"<b>\1</b>", text)


def render(source, destination):
    text = source.read_text()
    if "```" in text or "![" in text:
        raise ValueError("Code blocks and images require a reviewed renderer extension")
    if any(ord(c) > 126 and c not in "\n\r\t" for c in text):
        raise ValueError("Use ASCII mathematical notation to avoid missing PDF glyphs")
    styles = getSampleStyleSheet()
    styles.add(
        ParagraphStyle(
            "Body",
            fontName="Helvetica",
            fontSize=10,
            leading=13,
            textColor=colors.HexColor("#243448"),
            spaceAfter=6,
        )
    )
    styles.add(
        ParagraphStyle(
            "Cell", parent=styles["Body"], fontSize=9, leading=12, spaceAfter=0, alignment=TA_LEFT
        )
    )
    for name in ["Title", "Heading1", "Heading2"]:
        styles[name].textColor = colors.HexColor("#143c5a")
    styles["Heading1"].fontSize = 14
    styles["Heading1"].leading = 17
    styles["Heading1"].spaceBefore = 10
    styles["Heading1"].spaceAfter = 6
    story = []
    lines = text.splitlines()
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        i += 1
        if not line:
            continue
        if line == "<!-- pagebreak -->":
            story.append(PageBreak())
        elif line.startswith("# "):
            story.append(Paragraph(inline(line[2:]), styles["Title"]))
            story.append(Spacer(1, 5 * mm))
        elif line.startswith("## "):
            story.append(Paragraph(inline(line[3:]), styles["Heading1"]))
        elif line.startswith("### "):
            story.append(Paragraph(inline(line[4:]), styles["Heading2"]))
        elif line.startswith("|"):
            table_lines = [line]
            while i < len(lines) and lines[i].strip().startswith("|"):
                table_lines.append(lines[i].strip())
                i += 1
            cells = [[x.strip() for x in s.strip("|").split("|")] for s in table_lines]
            cells = [r for r in cells if not all(re.fullmatch(r":?-+:?", x) for x in r)]
            if any(len(r) != len(cells[0]) for r in cells):
                raise ValueError("Ragged Markdown table")
            table = Table(
                [[Paragraph(inline(x), styles["Cell"]) for x in r] for r in cells],
                colWidths=[166 * mm / len(cells[0])] * len(cells[0]),
                repeatRows=1,
            )
            table.setStyle(
                TableStyle(
                    [
                        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#e3edf4")),
                        (
                            "ROWBACKGROUNDS",
                            (0, 1),
                            (-1, -1),
                            [colors.white, colors.HexColor("#f5f7f9")],
                        ),
                        ("VALIGN", (0, 0), (-1, -1), "TOP"),
                        ("TOPPADDING", (0, 0), (-1, -1), 5),
                        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
                        ("LINEBELOW", (0, 0), (-1, 0), 0.6, colors.HexColor("#8fa7b7")),
                    ]
                )
            )
            story.extend([table, Spacer(1, 4 * mm)])
        else:
            paragraph = [line]
            while (
                i < len(lines) and lines[i].strip() and not lines[i].startswith(("#", "|", "<!--"))
            ):
                paragraph.append(lines[i].strip())
                i += 1
            story.append(Paragraph(inline(" ".join(paragraph)), styles["Body"]))
    destination.parent.mkdir(parents=True, exist_ok=True)

    def footer(canvas, doc):
        canvas.saveState()
        canvas.setStrokeColor(colors.HexColor("#c4d2dc"))
        canvas.line(22 * mm, 18 * mm, 188 * mm, 18 * mm)
        canvas.setFont("Helvetica", 8)
        canvas.setFillColor(colors.HexColor("#52677a"))
        canvas.drawString(22 * mm, 13 * mm, "QUANT RESEARCH APPRENTICESHIP | Learning note")
        canvas.drawRightString(188 * mm, 13 * mm, str(doc.page))
        canvas.restoreState()

    doc = SimpleDocTemplate(
        str(destination),
        pagesize=(210 * mm, 297 * mm),
        leftMargin=22 * mm,
        rightMargin=22 * mm,
        topMargin=20 * mm,
        bottomMargin=25 * mm,
        title=source.stem,
        author="Quant Research Apprenticeship",
    )
    doc.build(story, onFirstPage=footer, onLaterPages=footer)
    reader = PdfReader(destination)
    extracted = " ".join(page.extract_text() for page in reader.pages)
    for heading in re.findall(r"^#{1,3} (.+)$", text, re.M):
        if heading not in extracted:
            raise ValueError(f"Missing heading: {heading}")
    for page in reader.pages:
        if not page.extract_text().strip():
            raise ValueError("Blank page")
        width, height = float(page.mediabox.width), float(page.mediabox.height)

        def check_bounds(fragment, cm, tm, font, size, width=width, height=height):
            if fragment.strip() and not (
                -1 <= cm[4] + tm[4] <= width + 1 and -1 <= cm[5] + tm[5] <= height + 1
            ):
                raise ValueError("Text origin outside page bounds")

        page.extract_text(visitor_text=check_bounds)
    print(
        f"Verified {len(reader.pages)} pages; {len(extracted)} extracted characters: {destination}"
    )
    return len(reader.pages)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        raise SystemExit("Usage: render_note.py INPUT.md OUTPUT.pdf")
    render(Path(sys.argv[1]), Path(sys.argv[2]))
