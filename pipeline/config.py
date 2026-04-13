"""
Pipeline configuration — paths, constants, and mappings.
"""
import os
from pathlib import Path

# ── Paths ──────────────────────────────────────────────────────────────────
ROOT = Path(__file__).parent.parent
PIPELINE_DIR = Path(__file__).parent
XLSX_PATH = Path(os.environ.get("XLSX_PATH", "/home/abhishekujale/Downloads/ai-strategy-raw-data-2025-1.xlsx"))
REPORTS_DIR = ROOT / "taskforcereports_rapportsgroupedetravail" / "EN Reports"
DB_PATH = PIPELINE_DIR / "chunks.db"
EXPORT_DIR = ROOT / "src" / "data"

# ── Anthropic models ────────────────────────────────────────────────────────
MODEL_PUBLIC = "claude-haiku-4-5-20251001"   # cheaper; public XLSX chunks
MODEL_EXPERT = "claude-sonnet-4-6"           # higher quality; expert chunks
MODEL_CANON  = "claude-sonnet-4-6"           # canonicalization pass

# ── XLSX column → pillar mapping ────────────────────────────────────────────
# Columns 27–52 are the 26 open-text consultation questions.
QUESTION_MAP: dict[int, str] = {
    # Pillar 1 — Talent & Research (4 questions)
    27: "talent-research",
    28: "talent-research",
    29: "talent-research",
    30: "talent-research",
    # Pillar 3 — Adoption & Commercialization (10 questions)
    31: "adoption-commercialization",
    32: "adoption-commercialization",
    33: "adoption-commercialization",
    34: "adoption-commercialization",
    35: "adoption-commercialization",
    36: "adoption-commercialization",
    37: "adoption-commercialization",
    38: "adoption-commercialization",
    39: "adoption-commercialization",
    40: "adoption-commercialization",
    # Pillar 6 — Public Trust & Safety (2 questions)
    41: "public-trust-safety",
    43: "public-trust-safety",
    # Pillar 4 — Regulation & Governance (1 question)
    42: "regulation-governance",
    # Pillar 7 — Inclusive AI / Workforce (3 questions)
    44: "inclusive-ai",
    45: "inclusive-ai",
    46: "inclusive-ai",
    # Pillar 2 — Data & Infrastructure (3 questions)
    47: "data-infrastructure",
    48: "data-infrastructure",
    49: "data-infrastructure",
    # Pillar 8 — Sovereignty & Security (3 questions)
    50: "sovereignty-security",
    51: "sovereignty-security",
    52: "sovereignty-security",
}

# XLSX column → question text (for context in LLM prompts)
QUESTION_TEXTS: dict[int, str] = {
    27: "How does Canada retain and grow its AI research edge? What are the promising areas that Canada should lean in on, where it can lead the world?",
    28: "How can Canada strengthen coordination across academia, industry, government and defence to accelerate impactful AI research?",
    29: "What conditions are needed to ensure Canadian AI research remains globally competitive and ethically grounded?",
    30: "What efforts are needed to attract, develop and retain top AI talent across research, industry and the public sector?",
    31: "Where is the greatest potential for impactful AI adoption in Canada? How can we ensure those sectors with the greatest opportunity can take advantage?",
    32: "What are the key barriers to AI adoption, and how can government and industry work together to accelerate responsible uptake?",
    33: "How will we know if Canada is meaningfully engaging with and adopting AI? What are the best measures of success?",
    34: "What needs to be put in place so Canada can grow globally competitive AI companies while retaining ownership, IP and economic sovereignty?",
    35: "What changes to the Canadian business enabling environment are needed to unlock AI commercialization?",
    36: "How can Canada better connect AI research with commercialization to meet strategic business needs?",
    37: "How does Canada get to more and stronger AI industrial champions? What supports would make our champions own the podium?",
    38: "What changes to Canada's landscape of business incentives would accelerate sustainable scaling of AI ventures?",
    39: "How can we best support AI companies to remain rooted in Canada while growing strength in global markets?",
    40: "What lessons can we learn from countries that are successful at investment attraction in AI and tech, both from domestic sources and from foreign capital?",
    41: "How can Canada build public trust in AI technologies while addressing the risks they present? What are the most important things to do to build confidence?",
    42: "What frameworks, standards, regulations and norms are needed to ensure AI products in Canada are trustworthy and responsibly deployed?",
    43: "How can Canada proactively engage citizens and businesses to promote responsible AI use and trust in its governance? Who is best placed to lead which efforts that fuel trust?",
    44: "What skills are required for a modern, digital economy, and how can Canada best support their development and deployment in the workforce?",
    45: "How can we enhance AI literacy in Canada, including awareness of AI's limitations and biases?",
    46: "What can Canada do to ensure equitable access to AI literacy across regions, demographics and socioeconomic groups?",
    47: "Which infrastructure gaps (compute, data, connectivity) are holding back AI innovation in Canada, and what is stopping Canadian firms from building sovereign infrastructure to address them?",
    48: "How can we ensure equitable access to AI infrastructure across regions, sectors and users (researchers, start-ups, SMEs)?",
    49: "How much sovereign AI compute capacity will we need for our security and growth, and in what formats?",
    50: "What are the emerging security risks associated with AI, and how can Canada proactively mitigate future threats?",
    51: "How can Canada strengthen cybersecurity and safeguard critical infrastructure, data and models in the age of AI?",
    52: "Where can AI better position Canada's protection and defence? What will be required to have a strong AI defensive posture?",
}

