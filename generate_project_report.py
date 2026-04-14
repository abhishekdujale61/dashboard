"""
GovAI Dashboard — Project Analysis Report Generator
Produces a professional PDF documenting the full system architecture,
data pipeline, component structure, and key insights.
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, KeepTogether, PageBreak
)
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY, TA_RIGHT
from reportlab.platypus import Flowable

# ── Colour palette (matches dashboard) ─────────────────────────────────────
INDIGO   = colors.HexColor("#6366f1")
SKY      = colors.HexColor("#0ea5e9")
AMBER    = colors.HexColor("#f59e0b")
RED      = colors.HexColor("#ef4444")
GREEN    = colors.HexColor("#10b981")
PURPLE   = colors.HexColor("#8b5cf6")
ORANGE   = colors.HexColor("#f97316")
SLATE    = colors.HexColor("#64748b")
DARK     = colors.HexColor("#0f1117")
MID      = colors.HexColor("#1e2330")
LIGHT_BG = colors.HexColor("#f8fafc")
CARD_BG  = colors.HexColor("#f1f5f9")
TEXT     = colors.HexColor("#1e293b")
MUTED    = colors.HexColor("#64748b")
WHITE    = colors.white
BORDER   = colors.HexColor("#e2e8f0")
EMERALD  = colors.HexColor("#10b981")

PILLAR_COLORS = [INDIGO, SKY, AMBER, RED, GREEN, PURPLE, ORANGE, SLATE]

OUTPUT = "/home/abhishekujale/vector/govai-dashboard/GovAI_Dashboard_Project_Report.pdf"

doc = SimpleDocTemplate(
    OUTPUT,
    pagesize=A4,
    rightMargin=2*cm, leftMargin=2*cm,
    topMargin=2.2*cm, bottomMargin=2.2*cm,
    title="GovAI Dashboard — Project Analysis Report",
    author="GovAI Team",
)

W, H = A4
BODY_W = W - 4*cm

base = getSampleStyleSheet()

def S(name, **kw):
    return ParagraphStyle(name, **kw)

# ── Typography ───────────────────────────────────────────────────────────────
cover_title = S("cover_title",
    fontSize=30, leading=36, textColor=WHITE, fontName="Helvetica-Bold",
    alignment=TA_CENTER)
cover_sub = S("cover_sub",
    fontSize=13, leading=20, textColor=colors.HexColor("#cbd5e1"),
    fontName="Helvetica", alignment=TA_CENTER)
cover_meta = S("cover_meta",
    fontSize=10, leading=15, textColor=colors.HexColor("#94a3b8"),
    fontName="Helvetica", alignment=TA_CENTER)

h1 = S("h1", fontSize=18, leading=24, textColor=INDIGO, fontName="Helvetica-Bold",
    spaceBefore=20, spaceAfter=6)
h2 = S("h2", fontSize=13, leading=18, textColor=TEXT, fontName="Helvetica-Bold",
    spaceBefore=14, spaceAfter=4)
h3 = S("h3", fontSize=11, leading=15, textColor=MUTED, fontName="Helvetica-Bold",
    spaceBefore=10, spaceAfter=2)
body = S("body", fontSize=9.5, leading=15, textColor=TEXT, fontName="Helvetica",
    spaceAfter=4, alignment=TA_JUSTIFY)
body_l = S("body_l", fontSize=9.5, leading=15, textColor=TEXT, fontName="Helvetica",
    spaceAfter=4)
bullet = S("bullet", fontSize=9.5, leading=14, textColor=TEXT, fontName="Helvetica",
    leftIndent=14, firstLineIndent=0, spaceAfter=3,
    bulletIndent=4, bulletText="•")
code_style = S("code", fontSize=8.5, leading=13, textColor=colors.HexColor("#475569"),
    fontName="Courier", backColor=CARD_BG, leftIndent=10, rightIndent=10,
    spaceBefore=4, spaceAfter=4)
caption = S("caption", fontSize=8, leading=11, textColor=MUTED, fontName="Helvetica",
    alignment=TA_CENTER, spaceAfter=6)
tag_style = S("tag", fontSize=8, leading=11, textColor=INDIGO, fontName="Helvetica-Bold",
    alignment=TA_LEFT)
label_bold = S("label_bold", fontSize=9.5, leading=14, textColor=TEXT,
    fontName="Helvetica-Bold")


# ── Custom Flowables ─────────────────────────────────────────────────────────
class ColorBlock(Flowable):
    """Filled rectangle banner for section headers."""
    def __init__(self, text, bg=INDIGO, fg=WHITE, width=None, height=28):
        super().__init__()
        self.text = text
        self.bg = bg
        self.fg = fg
        self.width = width or BODY_W
        self.height = height

    def draw(self):
        self.canv.setFillColor(self.bg)
        self.canv.roundRect(0, 0, self.width, self.height, 4, fill=1, stroke=0)
        self.canv.setFillColor(self.fg)
        self.canv.setFont("Helvetica-Bold", 11)
        self.canv.drawString(10, 8, self.text)

    def wrap(self, *args):
        return self.width, self.height


class HBar(Flowable):
    """Horizontal rule."""
    def __init__(self, color=BORDER, thickness=0.5, width=None):
        super().__init__()
        self.color = color
        self.thickness = thickness
        self.width = width or BODY_W

    def draw(self):
        self.canv.setStrokeColor(self.color)
        self.canv.setLineWidth(self.thickness)
        self.canv.line(0, 0, self.width, 0)

    def wrap(self, *args):
        return self.width, self.thickness + 4


class PillarStrip(Flowable):
    """Horizontal strip of 8 pillar colour squares."""
    def __init__(self, width=None, height=8):
        super().__init__()
        self.width = width or BODY_W
        self.height = height

    def draw(self):
        n = len(PILLAR_COLORS)
        sw = self.width / n
        for i, c in enumerate(PILLAR_COLORS):
            self.canv.setFillColor(c)
            self.canv.rect(i * sw, 0, sw, self.height, fill=1, stroke=0)

    def wrap(self, *args):
        return self.width, self.height


class MermaidDiagram(Flowable):
    """Renders a mermaid-style diagram as ASCII art with styled boxes."""
    def __init__(self, title, lines, bg=CARD_BG, width=None):
        super().__init__()
        self.title = title
        self.lines = lines
        self.bg = bg
        self.width = width or BODY_W
        self.line_h = 14
        self.padding = 8

    def draw(self):
        total_h = self.padding * 2 + 16 + len(self.lines) * self.line_h
        self.canv.setFillColor(self.bg)
        self.canv.roundRect(0, 0, self.width, total_h, 5, fill=1, stroke=0)
        self.canv.setStrokeColor(INDIGO)
        self.canv.setLineWidth(0.8)
        self.canv.roundRect(0, 0, self.width, total_h, 5, fill=0, stroke=1)

        # Title bar
        self.canv.setFillColor(INDIGO)
        self.canv.roundRect(0, total_h - 18, self.width, 18, 3, fill=1, stroke=0)
        self.canv.setFillColor(WHITE)
        self.canv.setFont("Helvetica-Bold", 8)
        self.canv.drawString(8, total_h - 13, self.title)

        # Lines
        self.canv.setFillColor(colors.HexColor("#334155"))
        self.canv.setFont("Courier", 7.5)
        y = total_h - 18 - self.line_h
        for line in self.lines:
            self.canv.drawString(10, y, line)
            y -= self.line_h

    def wrap(self, *args):
        total_h = self.padding * 2 + 16 + len(self.lines) * self.line_h
        return self.width, total_h


def cover_page():
    """Generate the cover page elements."""
    elems = []

    # Dark background banner
    class CoverBanner(Flowable):
        def draw(self):
            self.canv.setFillColor(DARK)
            self.canv.rect(0, 0, BODY_W, 200, fill=1, stroke=0)
            # Gradient-like accent
            for i, c in enumerate(PILLAR_COLORS):
                self.canv.setFillColor(c)
                self.canv.rect(i * (BODY_W / 8), 195, BODY_W / 8, 5, fill=1, stroke=0)

        def wrap(self, *args): return BODY_W, 200

    elems.append(Spacer(1, 0.5*cm))
    elems.append(CoverBanner())
    elems.append(Spacer(1, -190))  # overlap text on banner

    # Overlay text
    elems.append(Paragraph("GovAI Dashboard", cover_title))
    elems.append(Spacer(1, 0.3*cm))
    elems.append(Paragraph("Project Analysis Report", cover_sub))
    elems.append(Spacer(1, 0.5*cm))
    elems.append(Paragraph("Canada AI Task Force — National AI Strategy Consultation", cover_meta))
    elems.append(Spacer(1, 3.5*cm))

    elems.append(HBar(INDIGO, 1.5))
    elems.append(Spacer(1, 0.4*cm))

    # Meta table
    meta = [
        ["Project", "GovAI Dashboard"],
        ["Type", "React · TypeScript · Vite · Tailwind CSS v4"],
        ["Data Source", "open.canada.ca — ai-strategy-raw-data-2025-1.xlsx"],
        ["Pipeline", "3-Pass LLM Pipeline (Groq llama-3.1-8b-instant)"],
        ["Respondents", "11,383 Canadians · 28 Task Force Experts"],
        ["Responses", "68,702 open-text responses · 32 Expert Reports"],
        ["Date", "April 2026"],
    ]
    t = Table(meta, colWidths=[4.5*cm, BODY_W - 4.5*cm])
    t.setStyle(TableStyle([
        ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
        ("FONTNAME", (1, 0), (1, -1), "Helvetica"),
        ("FONTSIZE", (0, 0), (-1, -1), 9),
        ("TEXTCOLOR", (0, 0), (0, -1), INDIGO),
        ("TEXTCOLOR", (1, 0), (1, -1), TEXT),
        ("ROWBACKGROUNDS", (0, 0), (-1, -1), [CARD_BG, WHITE]),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("GRID", (0, 0), (-1, -1), 0.3, BORDER),
    ]))
    elems.append(t)
    elems.append(Spacer(1, 0.4*cm))
    elems.append(HBar(BORDER))
    elems.append(Spacer(1, 0.4*cm))
    elems.append(Paragraph(
        "This report documents the complete architecture, data pipeline, component design, "
        "and analytical findings of the GovAI Dashboard — an open-source tool that makes "
        "Canada's national AI strategy consultation transparent and explorable.",
        body))
    elems.append(PageBreak())
    return elems


def toc():
    elems = []
    elems.append(ColorBlock("TABLE OF CONTENTS"))
    elems.append(Spacer(1, 0.4*cm))

    sections = [
        ("1", "Executive Summary", "3"),
        ("2", "System Architecture Overview", "4"),
        ("3", "Data Pipeline", "5"),
        ("4", "Frontend Architecture", "7"),
        ("5", "The 8 Strategic Pillars", "9"),
        ("6", "Alignment Analysis", "11"),
        ("7", "Dashboard Components", "12"),
        ("8", "Key Insights & Findings", "14"),
        ("9", "Deployment & Infrastructure", "15"),
        ("10", "Mermaid Diagrams", "16"),
    ]

    rows = []
    for num, title, page in sections:
        rows.append([
            Paragraph(f"<b>{num}</b>", label_bold),
            Paragraph(title, body_l),
            Paragraph(page, S("pg", fontSize=9, fontName="Helvetica", textColor=MUTED, alignment=TA_RIGHT)),
        ])

    t = Table(rows, colWidths=[0.8*cm, BODY_W - 2.2*cm, 1.4*cm])
    t.setStyle(TableStyle([
        ("ROWBACKGROUNDS", (0, 0), (-1, -1), [WHITE, CARD_BG]),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("LINEBELOW", (0, 0), (-1, -1), 0.3, BORDER),
    ]))
    elems.append(t)
    elems.append(PageBreak())
    return elems


def section_executive_summary():
    elems = []
    elems.append(ColorBlock("1 — EXECUTIVE SUMMARY"))
    elems.append(Spacer(1, 0.3*cm))

    elems.append(Paragraph(
        "The GovAI Dashboard is an open-source data visualisation platform built to make "
        "Canada's 2025 national AI strategy consultation transparent and analytically rigorous. "
        "The Government of Canada's official summary was vague, contained no data weighting, "
        "and failed to surface where 11,383 public respondents and 28 Task Force experts actually "
        "agreed or disagreed. This dashboard fixes that.", body))

    elems.append(Spacer(1, 0.2*cm))

    stats = [
        ["11,383", "Total Respondents"],
        ["3,162", "Fully Submitted"],
        ["68,702", "Open-text Responses"],
        ["26", "Survey Questions"],
        ["28", "Task Force Experts"],
        ["32", "Expert Reports"],
        ["8", "Strategic Pillars"],
        ["93", "Mapped Recommendations"],
    ]

    cols = 4
    rows_data = []
    for i in range(0, len(stats), cols):
        chunk = stats[i:i+cols]
        row_val = []
        row_lbl = []
        for val, lbl in chunk:
            row_val.append(Paragraph(f'<font color="#6366f1" size="18"><b>{val}</b></font>', S("sv", fontSize=18, fontName="Helvetica-Bold", textColor=INDIGO, alignment=TA_CENTER)))
            row_lbl.append(Paragraph(lbl, S("sl", fontSize=8, fontName="Helvetica", textColor=MUTED, alignment=TA_CENTER)))
        rows_data.append(row_val)
        rows_data.append(row_lbl)

    cw = BODY_W / cols
    t = Table(rows_data, colWidths=[cw] * cols)
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), CARD_BG),
        ("ROWBACKGROUNDS", (0, 0), (-1, -1), [CARD_BG, WHITE]),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("GRID", (0, 0), (-1, -1), 0.3, BORDER),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
    ]))
    elems.append(t)
    elems.append(Spacer(1, 0.4*cm))

    elems.append(Paragraph("Core Question", h2))
    elems.append(Paragraph(
        "Across 8 strategic domains, how do the priorities of 11,383 Canadians compare to the "
        "priorities of 28 AI experts — and where do they diverge?", body))

    elems.append(Paragraph("Key Capabilities", h2))
    for item in [
        "Interactive radar chart comparing public vs. expert priority scores across all 8 pillars",
        "Alignment scatter plot revealing divergences with plain-language tension explanations",
        "93 searchable Task Force recommendations with public support scores",
        "Full demographic breakdown: geography, age, gender, sector, respondent role",
        "Per-pillar drill-down with topic-level comment viewer (public quotes + expert chunks)",
        "Real data sourced from open.canada.ca under Open Government Licence (Canada)",
    ]:
        elems.append(Paragraph(item, bullet))

    elems.append(Spacer(1, 0.3*cm))
    elems.append(HBar())
    return elems


def section_architecture():
    elems = []
    elems.append(Spacer(1, 0.3*cm))
    elems.append(ColorBlock("2 — SYSTEM ARCHITECTURE OVERVIEW"))
    elems.append(Spacer(1, 0.3*cm))

    elems.append(Paragraph(
        "The GovAI Dashboard is a single-page application (SPA) with a static data pipeline. "
        "There is no backend server at runtime — all data is pre-processed and baked into "
        "JSON files that ship with the frontend bundle.", body))

    elems.append(Paragraph("High-Level System Diagram", h2))

    arch_lines = [
        "┌─────────────────────────────────────────────────────────────────────┐",
        "│                     DATA SOURCES                                    │",
        "│  open.canada.ca XLSX  ←→  32 Expert Report DOCXs                   │",
        "└──────────────────────────────┬──────────────────────────────────────┘",
        "                               │",
        "                     ┌─────────▼──────────┐",
        "                     │  Python Pipeline   │  (3-pass LLM via Groq)",
        "                     │  pipeline/         │",
        "                     └─────────┬──────────┘",
        "                               │  chunks.db (SQLite)",
        "                     ┌─────────▼──────────┐",
        "                     │   JSON Export      │  src/data/*.json",
        "                     └─────────┬──────────┘",
        "                               │",
        "         ┌─────────────────────▼──────────────────────┐",
        "         │            React Frontend (Vite)            │",
        "         │  ┌──────────┐ ┌─────────┐ ┌────────────┐  │",
        "         │  │Overview  │ │Alignment│ │ Pillar     │  │",
        "         │  │Demographics│Recs    │ │ TopicDetail│  │",
        "         │  └──────────┘ └─────────┘ └────────────┘  │",
        "         └────────────────────┬───────────────────────┘",
        "                              │  npm run build",
        "                     ┌────────▼────────┐",
        "                     │  dist/ (static) │  → Vercel",
        "                     └─────────────────┘",
    ]
    elems.append(MermaidDiagram("System Architecture", arch_lines))
    elems.append(Spacer(1, 0.3*cm))

    elems.append(Paragraph("Technology Stack", h2))
    stack = [
        ["Layer", "Technology", "Version", "Purpose"],
        ["Frontend Framework", "React", "19.x", "UI component tree"],
        ["Language", "TypeScript", "5.9.x", "Type safety across all modules"],
        ["Build Tool", "Vite", "7.x", "Dev server + production bundler"],
        ["Styling", "Tailwind CSS", "v4 (Oxide)", "Utility-first dark-mode UI"],
        ["Charts", "Recharts", "3.x", "Radar, scatter, bar, donut charts"],
        ["Routing", "React Router", "v7", "Client-side SPA navigation"],
        ["Data Pipeline", "Python", "3.11", "XLSX parsing + LLM enrichment"],
        ["LLM API", "Groq", "llama-3.1-8b", "Atomize, label, canonicalize"],
        ["Database", "SQLite", "—", "Intermediate chunk storage"],
        ["Deployment", "Vercel", "—", "Static site hosting"],
        ["Linting", "ESLint + TypeScript-ESLint", "9.x", "Code quality enforcement"],
    ]
    t = Table(stack, colWidths=[4.5*cm, 3.5*cm, 2.5*cm, BODY_W - 10.5*cm])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), INDIGO),
        ("TEXTCOLOR", (0, 0), (-1, 0), WHITE),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),
        ("FONTSIZE", (0, 0), (-1, -1), 8.5),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [WHITE, CARD_BG]),
        ("GRID", (0, 0), (-1, -1), 0.3, BORDER),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
    ]))
    elems.append(t)
    elems.append(PageBreak())
    return elems


def section_pipeline():
    elems = []
    elems.append(ColorBlock("3 — DATA PIPELINE"))
    elems.append(Spacer(1, 0.3*cm))

    elems.append(Paragraph(
        "The data pipeline transforms raw government XLSX data and expert DOCX reports "
        "into structured JSON consumed by the React frontend. It runs as a 5-script Python "
        "pipeline with a SQLite intermediate store.", body))

    elems.append(Paragraph("Pipeline Scripts", h2))

    scripts = [
        ["Script", "Function", "Input", "Output"],
        ["01_load_xlsx.py", "Parse XLSX → SQLite", "ai-strategy-raw-data-2025-1.xlsx", "chunks.db rows (raw)"],
        ["02_pass1_atomize.py", "LLM Pass 1: Atomize", "Raw open-text chunks", "Atomic claim chunks"],
        ["03_pass2_label.py", "LLM Pass 2: Label", "Atomic chunks", "Sentiment + salience + depth labels"],
        ["04_pass3_canonicalize.py", "LLM Pass 3: Canonicalize", "Labelled expert chunks", "Canonical header + body"],
        ["05_export_json.py", "Export → src/data/", "chunks.db", "quotes.json, expert_chunks.json, topics.json"],
    ]
    t = Table(scripts, colWidths=[4.2*cm, 4*cm, 4*cm, BODY_W - 12.2*cm])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), DARK),
        ("TEXTCOLOR", (0, 0), (-1, 0), WHITE),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),
        ("FONTSIZE", (0, 0), (-1, -1), 8),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [WHITE, CARD_BG]),
        ("GRID", (0, 0), (-1, -1), 0.3, BORDER),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("LEFTPADDING", (0, 0), (-1, -1), 5),
        ("WORDWRAP", (0, 0), (-1, -1), True),
    ]))
    elems.append(t)
    elems.append(Spacer(1, 0.3*cm))

    elems.append(Paragraph("3-Pass LLM Pipeline Detail", h2))

    pipeline_flow = [
        "                   RAW OPEN-TEXT RESPONSE",
        "                          │",
        "         ┌────────────────▼────────────────┐",
        "  PASS 1 │  ATOMIZE (llama-3.1-8b-instant) │",
        "         │  Break multi-idea paragraphs     │",
        "         │  into single atomic claims        │",
        "         └────────────────┬────────────────┘",
        "                          │  Atomic chunk",
        "         ┌────────────────▼────────────────┐",
        "  PASS 2 │  LABEL   (llama-3.1-8b-instant) │",
        "         │  Assign: sentiment, salience,    │",
        "         │  depth, pillar, topic             │",
        "         └────────────────┬────────────────┘",
        "                          │  Labelled chunk",
        "         ┌────────────────▼────────────────┐",
        "  PASS 3 │  CANONICALIZE (expert only)      │",
        "         │  Normalize expert report chunks   │",
        "         │  to structured header+body format │",
        "         └────────────────┬────────────────┘",
        "                          │",
        "               ┌──────────▼──────────┐",
        "               │  chunks.db (SQLite)  │",
        "               └──────────┬──────────┘",
        "                          │  05_export_json.py",
        "          ┌───────────────┼───────────────┐",
        "          ▼               ▼               ▼",
        "    quotes.json   expert_chunks.json   topics.json",
    ]
    elems.append(MermaidDiagram("3-Pass LLM Pipeline", pipeline_flow))
    elems.append(Spacer(1, 0.3*cm))

    elems.append(Paragraph("Scoring System", h2))
    elems.append(Paragraph(
        "Each chunk receives a composite score used for priority calculation and ordering:", body))

    scoring_lines = [
        "score = salience_weight × depth_weight",
        "",
        "Salience weights:   primary=3,  secondary=2,  passing=1",
        "Depth weights:      evidence-based=3,  reasoned=2,  assertion=1",
        "",
        "Max score = 9  (primary + evidence-based)",
        "Min score = 1  (passing + assertion)",
        "",
        "Pillar priority score = Σ(chunk scores) / max_possible",
        "Normalized to 0–10 scale across submitted respondents",
    ]
    elems.append(MermaidDiagram("Scoring Formula", scoring_lines, bg=colors.HexColor("#f0fdf4")))
    elems.append(Spacer(1, 0.3*cm))

    elems.append(Paragraph("Question-to-Pillar Mapping", h2))
    elems.append(Paragraph(
        "The 26 XLSX survey questions are mapped to 8 pillars. Distribution is uneven — "
        "Adoption & Commercialization has 10 questions, while Regulation & Governance has only 1. "
        "This directly affects raw response volume comparisons.", body))

    q_map = [
        ["Pillar", "XLSX Columns", "Question Count"],
        ["Talent & Research", "27–30", "4"],
        ["Adoption & Commercialization", "31–40", "10"],
        ["Public Trust & Safety", "41, 43", "2"],
        ["Regulation & Governance", "42", "1"],
        ["Inclusive AI / Workforce", "44–46", "3"],
        ["Data & Infrastructure", "47–49", "3"],
        ["Sovereignty & Security", "50–52", "3"],
        ["International Collaboration", "—", "—  (derived from expert reports)"],
    ]
    cw_qmap = [6.5*cm, 3*cm, BODY_W - 9.5*cm]
    t2 = Table(q_map, colWidths=cw_qmap)
    t2.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), SLATE),
        ("TEXTCOLOR", (0, 0), (-1, 0), WHITE),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),
        ("FONTSIZE", (0, 0), (-1, -1), 8.5),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [WHITE, CARD_BG]),
        ("GRID", (0, 0), (-1, -1), 0.3, BORDER),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
    ]))
    elems.append(t2)
    elems.append(PageBreak())
    return elems


def section_frontend():
    elems = []
    elems.append(ColorBlock("4 — FRONTEND ARCHITECTURE"))
    elems.append(Spacer(1, 0.3*cm))

    elems.append(Paragraph("Component Tree", h2))

    tree_lines = [
        "App (BrowserRouter + DashboardProvider)",
        "└── AppShell (layout wrapper)",
        "    ├── Header",
        "    │   ├── GovAI logo + title",
        "    │   └── Navigation links",
        "    ├── Sidebar (desktop)",
        "    └── <Outlet> (page content)",
        "        ├── OverviewPage            /",
        "        │   ├── StatBlock ×4",
        "        │   ├── PillarRadarChart",
        "        │   ├── RespondentDonut",
        "        │   ├── PillarBarChart",
        "        │   └── PillarCard ×8",
        "        ├── DemographicsPage        /demographics",
        "        │   ├── GeographyBarChart",
        "        │   ├── SectorPieChart",
        "        │   └── Demographics tables",
        "        ├── AlignmentPage           /alignment",
        "        │   ├── AlignmentScatterPlot",
        "        │   └── Alignment detail table",
        "        ├── RecommendationsPage     /recommendations",
        "        │   ├── Pillar filter chips",
        "        │   ├── Priority filter + search",
        "        │   └── RecommendationCard grid",
        "        ├── PillarDetailPage        /pillars/:pillarId",
        "        │   ├── Pillar summary + scores",
        "        │   ├── Topic cards grid",
        "        │   └── Expert report section",
        "        └── TopicDetailPage         /pillars/:id/topics/:topicId",
        "            ├── PublicQuotePanel",
        "            └── ExpertChunkPanel",
    ]
    elems.append(MermaidDiagram("Component Tree", tree_lines))
    elems.append(Spacer(1, 0.3*cm))

    elems.append(Paragraph("State Management", h2))
    elems.append(Paragraph(
        "The application uses a single React Context (DashboardContext) for cross-page state. "
        "All other state is local. There is no Redux, Zustand, or external state library.", body))

    state_lines = [
        "DashboardContext {",
        "  activePillarId: string | null    // currently selected pillar filter",
        "  setActivePillarId: (id) => void  // cross-page filter setter",
        "  filteredRecommendations: Recommendation[]  // derived from activePillarId",
        "}",
        "",
        "// Usage: RecommendationsPage reads filteredRecommendations",
        "//        PillarCard calls setActivePillarId on click",
        "//        PillarBarChart navigates + sets active pillar",
    ]
    elems.append(MermaidDiagram("State Architecture", state_lines, bg=colors.HexColor("#f0f9ff")))
    elems.append(Spacer(1, 0.3*cm))

    elems.append(Paragraph("Routing Structure", h2))
    routes = [
        ["Route", "Component", "Description"],
        ["/", "OverviewPage", "Headline stats, radar chart, pillar cards"],
        ["/demographics", "DemographicsPage", "Who responded — geography, age, gender, sector"],
        ["/alignment", "AlignmentPage", "Scatter plot + table of public vs expert gap"],
        ["/recommendations", "RecommendationsPage", "93 recommendations with filters + search"],
        ["/pillars/:pillarId", "PillarDetailPage", "Per-pillar deep dive: summary, topics, expert report"],
        ["/pillars/:pillarId/topics/:topicId", "TopicDetailPage", "Topic view: public response count vs expert reference count + quote/chunk panels"],
    ]
    t = Table(routes, colWidths=[5*cm, 4*cm, BODY_W - 9*cm])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), INDIGO),
        ("TEXTCOLOR", (0, 0), (-1, 0), WHITE),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),
        ("FONTSIZE", (0, 0), (-1, -1), 8.5),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [WHITE, CARD_BG]),
        ("GRID", (0, 0), (-1, -1), 0.3, BORDER),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
    ]))
    elems.append(t)
    elems.append(Spacer(1, 0.3*cm))

    elems.append(Paragraph("Data Flow", h2))
    df_lines = [
        "src/data/*.json  ──(static import)──► src/data/index.ts",
        "                                              │",
        "                             ┌────────────────┼──────────────────┐",
        "                             ▼                ▼                  ▼",
        "                         PILLARS         DEMOGRAPHICS       ALIGNMENT_MAP",
        "                         TOPICS          QUOTES             RECOMMENDATIONS",
        "                         EXPERT_CHUNKS   EXPERT_REPORTS",
        "                             │",
        "                    imported directly in page components",
        "                    or via DashboardContext",
    ]
    elems.append(MermaidDiagram("Data Flow", df_lines))
    elems.append(PageBreak())
    return elems


def section_pillars():
    elems = []
    elems.append(ColorBlock("5 — THE 8 STRATEGIC PILLARS"))
    elems.append(Spacer(1, 0.3*cm))
    elems.append(PillarStrip())
    elems.append(Spacer(1, 0.3*cm))

    pillars = [
        ("P1", "Talent & Research", "#6366f1", 8.9, 9.1, "aligned", 14, 10832,
         "Strengthen Canadian AI talent pipelines through graduate funding, compute access grants, and global researcher attraction programs."),
        ("P2", "Data & Infrastructure", "#0ea5e9", 8.7, 8.8, "aligned", 11, 5840,
         "Build sovereign data infrastructure and open dataset commons accessible to researchers and SMEs."),
        ("P3", "Adoption & Commercialization", "#f59e0b", 9.1, 8.5, "tension", 12, 23303,
         "Accelerate AI adoption through tax incentives, regulatory sandboxes, and commercialization bridges. Only 32.4% of Canadian AI companies remain in Canada (2024)."),
        ("P4", "Regulation & Governance", "#ef4444", 8.5, 8.3, "aligned", 16, 7643,
         "Establish a risk-tiered AI regulatory framework with AIDA as the foundation, augmented by sector-specific guidance."),
        ("P5", "International Collaboration", "#10b981", 7.6, 7.9, "aligned", 8, 2162,
         "Position Canada as a multilateral AI governance leader through G7, OECD, and bilateral science agreements."),
        ("P6", "Public Trust & Safety", "#8b5cf6", 9.1, 8.7, "aligned", 13, 7643,
         "Build public literacy, transparent auditing requirements, and redress mechanisms. 83% of public responses mentioned trust/safety keywords."),
        ("P7", "Inclusive AI", "#f97316", 6.2, 7.5, "tension", 10, 6926,
         "Ensure Indigenous data sovereignty, accessibility for persons with disabilities, and equity-by-design. Largest expert-public divergence (+1.3)."),
        ("P8", "Sovereignty & Security", "#64748b", 8.2, 8.1, "aligned", 9, 6101,
         "Protect critical AI infrastructure, prevent foreign acquisition of AI companies, and establish national security review protocols."),
    ]

    rows = [["#", "Pillar", "Public", "Expert", "Status", "Recs", "Responses"]]
    for p in pillars:
        num, name, col, pub, exp, status, recs, resp, _ = p
        status_text = "✓ Aligned" if status == "aligned" else "⚠ Tension"
        rows.append([num, name, str(pub), str(exp), status_text, str(recs), f"{resp:,}"])

    cw = [0.8*cm, 5.2*cm, 1.3*cm, 1.3*cm, 2*cm, 1.2*cm, BODY_W - 11.8*cm]
    t = Table(rows, colWidths=cw)
    style = [
        ("BACKGROUND", (0, 0), (-1, 0), DARK),
        ("TEXTCOLOR", (0, 0), (-1, 0), WHITE),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),
        ("FONTSIZE", (0, 0), (-1, -1), 8),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [WHITE, CARD_BG]),
        ("GRID", (0, 0), (-1, -1), 0.3, BORDER),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("LEFTPADDING", (0, 0), (-1, -1), 5),
    ]
    for i, p in enumerate(pillars):
        c = colors.HexColor(p[2])
        style.append(("TEXTCOLOR", (1, i+1), (1, i+1), c))
        style.append(("FONTNAME", (1, i+1), (1, i+1), "Helvetica-Bold"))
        if p[5] == "tension":
            style.append(("TEXTCOLOR", (4, i+1), (4, i+1), AMBER))
        else:
            style.append(("TEXTCOLOR", (4, i+1), (4, i+1), EMERALD))
    t.setStyle(TableStyle(style))
    elems.append(t)
    elems.append(Spacer(1, 0.4*cm))

    elems.append(Paragraph("Pillar Summaries", h2))
    for p in pillars:
        num, name, col, pub, exp, status, recs, resp, summary = p
        c = colors.HexColor(col)
        elems.append(KeepTogether([
            Paragraph(f'<font color="{col}"><b>{num} — {name}</b></font>  '
                      f'<font color="#64748b" size="8">Public: {pub}/10 · Expert: {exp}/10 · {recs} recs · {resp:,} responses</font>',
                      S("ph", fontSize=9.5, fontName="Helvetica-Bold", textColor=c, spaceBefore=6)),
            Paragraph(summary, S("ps", fontSize=8.5, fontName="Helvetica", textColor=MUTED,
                                 leftIndent=8, spaceAfter=3)),
        ]))

    elems.append(PageBreak())
    return elems


def section_alignment():
    elems = []
    elems.append(ColorBlock("6 — ALIGNMENT ANALYSIS"))
    elems.append(Spacer(1, 0.3*cm))

    elems.append(Paragraph(
        "Alignment is measured as the absolute difference (delta) between the public priority "
        "score and the expert priority score for each pillar. The system classifies this gap "
        "into three tiers:", body))

    legend = [
        ["Status", "Delta Threshold", "Meaning", "Count"],
        ["✓ Aligned", "Δ < 1.0", "Public and experts broadly agree on importance", "6"],
        ["⚠ In Tension", "Δ 1.0 – 1.5", "Meaningful difference — one group rates it notably higher", "2"],
        ["✗ Diverges", "Δ > 1.5", "Significant gap — values difference or awareness gap", "0"],
    ]
    t = Table(legend, colWidths=[3*cm, 3.5*cm, 7*cm, BODY_W - 13.5*cm])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), INDIGO),
        ("TEXTCOLOR", (0, 0), (-1, 0), WHITE),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),
        ("FONTSIZE", (0, 0), (-1, -1), 8.5),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [WHITE, CARD_BG]),
        ("GRID", (0, 0), (-1, -1), 0.3, BORDER),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("TEXTCOLOR", (0, 1), (0, 1), EMERALD),
        ("TEXTCOLOR", (0, 2), (0, 2), AMBER),
        ("TEXTCOLOR", (0, 3), (0, 3), RED),
    ]))
    elems.append(t)
    elems.append(Spacer(1, 0.3*cm))

    elems.append(Paragraph("Scatter Plot Logic", h2))
    scatter_lines = [
        "AlignmentScatterPlot renders each pillar as a point:",
        "",
        "  X-axis = publicScore  (0–10)",
        "  Y-axis = expertScore  (0–10)",
        "  Diagonal line = perfect alignment (y = x)",
        "",
        "  Point ABOVE diagonal → experts rate higher than public",
        "  Point BELOW diagonal → public rates higher than experts",
        "",
        "  Color encoding:",
        "    Green  = aligned (Δ < 1.0)",
        "    Amber  = tension (Δ 1.0–1.5)",
        "    Red    = diverges (Δ > 1.5)",
        "",
        "  Label = first letter of pillar name",
        "  Hover = full pillar name + scores + tension note",
    ]
    elems.append(MermaidDiagram("Scatter Plot Specification", scatter_lines, bg=colors.HexColor("#f0f9ff")))
    elems.append(Spacer(1, 0.3*cm))

    elems.append(Paragraph("Topic-Level Design Decision", h2))
    elems.append(Paragraph(
        "Alignment scoring (aligned / tension / diverges) is applied at the pillar level only. "
        "At the topic level, showing a divergence label would be misleading: the public were "
        "explicitly directed to respond to those specific questions, so a score gap between public "
        "and expert does not represent a genuine difference in priority — it is an artefact of "
        "survey design.", body))
    elems.append(Paragraph(
        "Topics therefore display only the raw count of public responses vs expert references "
        "as a neutral, factual comparison. No score, no delta, no alignment badge.", body))

    topic_design = [
        "TopicCard shows:",
        "  ✓  Topic label",
        "  ✓  Public response count  (proportional bar)",
        "  ✓  Expert reference count (proportional bar)",
        "  ✓  Dominant public sentiment badge",
        "  ✓  Total response count",
        "",
        "  ✗  Public priority score",
        "  ✗  Expert priority score",
        "  ✗  Delta / gap",
        "  ✗  TensionBadge (aligned / tension / diverges)",
        "  ✗  'Sentiment divergence' label",
    ]
    elems.append(MermaidDiagram("Topic Card — What Is and Is Not Shown", topic_design, bg=colors.HexColor("#f0fdf4")))
    elems.append(Spacer(1, 0.2*cm))

    elems.append(Paragraph("Key Tensions", h2))
    tensions = [
        ("Adoption & Commercialization (P3)", "Δ = −0.6",
         "Public (9.1) vs Expert (8.5). Not a values conflict — both want commercialization. "
         "The tension is pace vs. safety guardrails. Public wants faster movement; experts "
         "emphasize ensuring safety infrastructure is in place first."),
        ("Inclusive AI (P7)", "Δ = +1.3",
         "Experts (7.5) vs Public (6.2). The largest gap in the consultation. "
         "This is an awareness gap, not a values gap. Only 25% of public respondents mentioned "
         "inclusion-related keywords vs. 83% who mentioned trust/safety. "
         "The public may not have been sufficiently prompted on inclusion dimensions."),
    ]
    for name, delta, desc in tensions:
        elems.append(KeepTogether([
            Paragraph(f'<b>{name}</b>  <font color="#f59e0b">{delta}</font>',
                      S("th", fontSize=10, fontName="Helvetica-Bold", textColor=TEXT, spaceBefore=8)),
            Paragraph(desc, S("td", fontSize=9, fontName="Helvetica", textColor=MUTED,
                               leftIndent=10, spaceAfter=4)),
        ]))

    elems.append(PageBreak())
    return elems


def section_components():
    elems = []
    elems.append(ColorBlock("7 — DASHBOARD COMPONENTS"))
    elems.append(Spacer(1, 0.3*cm))

    elems.append(Paragraph("Chart Components", h2))
    charts = [
        ["Component", "File", "Chart Type", "Data Source"],
        ["PillarRadarChart", "charts/PillarRadarChart.tsx", "Radar (spider web)", "pillars.json"],
        ["PillarBarChart", "charts/PillarBarChart.tsx", "Vertical bar", "pillars.json"],
        ["RespondentDonut", "charts/RespondentDonut.tsx", "Donut / Pie", "demographics.json"],
        ["AlignmentScatterPlot", "charts/AlignmentScatterPlot.tsx", "Scatter plot", "alignmentMap.json"],
        ["GeographyBarChart", "charts/GeographyBarChart.tsx", "Horizontal bar", "demographics.json"],
        ["SectorPieChart", "charts/SectorPieChart.tsx", "Pie chart", "demographics.json"],
    ]
    t = Table(charts, colWidths=[4*cm, 5*cm, 3.5*cm, BODY_W - 12.5*cm])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), SKY),
        ("TEXTCOLOR", (0, 0), (-1, 0), WHITE),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),
        ("FONTSIZE", (0, 0), (-1, -1), 8),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [WHITE, CARD_BG]),
        ("GRID", (0, 0), (-1, -1), 0.3, BORDER),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("LEFTPADDING", (0, 0), (-1, -1), 5),
    ]))
    elems.append(t)
    elems.append(Spacer(1, 0.3*cm))

    elems.append(Paragraph("Card & Viewer Components", h2))
    cards = [
        ["Component", "File", "Purpose"],
        ["PillarCard", "cards/PillarCard.tsx", "Pillar overview with scores and alignment status badge"],
        ["RecommendationCard", "cards/RecommendationCard.tsx", "Single recommendation with priority, expert, public support score"],
        ["TopicCard", "cards/TopicCard.tsx", "Topic within a pillar — shows public response count vs expert reference count (no scores, no divergence label)"],
        ["PublicQuotePanel", "viewer/PublicQuotePanel.tsx", "Paginated list of public quotes for a topic"],
        ["ExpertChunkPanel", "viewer/ExpertChunkPanel.tsx", "Paginated expert report chunks for a topic"],
    ]
    t2 = Table(cards, colWidths=[4*cm, 5*cm, BODY_W - 9*cm])
    t2.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), PURPLE),
        ("TEXTCOLOR", (0, 0), (-1, 0), WHITE),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),
        ("FONTSIZE", (0, 0), (-1, -1), 8),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [WHITE, CARD_BG]),
        ("GRID", (0, 0), (-1, -1), 0.3, BORDER),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("LEFTPADDING", (0, 0), (-1, -1), 5),
    ]))
    elems.append(t2)
    elems.append(Spacer(1, 0.3*cm))

    elems.append(Paragraph("UI Atoms", h2))
    ui = [
        ["Component", "Purpose"],
        ["TensionBadge", "Displays alignment status (aligned / tension / diverges) — pillar level only, not used at topic level"],
        ["SentimentBadge", "Shows sentiment type (supportive / opposed / concerned / neutral)"],
        ["PillarBadge", "Coloured pill showing pillar name, used in filter chips"],
        ["SectionHeader", "Consistent title + subtitle block for all chart/table sections"],
        ["Toggle", "Boolean on/off switch (used for expert report toggle)"],
    ]
    t3 = Table(ui, colWidths=[4*cm, BODY_W - 4*cm])
    t3.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), SLATE),
        ("TEXTCOLOR", (0, 0), (-1, 0), WHITE),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),
        ("FONTSIZE", (0, 0), (-1, -1), 8),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [WHITE, CARD_BG]),
        ("GRID", (0, 0), (-1, -1), 0.3, BORDER),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("LEFTPADDING", (0, 0), (-1, -1), 5),
    ]))
    elems.append(t3)
    elems.append(PageBreak())
    return elems


def section_insights():
    elems = []
    elems.append(ColorBlock("8 — KEY INSIGHTS & FINDINGS"))
    elems.append(Spacer(1, 0.3*cm))

    insights = [
        ("1", AMBER, "#f59e0b", "Adoption & Commercialization is a timing debate, not a values conflict.",
         "Both the public (9.1) and experts (8.5) rate this pillar highly. The tension is not "
         "whether Canada should commercialize AI — everyone agrees it should. The real debate is "
         "whether to move fast now or ensure safety guardrails are in place first. "
         "Critical stat: only 32.4% of Canadian-founded AI companies remain in Canada (down from 74.9% in 2016)."),

        ("2", ORANGE, "#f97316", "Inclusive AI has an awareness gap, not a values gap.",
         "Experts rate Inclusive AI at 7.5; the public at 6.2 — the largest divergence. "
         "Only 25% of public respondents mentioned inclusion-related keywords vs. 83% who mentioned "
         "trust and safety. The public may not have been prompted to think about inclusion dimensions. "
         "Policy should not interpret the gap as opposition to inclusive AI."),

        ("3", PURPLE, "#8b5cf6", "Public Trust & Safety is the dominant public concern by a wide margin.",
         "83% of all public responses with text included trust and safety keywords — far higher than "
         "any other topic. No other pillar comes close. Any AI strategy that does not lead with trust "
         "mechanisms risks losing public legitimacy."),

        ("4", RED, "#ef4444", "Geographic concentration is a structural risk in the data.",
         "Ontario (38.9%) and British Columbia (20.7%) together account for nearly 60% of all responses. "
         "Voices from northern Canada, rural communities, and smaller provinces are significantly "
         "underrepresented. Any policy derived from this consultation carries that geographic bias."),

        ("5", SKY, "#0ea5e9", "Response volume alone cannot compare pillar priority.",
         "Adoption & Commercialization has 23,303 responses because it had 10 survey questions. "
         "Regulation & Governance had only 1 question. Raw volume comparisons without normalizing "
         "for question count are misleading. The dashboard normalizes by question count and respondent weight."),

        ("6", EMERALD, "#10b981", "Public and expert views are broadly aligned across 6 of 8 pillars.",
         "The consultation narrative of public vs. expert conflict is overblown. "
         "Six of eight pillars show delta < 1.0 (aligned). The two exceptions are not conflicts — "
         "they are a timing debate (P3) and an awareness gap (P7). Canada has substantial consensus "
         "to build on."),
    ]

    for num, color, hex_str, title, desc in insights:
        elems.append(KeepTogether([
            Spacer(1, 0.15*cm),
            Paragraph(f'<font color="{hex_str}"><b>{num}. {title}</b></font>',
                      S("it", fontSize=10, fontName="Helvetica-Bold", textColor=color, spaceBefore=4)),
            Paragraph(desc, S("id", fontSize=9, fontName="Helvetica", textColor=MUTED,
                               leftIndent=10, spaceAfter=2, alignment=TA_JUSTIFY)),
            HBar(BORDER, 0.3),
        ]))

    elems.append(PageBreak())
    return elems


def section_deployment():
    elems = []
    elems.append(ColorBlock("9 — DEPLOYMENT & INFRASTRUCTURE"))
    elems.append(Spacer(1, 0.3*cm))

    elems.append(Paragraph("Build & Deploy", h2))
    deploy_lines = [
        "Local Development:",
        "  npm install",
        "  npm run dev           # Vite dev server → http://localhost:5173",
        "",
        "Production Build:",
        "  npm run build         # tsc -b && vite build → dist/",
        "",
        "Deployment (Vercel):",
        "  vercel.json → outputDirectory: 'dist'",
        "  buildCommand: 'npm run build'",
        "  framework: 'vite'",
        "",
        "Alternative (Netlify):",
        "  netlify.toml → publish = 'dist'",
        "  command = 'npm run build'",
        "  [[redirects]] from='/*' to='/index.html' status=200",
    ]
    elems.append(MermaidDiagram("Build & Deployment Commands", deploy_lines))
    elems.append(Spacer(1, 0.3*cm))

    elems.append(Paragraph("File Structure", h2))
    fs_lines = [
        "govai-dashboard/",
        "├── src/",
        "│   ├── App.tsx                 # Router + provider setup",
        "│   ├── main.tsx                # React DOM entry",
        "│   ├── index.css               # Tailwind CSS v4 base",
        "│   ├── context/",
        "│   │   └── DashboardContext.tsx",
        "│   ├── data/                   # All JSON data files",
        "│   │   ├── index.ts            # Re-exports",
        "│   │   ├── pillars.json",
        "│   │   ├── demographics.json",
        "│   │   ├── alignmentMap.json",
        "│   │   ├── recommendations.json",
        "│   │   ├── topics.json",
        "│   │   ├── quotes.json",
        "│   │   └── expert_chunks.json",
        "│   ├── pages/                  # 6 route pages",
        "│   ├── components/             # Charts, cards, UI atoms, viewers",
        "│   └── types/index.ts          # TypeScript interfaces",
        "├── pipeline/                   # Python data pipeline",
        "│   ├── 01_load_xlsx.py",
        "│   ├── 02_pass1_atomize.py",
        "│   ├── 03_pass2_label.py",
        "│   ├── 04_pass3_canonicalize.py",
        "│   ├── 05_export_json.py",
        "│   └── config.py",
        "├── public/                     # Static assets",
        "├── vercel.json                 # Deployment config",
        "└── package.json",
    ]
    elems.append(MermaidDiagram("Project File Structure", fs_lines))
    elems.append(Spacer(1, 0.3*cm))

    elems.append(Paragraph("Environment Variables", h2))
    env = [
        ["Variable", "Used By", "Description"],
        ["GROQ_API_KEY", "pipeline/02–04", "Groq API key for LLM pipeline passes"],
        ["XLSX_PATH", "pipeline/config.py", "Path to ai-strategy-raw-data-2025-1.xlsx"],
    ]
    t = Table(env, colWidths=[4*cm, 4*cm, BODY_W - 8*cm])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), DARK),
        ("TEXTCOLOR", (0, 0), (-1, 0), WHITE),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),
        ("FONTSIZE", (0, 0), (-1, -1), 8.5),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [WHITE, CARD_BG]),
        ("GRID", (0, 0), (-1, -1), 0.3, BORDER),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
    ]))
    elems.append(t)
    elems.append(PageBreak())
    return elems


def section_mermaid():
    elems = []
    elems.append(ColorBlock("10 — MERMAID DIAGRAMS"))
    elems.append(Spacer(1, 0.3*cm))
    elems.append(Paragraph(
        "The following diagrams represent the system in Mermaid notation. "
        "These can be rendered in any Mermaid-compatible tool (GitHub Markdown, Notion, etc.).",
        body))

    elems.append(Paragraph("10.1 — Overall Data Flow", h2))
    d1 = [
        "graph TD",
        "    A[open.canada.ca XLSX] --> B[01_load_xlsx.py]",
        "    C[32 Expert DOCXs] --> D[02_pass1_atomize.py]",
        "    B --> E[(chunks.db SQLite)]",
        "    D --> E",
        "    E --> F[03_pass2_label.py]",
        "    F --> G[04_pass3_canonicalize.py]",
        "    G --> H[05_export_json.py]",
        "    H --> I[src/data/quotes.json]",
        "    H --> J[src/data/expert_chunks.json]",
        "    H --> K[src/data/topics.json]",
        "    I --> L[React Frontend]",
        "    J --> L",
        "    K --> L",
        "    L --> M[Vercel - dist/]",
    ]
    elems.append(MermaidDiagram("Mermaid: Data Flow (graph TD)", d1))
    elems.append(Spacer(1, 0.3*cm))

    elems.append(Paragraph("10.2 — Component Hierarchy", h2))
    d2 = [
        "graph TD",
        "    App --> DashboardProvider",
        "    DashboardProvider --> AppShell",
        "    AppShell --> Header",
        "    AppShell --> Sidebar",
        "    AppShell --> Outlet",
        "    Outlet --> OverviewPage",
        "    Outlet --> DemographicsPage",
        "    Outlet --> AlignmentPage",
        "    Outlet --> RecommendationsPage",
        "    Outlet --> PillarDetailPage",
        "    Outlet --> TopicDetailPage",
        "    OverviewPage --> PillarRadarChart",
        "    OverviewPage --> RespondentDonut",
        "    OverviewPage --> PillarBarChart",
        "    AlignmentPage --> AlignmentScatterPlot",
        "    TopicDetailPage --> PublicQuotePanel",
        "    TopicDetailPage --> ExpertChunkPanel",
    ]
    elems.append(MermaidDiagram("Mermaid: Component Hierarchy (graph TD)", d2))
    elems.append(Spacer(1, 0.3*cm))

    elems.append(Paragraph("10.3 — User Navigation Flow", h2))
    d3 = [
        "flowchart LR",
        "    Start([User lands on /]) --> Overview",
        "    Overview -->|Click pillar card| PillarDetail",
        "    Overview -->|Nav link| Demographics",
        "    Overview -->|Nav link| Alignment",
        "    Overview -->|Nav link| Recommendations",
        "    PillarDetail -->|Click topic| TopicDetail",
        "    TopicDetail -->|Back| PillarDetail",
        "    Recommendations -->|Click pillar chip| Recommendations",
        "    Alignment -->|Hover point| Alignment[Alignment tooltip]",
        "    Demographics -->|View charts| Demographics[Demographics charts]",
    ]
    elems.append(MermaidDiagram("Mermaid: User Navigation (flowchart LR)", d3))
    elems.append(Spacer(1, 0.3*cm))

    elems.append(Paragraph("10.4 — TypeScript Type Hierarchy", h2))
    d4 = [
        "classDiagram",
        "    class Pillar {",
        "        +string id",
        "        +number publicPriorityScore",
        "        +number expertPriorityScore",
        "        +AlignmentStatus alignmentStatus",
        "    }",
        "    class Topic {",
        "        +string pillarId",
        "        +number publicScore",
        "        +number expertScore",
        "        +SentimentType dominantPublicSentiment",
        "    }",
        "    class PublicQuote {",
        "        +SentimentType sentiment",
        "        +SalienceLevel salience",
        "        +DepthLevel depth",
        "        +number score",
        "    }",
        "    class ExpertChunk {",
        "        +string expertName",
        "        +string affiliation",
        "        +string reportTitle",
        "        +number score",
        "    }",
        "    class Recommendation {",
        "        +string pillarId",
        "        +string member",
        "        +PriorityLevel priority",
        "        +number publicSupportScore",
        "    }",
        "    Pillar '1' --> '*' Topic",
        "    Topic '1' --> '*' PublicQuote",
        "    Topic '1' --> '*' ExpertChunk",
        "    Pillar '1' --> '*' Recommendation",
    ]
    elems.append(MermaidDiagram("Mermaid: Type Hierarchy (classDiagram)", d4))
    elems.append(Spacer(1, 0.3*cm))

    elems.append(Paragraph("10.5 — Topic-Level Display Design", h2))
    elems.append(Paragraph(
        "Topics do not use scores or divergence labels. "
        "The public were explicitly asked those questions, so a score gap is a survey artefact, "
        "not a genuine priority difference. Response counts are shown instead.", body))

    d5a = [
        "flowchart TD",
        "    PL[Pillar Level] -->|Uses scores + delta| PA",
        "    PA[TensionBadge / Public score / Expert score / Gap delta]",
        "",
        "    TL[Topic Level] -->|Counts only - no scores| TA",
        "    TA[Public response count / Expert reference count]",
        "    TA --> TB[No score  No delta  No TensionBadge]",
    ]
    elems.append(MermaidDiagram("Mermaid 10.5a: Pillar vs Topic Display Logic (flowchart TD)", d5a))
    elems.append(Spacer(1, 0.2*cm))

    d5b = [
        "flowchart LR",
        "    TC[TopicCard]",
        "    TC --> L[Topic label]",
        "    TC --> PB[Public responses - proportional bar + count]",
        "    TC --> EB[Expert references - proportional bar + count]",
        "    TC --> SM[Dominant public sentiment badge]",
        "    TC --> TOT[Total response count]",
        "",
        "    TD[TopicDetailPage]",
        "    TD --> C1[Public responses - count stat box]",
        "    TD --> C2[Expert references - count stat box]",
        "    TD --> C3[Total responses - count stat box]",
        "    TD --> QP[PublicQuotePanel]",
        "    TD --> EP[ExpertChunkPanel]",
    ]
    elems.append(MermaidDiagram("Mermaid 10.5b: TopicCard and TopicDetailPage Structure (flowchart LR)", d5b))
    elems.append(Spacer(1, 0.3*cm))

    elems.append(Paragraph("10.6 — LLM Pipeline Sequence", h2))
    d5 = [
        "sequenceDiagram",
        "    participant XLSX as XLSX File",
        "    participant DB as SQLite DB",
        "    participant Groq as Groq API",
        "    participant JSON as src/data/",
        "",
        "    XLSX->>DB: 01_load_xlsx.py (raw chunks)",
        "    DB->>Groq: 02_pass1_atomize (batch prompts)",
        "    Groq-->>DB: Atomic claims",
        "    DB->>Groq: 03_pass2_label (label each chunk)",
        "    Groq-->>DB: Labelled chunks",
        "    DB->>Groq: 04_pass3_canonicalize (expert only)",
        "    Groq-->>DB: Canonical header+body",
        "    DB->>JSON: 05_export_json.py",
        "    JSON-->>React: Static import at build time",
    ]
    elems.append(MermaidDiagram("Mermaid: LLM Pipeline Sequence (sequenceDiagram)", d5))

    elems.append(Spacer(1, 0.4*cm))
    elems.append(HBar(INDIGO, 1))
    elems.append(Spacer(1, 0.2*cm))
    elems.append(Paragraph(
        "End of Report — GovAI Dashboard Project Analysis · April 2026 · "
        "Data: open.canada.ca Open Government Licence (Canada)",
        caption))
    return elems


# ── Build document ──────────────────────────────────────────────────────────
story = []
story += cover_page()
story += toc()
story += section_executive_summary()
story += section_architecture()
story += section_pipeline()
story += section_frontend()
story += section_pillars()
story += section_alignment()
story += section_components()
story += section_insights()
story += section_deployment()
story += section_mermaid()

doc.build(story)
print(f"✓ Report generated: {OUTPUT}")
