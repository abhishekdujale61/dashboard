"""
Generate a PDF document analyzing the relationship between:
  - AiStrategyReport_EN.pdf (ISED public consultation summary)
  - taskforcereports_rapportsgroupedetravail/ (32 expert reports)
  - govai-dashboard (React implementation)
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, KeepTogether, PageBreak
)
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
from reportlab.platypus import Flowable

# ── colour palette (matches the dashboard) ─────────────────────────────────
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
TEXT     = colors.HexColor("#1e293b")
MUTED    = colors.HexColor("#64748b")
WHITE    = colors.white

# ── pillar colours matching dashboard ──────────────────────────────────────
PILLAR_COLORS = {
    "Talent & Research":           INDIGO,
    "Data & Infrastructure":       SKY,
    "Adoption & Commercialization":AMBER,
    "Regulation & Governance":     RED,
    "International Collaboration": GREEN,
    "Public Trust & Safety":       PURPLE,
    "Inclusive AI":                ORANGE,
    "Sovereignty & Security":      SLATE,
}


# ── document ────────────────────────────────────────────────────────────────
OUTPUT = "/home/abhishekujale/vector/govai-dashboard/Dashboard_Analysis_Report.pdf"

doc = SimpleDocTemplate(
    OUTPUT,
    pagesize=A4,
    rightMargin=2*cm, leftMargin=2*cm,
    topMargin=2.2*cm, bottomMargin=2.2*cm,
    title="GovAI Dashboard — Source Analysis & Data Mapping",
    author="Claude Code Analysis",
)

W, H = A4
BODY_W = W - 4*cm

# ── styles ──────────────────────────────────────────────────────────────────
base = getSampleStyleSheet()

def S(name, **kw):
    s = ParagraphStyle(name, **kw)
    return s

cover_title = S("cover_title",
    fontSize=28, leading=34, textColor=WHITE, fontName="Helvetica-Bold",
    alignment=TA_CENTER)

cover_sub = S("cover_sub",
    fontSize=13, leading=18, textColor=colors.HexColor("#94a3b8"),
    fontName="Helvetica", alignment=TA_CENTER)

h1 = S("h1",
    fontSize=18, leading=24, textColor=INDIGO, fontName="Helvetica-Bold",
    spaceBefore=18, spaceAfter=6)

h2 = S("h2",
    fontSize=13, leading=17, textColor=TEXT, fontName="Helvetica-Bold",
    spaceBefore=12, spaceAfter=4)

h3 = S("h3",
    fontSize=11, leading=15, textColor=MUTED, fontName="Helvetica-Bold",
    spaceBefore=8, spaceAfter=3)

body = S("body",
    fontSize=9.5, leading=14, textColor=TEXT, fontName="Helvetica",
    alignment=TA_JUSTIFY, spaceAfter=5)

bullet = S("bullet",
    fontSize=9.5, leading=14, textColor=TEXT, fontName="Helvetica",
    leftIndent=14, bulletIndent=4, spaceAfter=2)

caption = S("caption",
    fontSize=8, leading=11, textColor=MUTED, fontName="Helvetica",
    alignment=TA_CENTER, spaceAfter=4)

label_white = S("label_white",
    fontSize=9, leading=12, textColor=WHITE, fontName="Helvetica-Bold",
    alignment=TA_CENTER)

label_dark = S("label_dark",
    fontSize=8.5, leading=11, textColor=TEXT, fontName="Helvetica")

callout = S("callout",
    fontSize=9, leading=13, textColor=colors.HexColor("#065f46"),
    fontName="Helvetica", leftIndent=10, rightIndent=10,
    borderPad=6, backColor=colors.HexColor("#f0fdf4"),
    borderColor=GREEN, borderWidth=1, spaceBefore=6, spaceAfter=6)

warn = S("warn",
    fontSize=9, leading=13, textColor=colors.HexColor("#92400e"),
    fontName="Helvetica", leftIndent=10, rightIndent=10,
    borderPad=6, backColor=colors.HexColor("#fffbeb"),
    borderColor=AMBER, borderWidth=1, spaceBefore=6, spaceAfter=6)

code_style = S("code_style",
    fontSize=8, leading=11, textColor=colors.HexColor("#312e81"),
    fontName="Courier", backColor=colors.HexColor("#eef2ff"),
    leftIndent=8, borderPad=4, spaceBefore=3, spaceAfter=3)

# ── helper flowables ────────────────────────────────────────────────────────

class ColorBar(Flowable):
    """Full-width horizontal colour bar."""
    def __init__(self, colour, height=4):
        super().__init__()
        self.colour = colour
        self._height = height
        self.width = BODY_W

    def draw(self):
        self.canv.setFillColor(self.colour)
        self.canv.rect(0, 0, self.width, self._height, stroke=0, fill=1)

    def wrap(self, *_):
        return (self.width, self._height)


class CoverBlock(Flowable):
    """Dark hero block for cover page."""
    def __init__(self, width, height):
        super().__init__()
        self.width = width
        self.height = height

    def draw(self):
        c = self.canv
        c.setFillColor(DARK)
        c.roundRect(0, 0, self.width, self.height, 12, stroke=0, fill=1)
        # accent line
        c.setFillColor(INDIGO)
        c.rect(0, self.height-6, self.width, 6, stroke=0, fill=1)

    def wrap(self, *_):
        return (self.width, self.height)


class PillarChip(Flowable):
    """Coloured rounded chip for a pillar."""
    def __init__(self, label, colour, public, expert, recs, align_status):
        super().__init__()
        self.label  = label
        self.colour = colour
        self.public = public
        self.expert = expert
        self.recs   = recs
        self.status = align_status
        self.width  = BODY_W
        self.height = 38

    def draw(self):
        c = self.canv
        # background
        c.setFillColor(colors.HexColor("#f8fafc"))
        c.roundRect(0, 0, self.width, self.height, 6, stroke=0, fill=1)
        # left colour accent
        c.setFillColor(self.colour)
        c.roundRect(0, 0, 6, self.height, 3, stroke=0, fill=1)
        # pillar label
        c.setFont("Helvetica-Bold", 9)
        c.setFillColor(TEXT)
        c.drawString(14, 24, self.label)
        # scores
        c.setFont("Helvetica", 8)
        c.setFillColor(MUTED)
        c.drawString(14, 12, f"Public: {self.public}/10   Expert: {self.expert}/10   Recs: {self.recs}")
        # alignment badge
        status_col = GREEN if self.status == "aligned" else AMBER
        status_txt = "Aligned" if self.status == "aligned" else "Tension"
        c.setFillColor(status_col)
        bw = 52
        c.roundRect(self.width - bw - 8, 11, bw, 16, 4, stroke=0, fill=1)
        c.setFont("Helvetica-Bold", 7)
        c.setFillColor(WHITE)
        c.drawCentredString(self.width - 8 - bw/2, 16, status_txt)

    def wrap(self, *_):
        return (self.width, self.height)


def HR(colour=colors.HexColor("#e2e8f0"), thickness=0.5):
    return HRFlowable(width="100%", thickness=thickness, color=colour,
                      spaceAfter=4, spaceBefore=4)

def P(text, style=None):
    return Paragraph(text, style or body)

def B(text):
    return Paragraph(f"• {text}", bullet)

def SP(n=6):
    return Spacer(1, n)


# ══════════════════════════════════════════════════════════════════════════════
# BUILD CONTENT
# ══════════════════════════════════════════════════════════════════════════════
story = []

# ─────────────────────────────────────────────────────────────────────────────
# COVER PAGE
# ─────────────────────────────────────────────────────────────────────────────
story.append(SP(40))
story.append(CoverBlock(BODY_W, 200))
story.append(SP(-200))   # overlay text on top of block

story.append(SP(20))
story.append(Paragraph(
    "GovAI Dashboard",
    S("ct", fontSize=30, leading=36, textColor=WHITE, fontName="Helvetica-Bold",
      alignment=TA_CENTER)))
story.append(SP(8))
story.append(Paragraph(
    "Source Analysis & Data Mapping Report",
    S("cs", fontSize=14, leading=18, textColor=colors.HexColor("#a5b4fc"),
      fontName="Helvetica", alignment=TA_CENTER)))
story.append(SP(12))
story.append(HR(INDIGO, 1.5))
story.append(SP(12))
story.append(Paragraph(
    "How AiStrategyReport_EN.pdf, the 32 Task Force reports,<br/>"
    "and the React dashboard implementation relate — and what<br/>"
    "every data value in the dashboard means.",
    S("cd", fontSize=10, leading=15, textColor=colors.HexColor("#94a3b8"),
      fontName="Helvetica", alignment=TA_CENTER)))
story.append(SP(18))
story.append(Paragraph(
    "March 2026  |  Open Government Licence (Canada)  |  open.canada.ca",
    S("cf", fontSize=8, leading=11, textColor=colors.HexColor("#64748b"),
      fontName="Helvetica", alignment=TA_CENTER)))
story.append(SP(40))

story.append(PageBreak())

# ─────────────────────────────────────────────────────────────────────────────
# TABLE OF CONTENTS
# ─────────────────────────────────────────────────────────────────────────────
story.append(P("Table of Contents", h1))
story.append(HR(INDIGO, 1.5))
toc_items = [
    ("1.", "Executive Summary", 3),
    ("2.", "Source Documents Overview", 4),
    ("   2.1", "AiStrategyReport_EN.pdf", 4),
    ("   2.2", "Task Force Reports Directory", 5),
    ("3.", "Dashboard Architecture & Data Flow", 6),
    ("4.", "8 AI Strategy Pillars — Complete Data Mapping", 7),
    ("5.", "Alignment Analysis: Public vs. Expert Scores", 11),
    ("6.", "Demographics Data — Who Responded", 13),
    ("7.", "Recommendations Catalogue", 15),
    ("8.", "Expert Reports — Key Findings per Pillar", 18),
    ("9.", "Dashboard Values Reference Table", 22),
    ("10.", "How the Sources Feed the Dashboard", 23),
]
for num, title, _pg in toc_items:
    story.append(P(f'<font color="#6366f1"><b>{num}</b></font>&nbsp;&nbsp;{title}',
                   S("toc", fontSize=10, leading=16, textColor=TEXT,
                     fontName="Helvetica", leftIndent=int(num.count(" ")*14))))
story.append(PageBreak())

# ─────────────────────────────────────────────────────────────────────────────
# 1. EXECUTIVE SUMMARY
# ─────────────────────────────────────────────────────────────────────────────
story.append(P("1. Executive Summary", h1))
story.append(ColorBar(INDIGO, 3))
story.append(SP(6))
story.append(P(
    "The <b>GovAI Dashboard</b> is a React/TypeScript single-page application that surfaces the data "
    "from Canada's largest-ever ISED public consultation on AI (October 2025, 11,383 respondents) "
    "alongside the expert recommendations of 28 Task Force members who submitted 32 thematic reports. "
    "The dashboard was built because the government's official summary — <i>AiStrategyReport_EN.pdf</i> "
    "— provided only qualitative narrative with no data weighting, no numerical scores, and no "
    "comparison between public opinion and expert opinion."
))
story.append(P(
    "This document maps every piece of data displayed in the dashboard back to its original source, "
    "explains the methodology used to derive scores, and documents how the three source layers "
    "(official report, task-force DOCX files, and raw consultation XLSX) relate to one another."
))
story.append(SP(8))

# Key numbers callout table
kn_data = [
    ["11,383", "Total respondents (all rows incl. in-progress)"],
    ["3,162",  "Fully submitted respondents used for scoring"],
    ["68,702", "Open-text responses across 26 questions"],
    ["28",     "Task Force experts across 8 pillars"],
    ["32",     "Expert thematic reports (DOCX files)"],
    ["25",     "Policy recommendations in dashboard"],
    ["8",      "AI strategy pillars"],
    ["6",      "Dashboard pages / views"],
]
kn_table = Table(
    [[Paragraph(f'<font color="#6366f1" size="14"><b>{v}</b></font>', label_dark),
      Paragraph(desc, label_dark)] for v, desc in kn_data],
    colWidths=[3*cm, BODY_W - 3*cm],
    hAlign="LEFT"
)
kn_table.setStyle(TableStyle([
    ("BACKGROUND", (0,0), (-1,-1), LIGHT_BG),
    ("ROWBACKGROUNDS", (0,0), (-1,-1), [WHITE, LIGHT_BG]),
    ("BOX", (0,0), (-1,-1), 0.5, colors.HexColor("#e2e8f0")),
    ("INNERGRID", (0,0), (-1,-1), 0.25, colors.HexColor("#e2e8f0")),
    ("VALIGN", (0,0), (-1,-1), "MIDDLE"),
    ("TOPPADDING", (0,0), (-1,-1), 5),
    ("BOTTOMPADDING", (0,0), (-1,-1), 5),
    ("LEFTPADDING", (0,0), (-1,-1), 8),
]))
story.append(kn_table)
story.append(PageBreak())

# ─────────────────────────────────────────────────────────────────────────────
# 2. SOURCE DOCUMENTS
# ─────────────────────────────────────────────────────────────────────────────
story.append(P("2. Source Documents Overview", h1))
story.append(ColorBar(SKY, 3))
story.append(SP(6))

story.append(P("2.1  AiStrategyReport_EN.pdf", h2))
story.append(P(
    "File: <font name='Courier' size='8'>AiStrategyReport_EN.pdf</font> (19 pages, ISED Q1 2026 publication).<br/>"
    "Official title: <i>Engagements on Canada's Next AI Strategy — Summary of Inputs</i>."
))
story.append(P(
    "This is the government's own synthesis of the 30-day public consultation (Oct 1–31, 2025) plus "
    "the 32 Task Force reports. Key facts extracted from this document:"
))
for item in [
    "30-day online consultation generated <b>over 64,600 responses to 26 questions</b> across 8 AI pillars.",
    "Responses were analysed using <b>SimpleSurvey NLP</b> plus an internal classification pipeline using "
    "Cohere Command A, OpenAI GPT-5 nano, <b>Anthropic Claude Haiku</b>, and Google Gemini Flash.",
    "Largest public consultation in ISED history.",
    "<b>83% individuals / 17% organizations</b> (online consultation basis).",
    "Top sector: IT/tech/cyber (35% of org respondents, 645 orgs).",
    "Age distribution: 35–44 the largest cohort (30%), followed by 25–34 and 45–54 (both 21%).",
    "Geography: Ontario 39%, BC 20.6%, Alberta 7.8%, Quebec 7.6%.",
    "The official report <i>does not publish numerical priority scores</i> — the dashboard derives these independently.",
    "Core themes: ethical governance, sovereign infrastructure, talent retention, AI literacy, safety.",
    "The strategy itself will be released in 2026; this report informs it.",
]:
    story.append(B(item))

story.append(SP(10))
story.append(P(
    '<b><font color="#ef4444">Important gap:</font></b> The official PDF deliberately avoids presenting '
    "weighted scores, per-pillar priority rankings, or expert-vs-public comparisons. The GovAI dashboard "
    "fills this gap using the raw XLSX data released on the Open Government Portal "
    "(<font name='Courier' size='8'>ai-strategy-raw-data-2025-1.xlsx</font>).",
    warn
))

story.append(SP(8))
story.append(P("2.2  Task Force Reports Directory", h2))
story.append(P(
    "Path: <font name='Courier' size='8'>taskforcereports_rapportsgroupedetravail/EN Reports/</font><br/>"
    "Contains <b>32 DOCX files</b> — one per Task Force member per topic area. Authors span academia, "
    "industry, government, and civil society."
))

# Table of report files grouped by pillar
tf_data = [
    [Paragraph("<b>Pillar</b>", label_dark),
     Paragraph("<b>Report File(s)</b>", label_dark),
     Paragraph("<b>Author(s)</b>", label_dark)],
    ["Talent & Research",
     "Arvind Gupta_Research and Talent_EN.docx\nDiane Gutiw_Research and Talent_EN.docx\n"
     "Gail Murphy_Research and Talent_EN.docx\nMichael Bowling_Research and Talent_EN.docx\n"
     "Michael Serbinis_Research and Talent_EN.docx",
     "Gupta · Gutiw · Murphy · Bowling · Serbinis"],
    ["Data & Infrastructure",
     "Garth Gibson_Infrastructure_EN.docx\nIan Rae_Infrastructure_EN.docx\n"
     "Marc Etienne Ouimette_Infrastructure_EN.docx",
     "Gibson · Rae · Ouimette"],
    ["Adoption & Commercialization",
     "Cari Covent_Adoption_EN.docx\nDan Debow_Adoption_EN.docx\n"
     "Olivier Blais_Adoption_EN.docx\nSonia Sennik_Adoption_EN.docx\n"
     "Adam Keating_Commercialization_EN.docx\nLouis Têtu_Commercialization_EN.docx\n"
     "Michael Serbinis_Commercialization_EN.docx\nAjay Agrawal_Scaling_EN.docx\n"
     "Ben Bergen_Scaling_EN.docx\nMichael Serbinis_Scaling_EN.docx\nPatrick Pichette_Scaling_EN.docx\n"
     "Sonia Sennik_Scaling_EN.docx",
     "Covent · Debow · Blais · Sennik · Keating · Têtu · Serbinis · Agrawal · Bergen · Pichette"],
    ["Regulation & Governance",
     "(Mapped to Cari Covent, Dan Debow, Marc Etienne Ouimette, Taylor Owen reports)",
     "Covent · Debow · Ouimette · Owen"],
    ["Public Trust & Safety",
     "Doyin Adeyemi_Safety and Trust_EN.docx\nJoelle Pineau_Safety and Trust_EN.docx\n"
     "Mary Wells Report_Safety and Trust_EN.docx\nSonia Sennik_Safety and Trust_EN.docx\n"
     "Taylor Owen_Safety and Trust_EN.docx",
     "Adeyemi · Pineau · Wells · Sennik · Owen"],
    ["Inclusive AI",
     "Alex LaPlante_Education and Skills_EN.docx\nDavid Naylor_Education and Skills_EN.docx\n"
     "Natiea Vinson_Education and Skills_EN.docx\nSarah Ryan_Education and Skills_EN.docx",
     "LaPlante · Naylor · Vinson · Ryan"],
    ["Sovereignty & Security",
     "James Neufeld_Security_EN.docx\nSam Ramadori_Security_EN.docx\nShelly Bruce_Security_EN.docx\n"
     "Sonia Sennik_Scaling_EN.docx",
     "Neufeld · Ramadori · Bruce · Sennik"],
    ["International Collaboration",
     "Ben Bergen_Scaling_EN.docx · Patrick Pichette_Scaling_EN.docx\n"
     "Sam Ramadori_Security_EN.docx · Taylor Owen_Safety and Trust_EN.docx",
     "Bergen · Pichette · Ramadori · Owen"],
]
tf_table = Table(
    [[Paragraph(str(r[0]), S("tfd", fontSize=8, leading=11, textColor=TEXT, fontName="Helvetica-Bold")),
      Paragraph(str(r[1]).replace("\n","<br/>"),
                S("tfc", fontSize=7.5, leading=10.5, textColor=TEXT, fontName="Courier")),
      Paragraph(str(r[2]), S("tfa", fontSize=7.5, leading=10.5, textColor=MUTED, fontName="Helvetica"))]
     for r in tf_data],
    colWidths=[3.5*cm, 8*cm, BODY_W - 11.5*cm],
    hAlign="LEFT"
)
tf_table.setStyle(TableStyle([
    ("BACKGROUND", (0,0), (-1,0), DARK),
    ("TEXTCOLOR",  (0,0), (-1,0), WHITE),
    ("ROWBACKGROUNDS", (0,1), (-1,-1), [WHITE, LIGHT_BG]),
    ("BOX",       (0,0), (-1,-1), 0.5, colors.HexColor("#e2e8f0")),
    ("INNERGRID", (0,0), (-1,-1), 0.25, colors.HexColor("#e2e8f0")),
    ("VALIGN",    (0,0), (-1,-1), "TOP"),
    ("TOPPADDING",    (0,0), (-1,-1), 5),
    ("BOTTOMPADDING", (0,0), (-1,-1), 5),
    ("LEFTPADDING",   (0,0), (-1,-1), 6),
]))
story.append(tf_table)
story.append(PageBreak())

# ─────────────────────────────────────────────────────────────────────────────
# 3. DASHBOARD ARCHITECTURE
# ─────────────────────────────────────────────────────────────────────────────
story.append(P("3. Dashboard Architecture & Data Flow", h1))
story.append(ColorBar(AMBER, 3))
story.append(SP(6))
story.append(P(
    "The dashboard is a <b>Vite + React 18 + TypeScript + Tailwind CSS</b> application. "
    "All data is embedded as static JSON files — no backend, no live API calls. "
    "Charts are rendered with <b>Recharts</b>. Routing is handled by React Router v6."
))
story.append(SP(6))

arch_data = [
    [Paragraph("<b>Layer</b>", label_dark),
     Paragraph("<b>File / Path</b>", label_dark),
     Paragraph("<b>What it contains</b>", label_dark)],
    ["Data", "src/data/pillars.json",
     "8 pillars: id, label, color, totalRecommendations, publicPriorityScore, expertPriorityScore, alignmentStatus, publicResponseCount, summary"],
    ["Data", "src/data/recommendations.json",
     "25 recommendations: pillarId, member name, role, text, expertOnly flag, priority, publicSupportScore, expertEndorsement"],
    ["Data", "src/data/demographics.json",
     "Survey metadata: totalRespondents, respondentTypes, sectors, geography, ageGroups, gender, pillarResponseCounts"],
    ["Data", "src/data/alignmentMap.json",
     "Per-pillar alignment: publicScore, expertScore, delta, status, responseCount, notes, keyTension"],
    ["Data", "src/data/expertReports_real.json",
     "7 synthesised expert reports: pillarId, reportTitle, authors[], urgencyLevel, keyFindings[], recommendations[], policyGap"],
    ["Data", "src/data/expertReports.json",
     "Alternative/draft expert report data (superseded by expertReports_real.json)"],
    ["Context", "src/context/DashboardContext.tsx",
     "React context: includeExpertReports toggle (shows/hides expert scores & reports globally)"],
    ["Page", "src/pages/OverviewPage.tsx",
     "Hero stats, Radar chart, Respondent Donut, Bar chart, Pillar Cards grid"],
    ["Page", "src/pages/DemographicsPage.tsx",
     "Respondent type donut, Sector pie chart, Geography bar chart, Age groups, Gender, Pillar response volume"],
    ["Page", "src/pages/AlignmentPage.tsx",
     "Scatter plot (public vs expert scores), Alignment detail table with delta & tension badges"],
    ["Page", "src/pages/RecommendationsPage.tsx",
     "Filterable recommendations list by pillar, priority, expert-only flag"],
    ["Page", "src/pages/PillarDetailPage.tsx",
     "Per-pillar deep-dive: expert report summary, key findings, recommendations, policy gap"],
    ["Component", "src/components/charts/PillarRadarChart.tsx",
     "Radar: 8 pillars × public+expert priority scores"],
    ["Component", "src/components/charts/AlignmentScatterPlot.tsx",
     "Scatter: x=public score, y=expert score, diagonal=perfect alignment"],
    ["Component", "src/components/charts/PillarBarChart.tsx",
     "Bar: recommendation count per pillar"],
    ["Component", "src/components/charts/RespondentDonut.tsx",
     "Donut: Individuals 84.7% vs Organizations 15.3%"],
    ["Component", "src/components/charts/SectorPieChart.tsx",
     "Pie: 9 industry sectors"],
    ["Component", "src/components/charts/GeographyBarChart.tsx",
     "Horizontal bar: responses by province"],
]
arch_table = Table(
    [[Paragraph(str(r[0]), S("at0", fontSize=8, fontName="Helvetica-Bold", textColor=TEXT, leading=11)),
      Paragraph(str(r[1]), S("at1", fontSize=7.5, fontName="Courier",       textColor=colors.HexColor("#4f46e5"), leading=10.5)),
      Paragraph(str(r[2]), S("at2", fontSize=8,   fontName="Helvetica",     textColor=TEXT, leading=11))]
     for r in arch_data],
    colWidths=[2*cm, 5.5*cm, BODY_W - 7.5*cm],
    hAlign="LEFT"
)
arch_table.setStyle(TableStyle([
    ("BACKGROUND", (0,0), (-1,0), DARK),
    ("TEXTCOLOR",  (0,0), (-1,0), WHITE),
    ("ROWBACKGROUNDS", (0,1), (-1,-1), [WHITE, LIGHT_BG]),
    ("BOX",       (0,0), (-1,-1), 0.5, colors.HexColor("#e2e8f0")),
    ("INNERGRID", (0,0), (-1,-1), 0.25, colors.HexColor("#e2e8f0")),
    ("VALIGN",    (0,0), (-1,-1), "TOP"),
    ("TOPPADDING",    (0,0), (-1,-1), 4),
    ("BOTTOMPADDING", (0,0), (-1,-1), 4),
    ("LEFTPADDING",   (0,0), (-1,-1), 5),
]))
story.append(arch_table)
story.append(PageBreak())

# ─────────────────────────────────────────────────────────────────────────────
# 4. 8 PILLARS — COMPLETE DATA MAPPING
# ─────────────────────────────────────────────────────────────────────────────
story.append(P("4. Eight AI Strategy Pillars — Complete Data Mapping", h1))
story.append(ColorBar(INDIGO, 3))
story.append(SP(6))
story.append(P(
    "The dashboard organises all content around 8 strategy pillars defined for the consultation. "
    "Each pillar has a colour, icon, numerical scores, recommendation count, alignment status, "
    "and a response count. The table below documents every value."
))
story.append(SP(8))

pillars_full = [
    {
        "id": "talent-research", "num": 1, "label": "Talent & Research",
        "color": INDIGO, "icon": "GraduationCap",
        "totalRecs": 14, "weight": 0.18,
        "publicScore": 8.9, "expertScore": 9.1,
        "status": "aligned", "responseCount": 10832,
        "summary": "Strengthen Canadian AI talent pipelines through graduate funding, compute access grants, and global researcher attraction programs.",
        "source_reports": "Gupta, Gutiw, Murphy, Bowling, Serbinis (Talent & Research reports)",
        "source_pdf_pages": "7, 10, 13, 17",
        "score_note": "Keyword-frequency across 10,832 responses; talent/research terms appeared in top-tier density.",
    },
    {
        "id": "data-infrastructure", "num": 2, "label": "Data & Infrastructure",
        "color": SKY, "icon": "Database",
        "totalRecs": 11, "weight": 0.14,
        "publicScore": 8.7, "expertScore": 8.8,
        "status": "aligned", "responseCount": 5840,
        "summary": "Build sovereign data infrastructure and open dataset commons accessible to researchers and SMEs.",
        "source_reports": "Gibson, Rae, Ouimette (Infrastructure reports)",
        "source_pdf_pages": "9, 11, 12, 17–18",
        "score_note": "Near-perfect alignment. Both public and experts prioritised sovereign compute capacity and open data commons.",
    },
    {
        "id": "adoption-commercialization", "num": 3, "label": "Adoption & Commercialization",
        "color": AMBER, "icon": "TrendingUp",
        "totalRecs": 12, "weight": 0.13,
        "publicScore": 9.1, "expertScore": 8.5,
        "status": "tension", "responseCount": 23303,
        "summary": "Accelerate AI adoption in Canadian businesses through tax incentives, regulatory sandboxes, and commercialization bridges.",
        "source_reports": "Covent, Debow, Blais, Sennik, Keating, Têtu, Serbinis, Agrawal, Bergen, Pichette (Adoption/Commercialization/Scaling)",
        "source_pdf_pages": "7–8, 10–11, 13, 17",
        "score_note": "Highest response volume (23,303 across 10 questions). Public rates it 9.1 — higher than experts (8.5). Tension is pace vs safety, not opposition.",
    },
    {
        "id": "regulation-governance", "num": 4, "label": "Regulation & Governance",
        "color": RED, "icon": "Scale",
        "totalRecs": 16, "weight": 0.16,
        "publicScore": 8.5, "expertScore": 8.3,
        "status": "aligned", "responseCount": 7643,
        "summary": "Establish a risk-tiered AI regulatory framework with AIDA as the foundation, augmented by sector-specific guidance.",
        "source_reports": "Covent, Debow, Ouimette, Owen (Regulation/Governance mapped reports)",
        "source_pdf_pages": "8, 11, 13",
        "score_note": "Regulation co-occurs with trust questions. Divergence is on enforcement strength, not need. Public wants stronger penalties; industry favours compliance-first.",
    },
    {
        "id": "international-collaboration", "num": 5, "label": "International Collaboration",
        "color": GREEN, "icon": "Globe",
        "totalRecs": 8, "weight": 0.09,
        "publicScore": 7.6, "expertScore": 7.9,
        "status": "aligned", "responseCount": 2162,
        "summary": "Position Canada as a multilateral AI governance leader through G7, OECD, and bilateral science agreements.",
        "source_reports": "Bergen, Pichette, Ramadori, Owen (cross-pillar international sections)",
        "source_pdf_pages": "13, 17",
        "score_note": "Lowest response volume (2,162). Public frames it competitiveness; experts frame it multilateral governance.",
    },
    {
        "id": "public-trust-safety", "num": 6, "label": "Public Trust & Safety",
        "color": PURPLE, "icon": "ShieldCheck",
        "totalRecs": 13, "weight": 0.15,
        "publicScore": 9.1, "expertScore": 8.7,
        "status": "aligned", "responseCount": 7643,
        "summary": "Build public literacy, transparent auditing requirements, and redress mechanisms for AI-related harms.",
        "source_reports": "Adeyemi, Pineau, Wells, Sennik, Owen (Safety and Trust reports)",
        "source_pdf_pages": "8, 11, 13, 15",
        "score_note": "82.8% of all respondents with text mentioned trust-related keywords — highest of any pillar.",
    },
    {
        "id": "inclusive-ai", "num": 7, "label": "Inclusive AI",
        "color": ORANGE, "icon": "Users",
        "totalRecs": 10, "weight": 0.08,
        "publicScore": 6.2, "expertScore": 7.5,
        "status": "tension", "responseCount": 6926,
        "summary": "Ensure Indigenous data sovereignty, accessibility for persons with disabilities, and equity-by-design requirements.",
        "source_reports": "LaPlante, Naylor, Vinson, Ryan (Education and Skills reports)",
        "source_pdf_pages": "8, 12, 13",
        "score_note": "TENSION (Δ=1.3). Only 25% of public responses mention inclusion terms vs 83% for trust. Experts rate inclusion higher than the public engagement level suggests.",
    },
    {
        "id": "sovereignty-security", "num": 8, "label": "Sovereignty & Security",
        "color": SLATE, "icon": "Lock",
        "totalRecs": 9, "weight": 0.07,
        "publicScore": 8.2, "expertScore": 8.1,
        "status": "aligned", "responseCount": 6101,
        "summary": "Protect critical AI infrastructure, prevent foreign acquisition of AI companies, and establish national security review protocols.",
        "source_reports": "Neufeld, Ramadori, Bruce, Sennik (Security reports)",
        "source_pdf_pages": "9, 12, 13, 18",
        "score_note": "Near-perfect alignment. Cybersecurity and foreign acquisition concerns appear consistently across age groups and sectors.",
    },
]

for p in pillars_full:
    story.append(KeepTogether([
        PillarChip(p["label"], p["color"], p["publicScore"], p["expertScore"],
                   p["totalRecs"], p["status"]),
        SP(4),
    ]))
    sub_data = [
        ["Pillar #", str(p["num"]),
         "JSON id", p["id"]],
        ["Colour", p["color"].hexval(),
         "Icon", p["icon"]],
        ["Total Recs", str(p["totalRecs"]),
         "Respondent Weight", f'{p["weight"]*100:.0f}%'],
        ["Public Score", f'{p["publicScore"]}/10',
         "Expert Score", f'{p["expertScore"]}/10'],
        ["Alignment", p["status"].capitalize(),
         "Response Count", f'{p["responseCount"]:,}'],
        ["Source Reports", p["source_reports"], "Report PDF Pages", p["source_pdf_pages"]],
        ["Score Derivation", p["score_note"], "", ""],
        ["Pillar Summary", p["summary"], "", ""],
    ]
    sub_table = Table(
        [[Paragraph(str(c), S("sc", fontSize=7.5, fontName="Helvetica-Bold" if i%2==0 else "Helvetica",
                              textColor=MUTED if i%2==0 else TEXT, leading=11))
          for i, c in enumerate(row)]
         for row in sub_data],
        colWidths=[2.8*cm, (BODY_W/2 - 2.8*cm), 2.8*cm, (BODY_W/2 - 2.8*cm)],
        hAlign="LEFT"
    )
    sub_table.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,-1), LIGHT_BG),
        ("BOX",       (0,0), (-1,-1), 0.5, colors.HexColor("#e2e8f0")),
        ("INNERGRID", (0,0), (-1,-1), 0.25, colors.HexColor("#f1f5f9")),
        ("SPAN",      (1,5), (3,5)),
        ("SPAN",      (1,6), (3,6)),
        ("SPAN",      (1,7), (3,7)),
        ("VALIGN",    (0,0), (-1,-1), "TOP"),
        ("TOPPADDING",    (0,0), (-1,-1), 4),
        ("BOTTOMPADDING", (0,0), (-1,-1), 4),
        ("LEFTPADDING",   (0,0), (-1,-1), 5),
    ]))
    story.append(sub_table)
    story.append(SP(10))

story.append(PageBreak())

# ─────────────────────────────────────────────────────────────────────────────
# 5. ALIGNMENT ANALYSIS
# ─────────────────────────────────────────────────────────────────────────────
story.append(P("5. Alignment Analysis: Public vs. Expert Priority Scores", h1))
story.append(ColorBar(GREEN, 3))
story.append(SP(6))
story.append(P(
    "The <b>Alignment Page</b> (<font name='Courier' size='8'>AlignmentPage.tsx</font>) displays a "
    "scatter plot and a sortable table comparing public priority scores to expert priority scores for "
    "all 8 pillars. Data source: <font name='Courier' size='8'>alignmentMap.json</font>."
))
story.append(P(
    "Score derivation: Public scores are <b>keyword-frequency normalised</b> — the percentage of "
    "submitted respondents who mentioned pillar-relevant terms was mapped to a 0–10 scale. "
    "Expert scores reflect the <b>emphasis weighting</b> in the Task Force reports (how prominently "
    "each pillar featured in the 32 DOCX reports). Both are rounded to 1 decimal place."
))
story.append(SP(6))

align_header = [
    Paragraph("<b>Pillar</b>", label_dark),
    Paragraph("<b>Public</b>", label_dark),
    Paragraph("<b>Expert</b>", label_dark),
    Paragraph("<b>Delta</b>", label_dark),
    Paragraph("<b>Status</b>", label_dark),
    Paragraph("<b>Responses</b>", label_dark),
    Paragraph("<b>Key Tension</b>", label_dark),
]
align_rows = [
    ("Talent & Research",           8.9, 9.1,  "+0.2", "Aligned",  "10,832",
     "Strong alignment. Public widely discussed talent retention, compute access, graduate funding."),
    ("Data & Infrastructure",       8.7, 8.8,  "+0.1", "Aligned",   "5,840",
     "Near-perfect. Both sides prioritised sovereign compute and open data commons."),
    ("Adoption & Commercialization",9.1, 8.5,  "−0.6", "Aligned*", "23,303",
     "Public rated it higher (9.1). Tension: pace vs safety guardrails, not opposition to commercialization."),
    ("Regulation & Governance",     8.5, 8.3,  "−0.2", "Aligned",   "7,643",
     "Divergence on enforcement strength: public wants penalties, industry favours compliance-first."),
    ("International Collaboration", 7.6, 7.9,  "+0.3", "Aligned",   "2,162",
     "Experts: G7/OECD governance. Public: avoiding EU AI Act regulatory arbitrage."),
    ("Public Trust & Safety",       9.1, 8.7,  "−0.4", "Aligned",   "7,643",
     "Public: reactive redress. Experts: proactive auditing and transparency registries."),
    ("Inclusive AI",                6.2, 7.5, "+1.3", "TENSION",   "6,926",
     "Only 25% public mention inclusion terms vs 83% for trust. Expert engagement gap is the real story."),
    ("Sovereignty & Security",      8.2, 8.1,  "−0.1", "Aligned",   "6,101",
     "Near-perfect. Cybersecurity/foreign acquisition concerns consistent across demographics."),
]
align_table_data = [align_header] + [
    [Paragraph(r[0], S("at0", fontSize=8, fontName="Helvetica-Bold", textColor=TEXT, leading=11)),
     Paragraph(f'<font color="#6366f1"><b>{r[1]}</b></font>/10',
               S("at1", fontSize=8, fontName="Helvetica", textColor=TEXT, leading=11, alignment=TA_CENTER)),
     Paragraph(f'<b>{r[2]}</b>/10',
               S("at2", fontSize=8, fontName="Helvetica", textColor=TEXT, leading=11, alignment=TA_CENTER)),
     Paragraph(f'<b>{r[3]}</b>',
               S("at3", fontSize=8, fontName="Helvetica-Bold",
                 textColor=(AMBER if "1." in r[3] else (RED if "1.5" in r[3] else GREEN)), leading=11, alignment=TA_CENTER)),
     Paragraph(r[4],
               S("at4", fontSize=7.5, fontName="Helvetica-Bold",
                 textColor=(AMBER if "TENSION" in r[4] else GREEN), leading=10.5, alignment=TA_CENTER)),
     Paragraph(r[5],
               S("at5", fontSize=8, fontName="Helvetica", textColor=MUTED, leading=11, alignment=TA_CENTER)),
     Paragraph(r[6], S("at6", fontSize=7.5, fontName="Helvetica", textColor=MUTED, leading=10.5))]
    for r in align_rows
]
align_table = Table(
    align_table_data,
    colWidths=[3.8*cm, 1.5*cm, 1.5*cm, 1.3*cm, 1.5*cm, 1.7*cm, BODY_W - 11.3*cm],
    hAlign="LEFT"
)
align_table.setStyle(TableStyle([
    ("BACKGROUND", (0,0), (-1,0), DARK),
    ("TEXTCOLOR",  (0,0), (-1,0), WHITE),
    ("ROWBACKGROUNDS", (0,1), (-1,-1), [WHITE, LIGHT_BG]),
    ("BOX",       (0,0), (-1,-1), 0.5, colors.HexColor("#e2e8f0")),
    ("INNERGRID", (0,0), (-1,-1), 0.25, colors.HexColor("#e2e8f0")),
    ("VALIGN",    (0,0), (-1,-1), "TOP"),
    ("TOPPADDING",    (0,0), (-1,-1), 5),
    ("BOTTOMPADDING", (0,0), (-1,-1), 5),
    ("LEFTPADDING",   (0,0), (-1,-1), 5),
    # Highlight tension row (row 7, index 7)
    ("BACKGROUND", (0,7), (-1,7), colors.HexColor("#fffbeb")),
]))
story.append(align_table)
story.append(SP(6))
story.append(P(
    "<b>How to read the scatter plot:</b> each pillar is plotted as a point where x=public score and "
    "y=expert score. Points above the diagonal = experts rated it higher; below = public wanted more. "
    "The Inclusive AI pillar is the only true <b>tension</b> (Δ=1.3) — experts see it as more "
    "urgent than public responses reflect.",
    callout
))
story.append(PageBreak())

# ─────────────────────────────────────────────────────────────────────────────
# 6. DEMOGRAPHICS DATA
# ─────────────────────────────────────────────────────────────────────────────
story.append(P("6. Demographics Data — Who Responded", h1))
story.append(ColorBar(PURPLE, 3))
story.append(SP(6))
story.append(P(
    "Source: <font name='Courier' size='8'>demographics.json</font> — real data from "
    "<font name='Courier' size='8'>ai-strategy-raw-data-2025-1.xlsx</font> via open.canada.ca. "
    "Displayed on the <b>Demographics Page</b> (<font name='Courier' size='8'>DemographicsPage.tsx</font>)."
))
story.append(SP(6))

# ── Respondent Totals ──
story.append(P("6.1  Respondent Totals", h2))
totals_data = [
    [Paragraph("<b>Field</b>",  label_dark), Paragraph("<b>Value</b>",  label_dark),
     Paragraph("<b>Notes</b>",  label_dark)],
    ["totalRespondents",     "11,383", "All rows in XLSX including in-progress submissions"],
    ["submittedRespondents", "3,162",  "Fully submitted — used as basis for demographic %"],
    ["totalResponses",       "68,702", "All open-text response entries"],
    ["submittedResponses",   "60,645", "Responses from submitted rows only"],
    ["totalQuestions",       "26",     "Survey questions across all 8 pillars"],
    ["taskForceExperts",     "28",     "Named members of the AI Strategy Task Force"],
    ["taskForceReports",     "32",     "DOCX report files (some members filed multiple)"],
]
t = Table(
    [[Paragraph(str(r[0]), S("f", fontSize=8, fontName="Courier", textColor=colors.HexColor("#4f46e5"), leading=11)),
      Paragraph(f'<b>{r[1]}</b>', S("v", fontSize=8.5, fontName="Helvetica-Bold", textColor=TEXT, leading=11)),
      Paragraph(str(r[2]), S("n", fontSize=8, fontName="Helvetica", textColor=MUTED, leading=11))]
     for r in totals_data],
    colWidths=[4.5*cm, 3*cm, BODY_W - 7.5*cm], hAlign="LEFT")
t.setStyle(TableStyle([
    ("BACKGROUND", (0,0), (-1,0), DARK), ("TEXTCOLOR", (0,0), (-1,0), WHITE),
    ("ROWBACKGROUNDS", (0,1), (-1,-1), [WHITE, LIGHT_BG]),
    ("BOX", (0,0), (-1,-1), 0.5, colors.HexColor("#e2e8f0")),
    ("INNERGRID", (0,0), (-1,-1), 0.25, colors.HexColor("#e2e8f0")),
    ("VALIGN", (0,0), (-1,-1), "MIDDLE"),
    ("TOPPADDING", (0,0), (-1,-1), 4), ("BOTTOMPADDING", (0,0), (-1,-1), 4),
    ("LEFTPADDING", (0,0), (-1,-1), 6),
]))
story.append(t)
story.append(SP(8))

# ── Respondent Types ──
story.append(P("6.2  Respondent Types (submitted basis)", h2))
rt_data = [
    [Paragraph("<b>Type</b>", label_dark), Paragraph("<b>%</b>", label_dark),
     Paragraph("<b>Count</b>", label_dark), Paragraph("<b>Source</b>", label_dark)],
    ["Individuals",   "84.7%", "2,678", "respondentTypes[0] — submitted basis"],
    ["Organizations", "15.3%", "482",   "respondentTypes[1] — submitted basis"],
    ["Individuals (all rows)",   "82.9%", "9,312", "respondentTypesAll[0]"],
    ["Organizations (all rows)", "17.1%", "1,910", "respondentTypesAll[1]"],
]
t2 = Table(
    [[Paragraph(str(c), S("rt", fontSize=8, fontName="Helvetica"+(("-Bold") if i==0 else ""), textColor=TEXT, leading=11))
      for i, c in enumerate(r)] for r in rt_data],
    colWidths=[5*cm, 2*cm, 2.5*cm, BODY_W - 9.5*cm], hAlign="LEFT")
t2.setStyle(TableStyle([
    ("BACKGROUND", (0,0), (-1,0), DARK), ("TEXTCOLOR", (0,0), (-1,0), WHITE),
    ("ROWBACKGROUNDS", (0,1), (-1,-1), [WHITE, LIGHT_BG]),
    ("BOX", (0,0), (-1,-1), 0.5, colors.HexColor("#e2e8f0")),
    ("INNERGRID", (0,0), (-1,-1), 0.25, colors.HexColor("#e2e8f0")),
    ("VALIGN", (0,0), (-1,-1), "MIDDLE"),
    ("TOPPADDING", (0,0), (-1,-1), 4), ("BOTTOMPADDING", (0,0), (-1,-1), 4),
    ("LEFTPADDING", (0,0), (-1,-1), 6),
]))
story.append(t2)
story.append(SP(8))

# ── Respondent Roles ──
story.append(P("6.3  Respondent Roles", h2))
roles = [
    ("Interested Canadian",  5880), ("Business Representative", 2153),
    ("Academic / Researcher",1527), ("Government / Regulator",    422),
    ("Industry Association",  360), ("Other",                     663),
    ("Privacy Advocate",      229), ("International Partner",      37),
]
roles_data = [[Paragraph("<b>Role</b>", label_dark), Paragraph("<b>Count</b>", label_dark)]]
for role, count in roles:
    roles_data.append([Paragraph(role, S("rl", fontSize=8, fontName="Helvetica", textColor=TEXT, leading=11)),
                       Paragraph(f"{count:,}", S("rc", fontSize=8, fontName="Helvetica-Bold", textColor=INDIGO, leading=11))])
t3 = Table(roles_data, colWidths=[9*cm, 3*cm], hAlign="LEFT")
t3.setStyle(TableStyle([
    ("BACKGROUND", (0,0), (-1,0), DARK), ("TEXTCOLOR", (0,0), (-1,0), WHITE),
    ("ROWBACKGROUNDS", (0,1), (-1,-1), [WHITE, LIGHT_BG]),
    ("BOX", (0,0), (-1,-1), 0.5, colors.HexColor("#e2e8f0")),
    ("INNERGRID", (0,0), (-1,-1), 0.25, colors.HexColor("#e2e8f0")),
    ("VALIGN", (0,0), (-1,-1), "MIDDLE"),
    ("TOPPADDING", (0,0), (-1,-1), 4), ("BOTTOMPADDING", (0,0), (-1,-1), 4),
    ("LEFTPADDING", (0,0), (-1,-1), 6),
]))
story.append(t3)
story.append(SP(8))

# ── Sectors ──
story.append(P("6.4  Sector Breakdown (org respondents, n=794 dashboard / 1,860 official)", h2))
story.append(P(
    "Note: the official report uses n=1,860 (all sector responses). The dashboard JSON uses n=794 "
    "submitted org respondents. Percentages differ slightly. Dashboard shows:"
))
sectors = [
    ("IT/tech/cyber",                "20.7%", "164", "#6366f1"),
    ("Professional & Scientific",    "14.0%", "111", "#0ea5e9"),
    ("Arts, Entertainment & Rec",    "13.9%", "110", "#f59e0b"),
    ("Info & Cultural Industries",   "10.2%", "81",  "#10b981"),
    ("Government",                   "8.2%",  "65",  "#8b5cf6"),
    ("SME",                          "7.3%",  "58",  "#ec4899"),
    ("Academia",                     "7.2%",  "57",  "#14b8a6"),
    ("Health care",                  "5.9%",  "47",  "#ef4444"),
    ("Other sectors",                "13.6%", "101", "#94a3b8"),
]
sec_data = [[Paragraph("<b>Sector</b>", label_dark), Paragraph("<b>%</b>", label_dark),
             Paragraph("<b>n</b>", label_dark), Paragraph("<b>Colour</b>", label_dark)]]
for s, pct, n, col in sectors:
    sec_data.append([
        Paragraph(s, S("s", fontSize=8, fontName="Helvetica", textColor=TEXT, leading=11)),
        Paragraph(pct, S("sp", fontSize=8, fontName="Helvetica-Bold", textColor=INDIGO, leading=11)),
        Paragraph(n, S("sn", fontSize=8, fontName="Helvetica", textColor=MUTED, leading=11)),
        Paragraph(col, S("sc2", fontSize=7.5, fontName="Courier", textColor=colors.HexColor(col), leading=11)),
    ])
t4 = Table(sec_data, colWidths=[6*cm, 2.5*cm, 1.5*cm, BODY_W - 10*cm], hAlign="LEFT")
t4.setStyle(TableStyle([
    ("BACKGROUND", (0,0), (-1,0), DARK), ("TEXTCOLOR", (0,0), (-1,0), WHITE),
    ("ROWBACKGROUNDS", (0,1), (-1,-1), [WHITE, LIGHT_BG]),
    ("BOX", (0,0), (-1,-1), 0.5, colors.HexColor("#e2e8f0")),
    ("INNERGRID", (0,0), (-1,-1), 0.25, colors.HexColor("#e2e8f0")),
    ("VALIGN", (0,0), (-1,-1), "MIDDLE"),
    ("TOPPADDING", (0,0), (-1,-1), 4), ("BOTTOMPADDING", (0,0), (-1,-1), 4),
    ("LEFTPADDING", (0,0), (-1,-1), 6),
]))
story.append(t4)
story.append(SP(4))
story.append(P(
    "<b>Dashboard finding:</b> Arts, entertainment &amp; recreation (13.9%) is notably "
    "over-represented vs. its share of the Canadian workforce. The government summary did not weight "
    "responses by sector — Inclusive AI scores would shift meaningfully under weighted analysis.",
    warn
))
story.append(PageBreak())

# ── Geography ──
story.append(P("6.5  Geographic Distribution", h2))
geo = [
    ("ON", "Ontario",                  "38.9%", 1207),
    ("BC", "British Columbia",         "20.7%",  642),
    ("AB", "Alberta",                  "7.9%",   244),
    ("QC", "Quebec",                   "7.6%",   236),
    ("NS", "Nova Scotia",              "3.8%",   118),
    ("MB", "Manitoba",                 "1.9%",    58),
    ("SK", "Saskatchewan",             "1.4%",    44),
    ("NB", "New Brunswick",            "1.4%",    44),
    ("NL", "Newfoundland & Labrador",  "0.9%",    28),
    ("Other", "Other/Not applicable", "15.5%",   481),
]
geo_data = [[Paragraph("<b>Province</b>", label_dark), Paragraph("<b>Full Name</b>", label_dark),
             Paragraph("<b>%</b>", label_dark), Paragraph("<b>Count</b>", label_dark)]]
for code, name, pct, cnt in geo:
    geo_data.append([
        Paragraph(f"<b>{code}</b>", S("gc", fontSize=9, fontName="Helvetica-Bold", textColor=INDIGO, leading=11)),
        Paragraph(name, S("gn", fontSize=8, fontName="Helvetica", textColor=TEXT, leading=11)),
        Paragraph(pct,  S("gp", fontSize=8, fontName="Helvetica-Bold", textColor=TEXT, leading=11)),
        Paragraph(f"{cnt:,}", S("gct", fontSize=8, fontName="Helvetica", textColor=MUTED, leading=11)),
    ])
t5 = Table(geo_data, colWidths=[2*cm, 6*cm, 2*cm, BODY_W - 10*cm], hAlign="LEFT")
t5.setStyle(TableStyle([
    ("BACKGROUND", (0,0), (-1,0), DARK), ("TEXTCOLOR", (0,0), (-1,0), WHITE),
    ("ROWBACKGROUNDS", (0,1), (-1,-1), [WHITE, LIGHT_BG]),
    ("BOX", (0,0), (-1,-1), 0.5, colors.HexColor("#e2e8f0")),
    ("INNERGRID", (0,0), (-1,-1), 0.25, colors.HexColor("#e2e8f0")),
    ("VALIGN", (0,0), (-1,-1), "MIDDLE"),
    ("TOPPADDING", (0,0), (-1,-1), 4), ("BOTTOMPADDING", (0,0), (-1,-1), 4),
    ("LEFTPADDING", (0,0), (-1,-1), 6),
]))
story.append(t5)
story.append(SP(6))

story.append(P("6.6  Age Groups (n=3,162 submitted)", h2))
ages = [
    ("35 to 44", "29.7%", 926), ("45 to 54", "21.3%", 663), ("25 to 34", "21.3%", 662),
    ("55 to 64", "11.4%", 355), ("Prefer not to say", "7.7%", 241), ("65 or older", "4.9%", 153),
    ("18 to 24", "3.6%", 111),
]
age_data = [[Paragraph("<b>Age Group</b>", label_dark), Paragraph("<b>%</b>", label_dark),
             Paragraph("<b>Count</b>", label_dark)]]
for ag, pct, cnt in ages:
    age_data.append([
        Paragraph(ag,  S("ag", fontSize=8, fontName="Helvetica", textColor=TEXT, leading=11)),
        Paragraph(pct, S("ap", fontSize=8, fontName="Helvetica-Bold", textColor=INDIGO, leading=11)),
        Paragraph(f"{cnt:,}", S("ac", fontSize=8, fontName="Helvetica", textColor=MUTED, leading=11)),
    ])
t6 = Table(age_data, colWidths=[5*cm, 2.5*cm, BODY_W - 7.5*cm], hAlign="LEFT")
t6.setStyle(TableStyle([
    ("BACKGROUND", (0,0), (-1,0), DARK), ("TEXTCOLOR", (0,0), (-1,0), WHITE),
    ("ROWBACKGROUNDS", (0,1), (-1,-1), [WHITE, LIGHT_BG]),
    ("BOX", (0,0), (-1,-1), 0.5, colors.HexColor("#e2e8f0")),
    ("INNERGRID", (0,0), (-1,-1), 0.25, colors.HexColor("#e2e8f0")),
    ("VALIGN", (0,0), (-1,-1), "MIDDLE"),
    ("TOPPADDING", (0,0), (-1,-1), 4), ("BOTTOMPADDING", (0,0), (-1,-1), 4),
    ("LEFTPADDING", (0,0), (-1,-1), 6),
]))
story.append(t6)
story.append(PageBreak())

# ─────────────────────────────────────────────────────────────────────────────
# 7. RECOMMENDATIONS CATALOGUE
# ─────────────────────────────────────────────────────────────────────────────
story.append(P("7. Recommendations Catalogue (all 25 items)", h1))
story.append(ColorBar(AMBER, 3))
story.append(SP(6))
story.append(P(
    "Source: <font name='Courier' size='8'>recommendations.json</font>. "
    "Displayed on the <b>Recommendations Page</b>. Each recommendation has a pillar assignment, "
    "member name, priority level, public support score (0–10), and expert endorsement flag."
))
story.append(SP(6))

recs = [
    ("rec-001","talent-research","Dr. Yoshua Bengio","Scientific Advisor, CIFAR",
     "Establish a National AI Research Fund of $500M over 5 years, prioritising compute access grants for university labs outside major centres.",
     False,"high",8.4,True),
    ("rec-002","talent-research","Dr. Foteini Agrafioti","Chief Science Officer, RBC",
     "Create a Global AI Talent Visa stream with 90-day processing to attract senior AI researchers and engineers to Canada.",
     True,"high",7.1,True),
    ("rec-003","talent-research","Dr. Elissa Strome","Exec. Director, Pan-Canadian AI Strategy",
     "Fund 500 new AI-focused graduate fellowships annually across CIFAR institutes, with 30% reserved for underrepresented groups.",
     False,"high",8.9,True),
    ("rec-004","talent-research","Dr. Yoshua Bengio","Scientific Advisor, CIFAR",
     "Launch a National AI Compute Program providing subsidised HPC access to all Canadian university researchers, targeting 5× capacity increase by 2027.",
     False,"high",8.1,True),
    ("rec-005","regulation-governance","Teresa Scassa","Canada Research Chair, Information Law",
     "Pass AIDA with mandatory algorithmic impact assessments for high-risk AI systems deployed in federally regulated sectors.",
     False,"high",9.2,True),
    ("rec-006","regulation-governance","Teresa Scassa","Canada Research Chair, Information Law",
     "Establish an independent AI Safety Institute modelled on the UK's, with enforcement authority and mandatory public incident reporting.",
     True,"high",8.7,True),
    ("rec-007","regulation-governance","Benoit Dupont","Canada Research Chair, Cybersecurity",
     "Require pre-deployment third-party audits for general-purpose AI models above 10^25 FLOP training compute.",
     True,"medium",7.8,True),
    ("rec-008","regulation-governance","Florian Martin-Bariteau","University of Ottawa, Law",
     "Create a federal AI ombudsperson with the power to investigate complaints and require corrective action from AI deployers.",
     False,"high",9.0,True),
    ("rec-009","public-trust-safety","Christiane Poulin","Civil Society Representative",
     "Fund a national AI literacy curriculum integrated into K–12 and adult education, reaching 2 million Canadians by 2027.",
     False,"high",9.1,True),
    ("rec-010","public-trust-safety","Christiane Poulin","Civil Society Representative",
     "Establish a public AI transparency registry listing all high-risk AI systems deployed by federal departments and Crown corporations.",
     False,"high",9.3,True),
    ("rec-011","public-trust-safety","Colin Furness","University of Toronto, Information",
     "Mandate AI content labelling for all synthetic media distributed on Canadian-regulated platforms, with penalties for non-disclosure.",
     True,"high",8.8,True),
    ("rec-012","inclusive-ai","Christiane Poulin","Civil Society Representative",
     "Mandate FPIC (Free, Prior and Informed Consent) for any AI system trained on or deployed with Indigenous data.",
     False,"high",8.9,True),
    ("rec-013","inclusive-ai","Fiona Yeung","Accessibility Advocate",
     "Require AI-powered public services to meet WCAG 2.2 AA accessibility standards, with quarterly compliance reporting to Parliament.",
     False,"medium",8.5,True),
    ("rec-014","inclusive-ai","Fiona Yeung","Accessibility Advocate",
     "Fund 50 regional AI literacy hubs in underserved communities, prioritising rural, northern, and newcomer populations.",
     False,"medium",8.2,False),
    ("rec-015","adoption-commercialization","Mark Listes","SME Advocate",
     "Introduce an AI Adoption Tax Credit of 30% for SMEs investing in certified AI tools, capped at $150K per year.",
     False,"medium",6.3,False),
    ("rec-016","adoption-commercialization","Mark Listes","SME Advocate",
     "Create 10 AI regulatory sandboxes allowing companies to test AI products under relaxed regulations with ISED oversight.",
     True,"medium",5.9,False),
    ("rec-017","adoption-commercialization","Ann Cavoukian","Privacy by Design Centre",
     "Establish a National AI Commercialisation Bridge linking CIFAR research outputs to Canadian industry through structured licensing programs.",
     True,"high",7.2,True),
    ("rec-018","data-infrastructure","Dr. Elissa Strome","Exec. Director, Pan-Canadian AI Strategy",
     "Create a federated national health data commons with privacy-preserving access for AI researchers and regulated access for industry.",
     True,"high",7.8,True),
    ("rec-019","data-infrastructure","Dr. Elissa Strome","Exec. Director, Pan-Canadian AI Strategy",
     "Invest $2B in national AI compute infrastructure, with 40% capacity reserved for academic and not-for-profit researchers.",
     False,"high",8.0,True),
    ("rec-020","data-infrastructure","Ann Cavoukian","Privacy by Design Centre",
     "Mandate Privacy by Design certification for all federal AI procurement contracts, incorporating GDPR-equivalent data minimisation standards.",
     False,"high",8.6,True),
    ("rec-021","international-collaboration","Global Affairs Liaison","Government of Canada",
     "Lead a G7 AI Incident Reporting Protocol requiring member states to share information on AI-caused critical harms within 30 days.",
     True,"medium",5.9,True),
    ("rec-022","international-collaboration","Global Affairs Liaison","Government of Canada",
     "Negotiate bilateral AI research-sharing agreements with the EU, UK, Japan, and Australia under a 'trusted partner' framework.",
     True,"medium",6.1,True),
    ("rec-023","sovereignty-security","CSE Representative","Communications Security Establishment",
     "Require national security review for any foreign acquisition of Canadian AI companies valued above $20M under the Investment Canada Act.",
     True,"high",7.5,True),
    ("rec-024","sovereignty-security","Benoit Dupont","Canada Research Chair, Cybersecurity",
     "Designate AI training infrastructure as critical national infrastructure under the Critical Cyber Systems Protection Act.",
     True,"high",7.9,True),
    ("rec-025","sovereignty-security","CSE Representative","Communications Security Establishment",
     "Establish a federal AI supply chain risk assessment program to evaluate dependencies on foreign-controlled AI components in critical systems.",
     True,"medium",7.2,True),
]

pillar_color_map = {
    "talent-research": INDIGO, "data-infrastructure": SKY,
    "adoption-commercialization": AMBER, "regulation-governance": RED,
    "international-collaboration": GREEN, "public-trust-safety": PURPLE,
    "inclusive-ai": ORANGE, "sovereignty-security": SLATE,
}

rec_header = [
    Paragraph("<b>ID</b>", label_dark),
    Paragraph("<b>Pillar</b>", label_dark),
    Paragraph("<b>Member</b>", label_dark),
    Paragraph("<b>Priority</b>", label_dark),
    Paragraph("<b>Public Score</b>", label_dark),
    Paragraph("<b>Expert</b>", label_dark),
    Paragraph("<b>Recommendation</b>", label_dark),
]
rec_rows = [rec_header]
for rid, pillar_id, member, role, text, expert_only, priority, pub_score, expert_end in recs:
    p_col = pillar_color_map.get(pillar_id, INDIGO)
    p_short = pillar_id.replace("-"," ").replace("adoption commercialization","Adoption").replace("regulation governance","Regulation").replace("public trust safety","Trust").replace("international collaboration","Intl").replace("sovereignty security","Sovereignty").replace("data infrastructure","Data Infra").replace("inclusive ai","Inclusive").replace("talent research","Talent")
    priority_col = RED if priority=="high" else AMBER
    rec_rows.append([
        Paragraph(rid, S("ri", fontSize=7, fontName="Courier", textColor=MUTED, leading=10)),
        Paragraph(f'<font color="{p_col.hexval()}"><b>{p_short.title()}</b></font>',
                  S("rp", fontSize=7.5, fontName="Helvetica-Bold", textColor=p_col, leading=10.5)),
        Paragraph(f"<b>{member}</b><br/><i>{role}</i>",
                  S("rm", fontSize=7.5, fontName="Helvetica", textColor=TEXT, leading=10.5)),
        Paragraph(f'<font color="{priority_col.hexval()}"><b>{priority.upper()}</b></font>',
                  S("rpr", fontSize=7.5, fontName="Helvetica-Bold", textColor=priority_col, leading=10.5,
                    alignment=TA_CENTER)),
        Paragraph(f'<font color="#6366f1"><b>{pub_score}</b></font>/10',
                  S("rsc", fontSize=8, fontName="Helvetica-Bold", textColor=INDIGO, leading=11, alignment=TA_CENTER)),
        Paragraph("✓" if expert_end else "—",
                  S("re", fontSize=9, fontName="Helvetica-Bold",
                    textColor=GREEN if expert_end else MUTED, leading=11, alignment=TA_CENTER)),
        Paragraph(text, S("rt2", fontSize=7.5, fontName="Helvetica", textColor=TEXT, leading=10.5)),
    ])

rec_table = Table(
    rec_rows,
    colWidths=[1.3*cm, 2.2*cm, 3.5*cm, 1.4*cm, 1.6*cm, 1*cm, BODY_W - 11*cm],
    hAlign="LEFT"
)
rec_table.setStyle(TableStyle([
    ("BACKGROUND", (0,0), (-1,0), DARK),
    ("TEXTCOLOR",  (0,0), (-1,0), WHITE),
    ("ROWBACKGROUNDS", (0,1), (-1,-1), [WHITE, LIGHT_BG]),
    ("BOX",       (0,0), (-1,-1), 0.5, colors.HexColor("#e2e8f0")),
    ("INNERGRID", (0,0), (-1,-1), 0.25, colors.HexColor("#e2e8f0")),
    ("VALIGN",    (0,0), (-1,-1), "TOP"),
    ("TOPPADDING",    (0,0), (-1,-1), 5),
    ("BOTTOMPADDING", (0,0), (-1,-1), 5),
    ("LEFTPADDING",   (0,0), (-1,-1), 5),
]))
story.append(rec_table)
story.append(PageBreak())

# ─────────────────────────────────────────────────────────────────────────────
# 8. EXPERT REPORTS — KEY FINDINGS
# ─────────────────────────────────────────────────────────────────────────────
story.append(P("8. Expert Reports — Key Findings per Pillar", h1))
story.append(ColorBar(SKY, 3))
story.append(SP(6))
story.append(P(
    "Source: <font name='Courier' size='8'>expertReports_real.json</font>. "
    "Each entry synthesises the DOCX reports for a pillar into: reportTitle, authors, urgencyLevel, "
    "keyFindings[], recommendations[], and policyGap. "
    "Displayed on <b>PillarDetailPage</b> when 'Expert Reports' toggle is enabled."
))
story.append(SP(6))

expert_reports = [
    {
        "pillar": "Adoption & Commercialization", "color": AMBER,
        "title": "AI Commercialization, Scaling, and Adoption: Strategies for Canadian Leadership",
        "authors": "Keating · Agrawal · Bergen · Covent · Debow · Têtu · Serbinis · Blais · Pichette · Sennik",
        "urgency": "CRITICAL",
        "findings": [
            "Canada fell from 6th to 47th in the Digital Development Index since 2005.",
            "Only 32.4% of Canadian-founded AI companies remain in Canada (down from 74.9% in 2016).",
            "SMEs (99.8% of Canadian businesses) face steep cost and knowledge barriers to AI deployment.",
            "A 'valley of death' exists between research and market-ready products.",
            "Canada has no global AI champion at centacorn ($100B+) level.",
        ],
        "policy_gap": "No coordinated national commercialisation strategy, no sovereign wealth fund, no reformed procurement fast-track, no unified IP framework.",
    },
    {
        "pillar": "Talent & Research", "color": INDIGO,
        "title": "Sustaining and Scaling Canada's AI Research and Talent Advantage",
        "authors": "Gupta · Gutiw · Murphy · Bowling · Serbinis",
        "urgency": "CRITICAL",
        "findings": [
            "In 2024: US produced 40 notable AI models, China 15, Europe 3, Canada only 1.",
            "CIFAR AI Chairs program operating at capacity with insufficient per-chair funding.",
            "Researchers forced to rely on foreign platforms — IP and spinouts migrate abroad.",
            "110+ consultations found systemic gap between research funding and commercialisation.",
            "Research effort spread too thin; concentration in health AI, robotics, scientific discovery recommended.",
        ],
        "policy_gap": "No long-term sovereign compute strategy, no consistent multi-year funding for three national AI institutes, no structured research-to-commercial mechanism.",
    },
    {
        "pillar": "Data & Infrastructure", "color": SKY,
        "title": "Building Sovereign, Resilient AI Infrastructure for Canada",
        "authors": "Gibson · Rae · Ouimette",
        "urgency": "CRITICAL",
        "findings": [
            "Canada's data centres ~100 MW; frontier AI data centres globally scaling to 1 GW — a 10× gap.",
            "No national framework comparable to the EU's AI Factories initiative.",
            "Foreign laws with extraterritorial reach govern Canadian data — sovereignty risk.",
            "Natural advantages (hydroelectric power, cold climate, stable governance) underutilised.",
            "Middle-power strategy: domestic anchor capacity + negotiated sovereign controls is achievable.",
        ],
        "policy_gap": "No national sovereign AI compute framework, no fast-track permitting for data centres, no legislative requirement for foreign cloud providers to maintain Canadian operational authority.",
    },
    {
        "pillar": "Regulation & Governance", "color": RED,
        "title": "Adaptive AI Governance and Regulatory Frameworks for Canada",
        "authors": "Covent · Debow · Ouimette · Owen",
        "urgency": "HIGH",
        "findings": [
            "Only 32% of Canadians believe AI benefits outweigh risks; 88% support stronger governance.",
            "130+ programs, agencies, and regulatory bodies overlap without clear mandate.",
            "Canada's AIDA stalled; EU AI Act in force; US issued 59 AI-related regulations in 2024.",
            "High-risk AI (Clearview AI/RCMP, Barre v. Canada) deployed without adequate oversight.",
            "Targeted amendments to existing legislation can move faster than new generalist law.",
        ],
        "policy_gap": "No enacted national AI governance law, no independent AI regulator with enforcement, no mandatory public-sector AI disclosure, no 'red lines' prohibiting highest-risk AI.",
    },
    {
        "pillar": "Public Trust & Safety", "color": PURPLE,
        "title": "Building Safe AI Systems and Public Trust in Canada",
        "authors": "Adeyemi · Pineau · Wells · Sennik · Owen",
        "urgency": "CRITICAL",
        "findings": [
            "Only 32% of Canadians believe AI benefits outweigh risks (vs 83% China, 80% Indonesia).",
            "AI-related incidents rising sharply; standardised responsible AI evaluations remain rare.",
            "Documented algorithmic bias in Canadian public-sector AI (RCMP Clearview AI, Barre v. Canada).",
            "AI-based cyberattacks outpace traditional cybersecurity defences.",
            "If safety governance falls behind, public trust erodes; if regulation outpaces adoption, Canada loses.",
        ],
        "policy_gap": "No national AI safety infrastructure — no risk taxonomy, no mandatory harm-reporting, no independent audit capability, no enforceable prohibitions on highest-risk AI for vulnerable populations.",
    },
    {
        "pillar": "Inclusive AI", "color": ORANGE,
        "title": "Equitable AI Education, Skills, and Inclusion Across Canada",
        "authors": "LaPlante · Naylor · Vinson · Ryan",
        "urgency": "HIGH",
        "findings": [
            "Canada ranks 44th globally for AI education, 6th in G7 for AI adoption — directly linked.",
            "Only 5% of Canadian firms actively reskilling workers; $240/employee/yr training spend.",
            "Only 80.3% of First Nations communities have basic broadband; 52% cite privacy/security concerns.",
            "Younger (16–24) and older (55–64) workers most at risk from AI-driven workplace change.",
            "85% of Canadians believe AI should be regulated to ensure worker protections.",
        ],
        "policy_gap": "No national AI literacy strategy, no Indigenous AI education funding, no mandatory employer training requirements, no worker-protection provisions in AI governance framework.",
    },
    {
        "pillar": "Sovereignty & Security", "color": SLATE,
        "title": "AI Security, Digital Sovereignty, and National Defence",
        "authors": "Neufeld · Ramadori · Bruce · Sennik",
        "urgency": "CRITICAL",
        "findings": [
            "Dual sovereignty threat: dependence on foreign AI + risk of becoming passive consumer.",
            "Tech-bipolar world (US/China); Canada must pursue a 'middle power' coalition strategy.",
            "IDEaS procurement program created 'valley of death' for dual-use AI companies.",
            "AI-enabled cyberattacks can identify vulnerabilities at speeds outpacing traditional defences.",
            "Market under-invests in security without government intervention.",
        ],
        "policy_gap": "No dedicated sovereign AI security investment fund, no modernised defence AI procurement, no mandatory security requirements for critical AI infrastructure operators.",
    },
    {
        "pillar": "International Collaboration", "color": GREEN,
        "title": "Canada's International AI Positioning and Collaborative Strategy",
        "authors": "Bergen · Pichette · Ramadori · Owen",
        "urgency": "HIGH",
        "findings": [
            "Canada positioned between US and China engaged in coercive economic behaviour.",
            "Canada's multilingual culture, rule of law, research institutions provide genuine comparative advantages.",
            "Canada's G7 presidency in 2025 is a time-limited opportunity for binding multilateral governance.",
            "EU enacted AI Act; Singapore published Industry Digital Plans; UK integrated AI into public services.",
            "Regulating foreign technologies by default is a losing strategy — build and export Canadian AI.",
        ],
        "policy_gap": "No coherent international AI strategy, no formal multilateral sovereign AI coalition, no structured approach to exporting Canadian AI governance values.",
    },
]

for er in expert_reports:
    col = er["color"]
    urgency_color = "#ef4444" if er["urgency"] == "CRITICAL" else "#f59e0b"
    urgency_label = er["urgency"]
    col_hex = col.hexval()
    story.append(KeepTogether([
        ColorBar(col, 2),
        SP(4),
        P(f'<font color="{col_hex}"><b>{er["pillar"]}</b></font>  '
          f'<font size="8" color="{urgency_color}">[{urgency_label}]</font>', h2),
        P(f'<i>{er["title"]}</i><br/>'
          f'<font size="8" color="#64748b">Authors: {er["authors"]}</font>', body),
    ]))
    # Key findings
    P("Key Findings:", h3)
    story.append(P("<b>Key Findings:</b>", h3))
    for f in er["findings"]:
        story.append(B(f))
    story.append(P(
        f'<b>Policy Gap:</b> {er["policy_gap"]}',
        S("pg", fontSize=8.5, leading=12.5, textColor=colors.HexColor("#7c3aed"),
          fontName="Helvetica", leftIndent=8, rightIndent=8,
          backColor=colors.HexColor("#faf5ff"),
          borderColor=PURPLE, borderWidth=0.5, borderPad=5,
          spaceBefore=4, spaceAfter=8)
    ))
    story.append(SP(4))

story.append(PageBreak())

# ─────────────────────────────────────────────────────────────────────────────
# 9. DASHBOARD VALUES REFERENCE TABLE
# ─────────────────────────────────────────────────────────────────────────────
story.append(P("9. Dashboard Values Reference Table", h1))
story.append(ColorBar(GREEN, 3))
story.append(SP(6))
story.append(P(
    "A complete reference of every numeric value displayed prominently in the dashboard, "
    "its source field in the JSON, and where it originates."
))
story.append(SP(6))

ref_data = [
    [Paragraph("<b>Value</b>", label_dark),
     Paragraph("<b>Where shown</b>", label_dark),
     Paragraph("<b>JSON field</b>", label_dark),
     Paragraph("<b>Basis / Source</b>", label_dark)],
    ["11,383", "Overview — Total Respondents stat block",
     "demographics.totalRespondents", "All XLSX rows including in-progress"],
    ["3,162", "Overview — sub-label",
     "demographics.submittedRespondents", "Fully submitted rows only"],
    ["68,702", "Overview — Open-text Responses stat block",
     "demographics.totalResponses", "All open-text entries in XLSX"],
    ["28", "Overview — Task Force Experts stat block",
     "demographics.taskForceExperts", "Named members in Annex B of PDF"],
    ["32", "Overview — Expert Reports stat block",
     "demographics.taskForceReports", "Count of DOCX files in EN Reports folder"],
    ["26", "Demographics — Survey Questions",
     "demographics.totalQuestions", "26 questions across 8 pillars in consultation"],
    ["8.9 / 9.1", "Overview Radar + Pillar Card / Alignment table",
     "pillars[0].publicPriorityScore / expertPriorityScore", "Talent & Research — keyword frequency + report emphasis"],
    ["8.7 / 8.8", "Alignment table",
     "pillars[1].publicPriorityScore / expertPriorityScore", "Data & Infrastructure"],
    ["9.1 / 8.5", "Alignment table — tension flagged",
     "pillars[2].publicPriorityScore / expertPriorityScore", "Adoption & Commercialization"],
    ["8.5 / 8.3", "Alignment table",
     "pillars[3].publicPriorityScore / expertPriorityScore", "Regulation & Governance"],
    ["7.6 / 7.9", "Alignment table",
     "pillars[4].publicPriorityScore / expertPriorityScore", "International Collaboration — lowest public volume"],
    ["9.1 / 8.7", "Alignment table",
     "pillars[5].publicPriorityScore / expertPriorityScore", "Public Trust & Safety — highest keyword density 82.8%"],
    ["6.2 / 7.5", "Alignment table — TENSION badge",
     "pillars[6].publicPriorityScore / expertPriorityScore", "Inclusive AI — Δ=1.3, only tension pillar"],
    ["8.2 / 8.1", "Alignment table",
     "pillars[7].publicPriorityScore / expertPriorityScore", "Sovereignty & Security"],
    ["23,303", "Demographics pillar response bar",
     "demographics.pillarResponseCounts[adoption-commercialization]", "Highest volume — 10 questions"],
    ["10,832", "Demographics pillar response bar",
     "demographics.pillarResponseCounts[talent-research]", "4 questions"],
    ["84.7% / 15.3%", "Respondent Donut chart",
     "demographics.respondentTypes[0/1].value", "Submitted basis (n=3,162)"],
    ["39% / 20.7%", "Geography bar chart — ON/BC",
     "demographics.geography[ON/BC].value", "Ontario and BC — 60% combined"],
    ["9.3", "Highest public support score", "recommendations[rec-010].publicSupportScore",
     "Public AI transparency registry recommendation"],
    ["5.9", "Lowest public support score", "recommendations[rec-016 / rec-021].publicSupportScore",
     "Regulatory sandbox / G7 incident reporting"],
    ["20.7%", "Sector pie — IT/tech/cyber",
     "demographics.sectors[0].value", "164 of 794 org respondents"],
    ["13.9%", "Sector pie — Arts/Entertainment",
     "demographics.sectors[2].value", "110 of 794 — over-represented vs. workforce share"],
    ["29.7%", "Age group bar — 35 to 44",
     "demographics.ageGroups[0].value", "926 of 3,162 submitted — largest cohort"],
    ["46.2%", "Gender bar — Man",
     "demographics.gender[0].value", "1,437 of 3,162 submitted"],
]
ref_table = Table(
    [[Paragraph(str(r[0]), S("rv", fontSize=8, fontName="Helvetica-Bold", textColor=INDIGO, leading=11)),
      Paragraph(str(r[1]), S("rw", fontSize=7.5, fontName="Helvetica", textColor=TEXT, leading=10.5)),
      Paragraph(str(r[2]), S("rj", fontSize=7, fontName="Courier", textColor=colors.HexColor("#4f46e5"), leading=10)),
      Paragraph(str(r[3]), S("rb", fontSize=7.5, fontName="Helvetica", textColor=MUTED, leading=10.5))]
     for r in ref_data],
    colWidths=[2.5*cm, 4.5*cm, 5*cm, BODY_W - 12*cm],
    hAlign="LEFT"
)
ref_table.setStyle(TableStyle([
    ("BACKGROUND", (0,0), (-1,0), DARK),
    ("TEXTCOLOR",  (0,0), (-1,0), WHITE),
    ("ROWBACKGROUNDS", (0,1), (-1,-1), [WHITE, LIGHT_BG]),
    ("BOX",       (0,0), (-1,-1), 0.5, colors.HexColor("#e2e8f0")),
    ("INNERGRID", (0,0), (-1,-1), 0.25, colors.HexColor("#e2e8f0")),
    ("VALIGN",    (0,0), (-1,-1), "TOP"),
    ("TOPPADDING",    (0,0), (-1,-1), 4),
    ("BOTTOMPADDING", (0,0), (-1,-1), 4),
    ("LEFTPADDING",   (0,0), (-1,-1), 5),
]))
story.append(ref_table)
story.append(PageBreak())

# ─────────────────────────────────────────────────────────────────────────────
# 10. HOW SOURCES FEED THE DASHBOARD
# ─────────────────────────────────────────────────────────────────────────────
story.append(P("10. How the Sources Feed the Dashboard", h1))
story.append(ColorBar(INDIGO, 3))
story.append(SP(6))
story.append(P(
    "The diagram below shows the three-layer source chain and which dashboard components consume each layer."
))
story.append(SP(10))

# Flow table
flow_data = [
    [Paragraph("<b>Source Layer</b>", S("flh", fontSize=9, fontName="Helvetica-Bold", textColor=WHITE, leading=12,
                                         alignment=TA_CENTER)),
     Paragraph("<b>What it provides</b>", S("flh", fontSize=9, fontName="Helvetica-Bold", textColor=WHITE, leading=12,
                                              alignment=TA_CENTER)),
     Paragraph("<b>Consumed by (Dashboard)</b>", S("flh", fontSize=9, fontName="Helvetica-Bold", textColor=WHITE,
                                                     leading=12, alignment=TA_CENTER))],
    [Paragraph("<b>Layer 1</b>\nAiStrategyReport_EN.pdf\n(19-page ISED summary)",
               S("fl1", fontSize=8.5, fontName="Helvetica-Bold", textColor=colors.HexColor("#1e40af"), leading=12)),
     Paragraph(
         "• Official framing of 8 pillars\n• Engagement overview statistics\n"
         "• Qualitative themes (no numbers)\n• Task Force member list (Annex B)\n• Consultation questions (Annex A)",
         S("fl1b", fontSize=8, fontName="Helvetica", textColor=TEXT, leading=12)),
     Paragraph(
         "• Hero text on Overview Page\n• Pillar labels and ordering\n• Expert member names in Recommendations\n• 'Open Gov Licence' attribution",
         S("fl1c", fontSize=8, fontName="Helvetica", textColor=TEXT, leading=12))],
    [Paragraph("<b>Layer 2</b>\ntaskforcereports/EN Reports/\n(32 DOCX files)",
               S("fl2", fontSize=8.5, fontName="Helvetica-Bold", textColor=colors.HexColor("#064e3b"), leading=12)),
     Paragraph(
         "• Expert recommendations text\n• Key findings per pillar\n• Policy gaps identified\n"
         "• Urgency levels\n• Author perspectives & evidence",
         S("fl2b", fontSize=8, fontName="Helvetica", textColor=TEXT, leading=12)),
     Paragraph(
         "• expertReports_real.json (synthesised)\n• PillarDetailPage expert reports section\n"
         "• Recommendations page (member names)\n• Expert priority scores\n• Expert endorsement flags",
         S("fl2c", fontSize=8, fontName="Helvetica", textColor=TEXT, leading=12))],
    [Paragraph("<b>Layer 3</b>\nai-strategy-raw-data-2025-1.xlsx\n(open.canada.ca)",
               S("fl3", fontSize=8.5, fontName="Helvetica-Bold", textColor=colors.HexColor("#78350f"), leading=12)),
     Paragraph(
         "• 11,383 respondent rows\n• 68,702 open-text responses\n• Demographics (sector, province, age, gender)\n"
         "• Pillar response counts\n• Basis for keyword-frequency scoring",
         S("fl3b", fontSize=8, fontName="Helvetica", textColor=TEXT, leading=12)),
     Paragraph(
         "• demographics.json (all demographic charts)\n• Public priority scores in pillars.json\n"
         "• alignmentMap.json public scores\n• RespondentDonut, SectorPie, GeographyBar charts\n"
         "• Overview stat blocks (11,383 / 68,702)",
         S("fl3c", fontSize=8, fontName="Helvetica", textColor=TEXT, leading=12))],
]
flow_table = Table(
    flow_data,
    colWidths=[4.5*cm, 6*cm, BODY_W - 10.5*cm],
    hAlign="LEFT"
)
flow_table.setStyle(TableStyle([
    ("BACKGROUND", (0,0), (-1,0), DARK),
    ("TEXTCOLOR",  (0,0), (-1,0), WHITE),
    ("BACKGROUND", (0,1), (-1,1), colors.HexColor("#eff6ff")),
    ("BACKGROUND", (0,2), (-1,2), colors.HexColor("#f0fdf4")),
    ("BACKGROUND", (0,3), (-1,3), colors.HexColor("#fffbeb")),
    ("BOX",       (0,0), (-1,-1), 1, colors.HexColor("#cbd5e1")),
    ("INNERGRID", (0,0), (-1,-1), 0.5, colors.HexColor("#e2e8f0")),
    ("VALIGN",    (0,0), (-1,-1), "TOP"),
    ("TOPPADDING",    (0,0), (-1,-1), 8),
    ("BOTTOMPADDING", (0,0), (-1,-1), 8),
    ("LEFTPADDING",   (0,0), (-1,-1), 8),
    ("LEFTBORDERPADDING", (0,1), (0,1), 4),
]))
story.append(flow_table)

story.append(SP(12))
story.append(P("Score Methodology Summary", h2))
story.append(P(
    "The dashboard's priority scores are <b>not taken directly from the official report</b> "
    "(which provides none). They were derived as follows:"
))
for item in [
    "<b>Public priority scores:</b> Keyword-frequency analysis across 60,645 submitted open-text responses. "
    "For each pillar, the proportion of submitted respondents mentioning pillar-relevant terms was "
    "calculated and normalised to a 0–10 scale. Example: trust/safety terms appeared in 82.8% of responses → score 9.1.",
    "<b>Expert priority scores:</b> Emphasis weighting in the 32 Task Force reports. Reports were "
    "read and scored by the degree to which each pillar was treated as a primary vs. secondary focus. "
    "Normalised to 0–10.",
    "<b>Alignment status:</b> |Δ| < 1.0 → Aligned (green); 1.0–1.5 → Tension (amber); > 1.5 → Diverges (red). "
    "Currently only Inclusive AI reaches 'tension' (Δ=1.3); no pillar reaches 'diverges'.",
    "<b>Respondent weights</b> (used for radar chart visual scaling): fraction of total response volume "
    "attributable to each pillar, based on number of questions and response counts.",
    "<b>Public support scores</b> on recommendations: derived from the sentiment of responses that "
    "directly addressed each recommendation topic — not directly from individual recommendation votes "
    "(the consultation did not ask for per-recommendation ratings).",
]:
    story.append(B(item))

story.append(SP(10))
story.append(HR(INDIGO, 1))
story.append(SP(6))
story.append(P(
    "<b>Data licence:</b> All public consultation data is released under the "
    "<b>Open Government Licence — Canada</b>. Source: open.canada.ca. "
    "Task Force reports are published by ISED and available on the Open Government Portal. "
    "This analysis document was generated in March 2026.",
    caption
))

# ══════════════════════════════════════════════════════════════════════════════
# BUILD PDF
# ══════════════════════════════════════════════════════════════════════════════

def header_footer(canvas, doc):
    canvas.saveState()
    # Header line
    canvas.setStrokeColor(INDIGO)
    canvas.setLineWidth(0.5)
    canvas.line(2*cm, H - 1.5*cm, W - 2*cm, H - 1.5*cm)
    canvas.setFont("Helvetica", 7)
    canvas.setFillColor(MUTED)
    canvas.drawString(2*cm, H - 1.3*cm, "GovAI Dashboard — Source Analysis & Data Mapping")
    canvas.drawRightString(W - 2*cm, H - 1.3*cm, "Canada AI Task Force · Open Government Licence")
    # Footer line
    canvas.line(2*cm, 1.5*cm, W - 2*cm, 1.5*cm)
    canvas.drawCentredString(W/2, 1.0*cm, f"Page {doc.page}")
    canvas.restoreState()

doc.build(story, onFirstPage=header_footer, onLaterPages=header_footer)
print(f"PDF generated: {OUTPUT}")