# Expert report filename → (pillar_id, expert_name, affiliation)
REPORT_MAP: dict[str, tuple[str, str, str]] = {
    "Adam Keating_Commercialization_EN.docx":        ("adoption-commercialization", "Adam Keating",        ""),
    "Ajay Agrawal_Scaling_EN.docx":                  ("adoption-commercialization", "Ajay Agrawal",         "University of Toronto"),
    "Alex LaPlante_Education and Skills_EN.docx":    ("inclusive-ai",               "Alex LaPlante",        ""),
    "Arvind Gupta_Research and Talent_EN.docx":      ("talent-research",            "Arvind Gupta",         "University of British Columbia"),
    "Ben Bergen_Scaling_EN.docx":                    ("adoption-commercialization", "Ben Bergen",           "Council of Canadian Innovators"),
    "Cari Covent_Adoption_EN.docx":                  ("adoption-commercialization", "Cari Covent",          ""),
    "Dan Debow_Adoption_EN.docx":                    ("adoption-commercialization", "Dan Debow",            ""),
    "David Naylor_Education and Skills_EN.docx":     ("inclusive-ai",               "David Naylor",         "University of Toronto"),
    "Diane Gutiw_Research and Talent_EN.docx":       ("talent-research",            "Diane Gutiw",          ""),
    "Doyin Adeyemi_Safety and Trust_EN.docx":        ("public-trust-safety",        "Doyin Adeyemi",        ""),
    "Gail Murphy_Research and Talent_EN.docx":       ("talent-research",            "Gail Murphy",          "University of British Columbia"),
    "Garth Gibson_Infrastructure_EN.docx":           ("data-infrastructure",        "Garth Gibson",         ""),
    "Ian Rae_Infrastructure_EN.docx":                ("data-infrastructure",        "Ian Rae",              "Google Cloud Canada"),
    "James Neufeld_Security_EN.docx":                ("sovereignty-security",       "James Neufeld",        ""),
    "Joelle Pineau_Safety and Trust_EN.docx":        ("public-trust-safety",        "Joelle Pineau",        "Meta AI / McGill University"),
    "Louis Têtu_Commercialization_EN.docx":          ("adoption-commercialization", "Louis Têtu",           "Coveo"),
    "Marc Etienne Ouimette_Infrastructure_EN.docx":  ("data-infrastructure",        "Marc Etienne Ouimette",""),
    "Mary Wells Report_Safety and Trust_EN.docx":    ("public-trust-safety",        "Mary Wells",           "University of Waterloo"),
    "Michael Bowling_Research and Talent_EN.docx":   ("talent-research",            "Michael Bowling",      "University of Alberta"),
    "Michael Serbinis_Commercialization_EN.docx":    ("adoption-commercialization", "Michael Serbinis",     ""),
    "Michael Serbinis_Research and Talent_EN.docx":  ("talent-research",            "Michael Serbinis",     ""),
    "Michael Serbinis_Scaling_EN.docx":              ("adoption-commercialization", "Michael Serbinis",     ""),
    "Natiea Vinson_Education and Skills_EN.docx":    ("inclusive-ai",               "Natiea Vinson",        ""),
    "Olivier Blais_Adoption_EN.docx":                ("adoption-commercialization", "Olivier Blais",        "Moov AI"),
    "Patrick Pichette_Scaling_EN.docx":              ("adoption-commercialization", "Patrick Pichette",     "iNovia Capital"),
    "Sam Ramadori_Security_EN.docx":                 ("sovereignty-security",       "Sam Ramadori",         "BrainBox AI"),
    "Sarah Ryan_Education and Skills_EN.docx":       ("inclusive-ai",               "Sarah Ryan",           ""),
    "Shelly Bruce_Security_EN.docx":                 ("sovereignty-security",       "Shelly Bruce",         "Former CSE Chief"),
    "Sonia Sennik_Adoption_EN.docx":                 ("adoption-commercialization", "Sonia Sennik",         "Creative Destruction Lab"),
    "Sonia Sennik_Safety and Trust_EN.docx":         ("public-trust-safety",        "Sonia Sennik",         "Creative Destruction Lab"),
    "Sonia Sennik_Scaling_EN.docx":                  ("adoption-commercialization", "Sonia Sennik",         "Creative Destruction Lab"),
    "Taylor Owen_Safety and Trust_EN.docx":          ("public-trust-safety",        "Taylor Owen",          "McGill University"),
}

# XLSX metadata columns
COL_ID            = 0
COL_STATUS        = 4
COL_RESPONDENT_AS = 7   # "A Canadian business representative", "An individual", etc.
COL_ORG_OR_IND    = 9   # "Individual" / "Organization"
COL_GENDER        = 53
COL_AGE           = 55
COL_PROVINCE      = 56

# Rating/ranking columns — responses are numeric scores, not open text.
# These are used directly as pillar priority scores (normalized to 0–10)
# and bypass the LLM chunk pipeline entirely.
# Format: col_index → (pillar_id, question_label)
# TODO: inspect the actual XLSX to identify rating columns and populate this.
# If the consultation used only open-text questions, leave this empty.
RATING_COLS: dict[int, tuple[str, str]] = {
    # Example — replace with real column indices after inspecting the XLSX:
    # 10: ("talent-research",          "Rate the importance of AI talent investment (1–5)"),
    # 11: ("regulation-governance",    "Rate the importance of AI regulation (1–5)"),
}

SALIENCE_WEIGHTS = {"primary": 3, "secondary": 2, "passing": 1}
DEPTH_WEIGHTS    = {"evidence-based": 3, "reasoned": 2, "assertion": 1}

# Public URLs for each expert report — shown as "View full report ↗" in the comment viewer.
# Populate once the PDFs are hosted (open.canada.ca, GitHub, or project CDN).
# Keys must match filenames in REPORT_MAP exactly (without path).
REPORT_URLS: dict[str, str] = {
    # "Arvind Gupta_Research and Talent_EN.docx": "https://example.com/reports/arvind-gupta.pdf",
}
