"""
Pass 1 — Atomize expert reports.

Each .docx expert report is split into atomic idea chunks (one idea = one chunk)
using an LLM. The LLM receives a section of text and returns a JSON array of
{header, body} objects.

Usage:
    python pipeline/02_pass1_atomize.py
"""
import json
import re
import sqlite3
import sys
import time
from pathlib import Path

import anthropic
import docx

sys.path.insert(0, str(Path(__file__).parent))
from config import DB_PATH, MODEL_EXPERT, REPORTS_DIR, REPORT_MAP

client = anthropic.Anthropic()

ATOMIZE_PROMPT = """You are processing a section of a Canadian government AI Task Force expert report.
Break the following text into atomic idea chunks — each chunk should contain exactly ONE distinct idea, claim, recommendation, or finding.

Rules:
- If the text contains a heading followed by a paragraph, that is often one chunk.
- Do not merge two separate recommendations into one chunk.
- Do not split one coherent argument across two chunks.
- Preserve the author's language as closely as possible in the body.
- Generate a concise header (5–10 words) if none is obvious from the text.

Return ONLY a JSON array with no preamble. Each element: {"header": "...", "body": "..."}

Text to process:
"""


def extract_sections(doc_path: Path) -> list[dict]:
    """Extract paragraphs grouped into sections from a .docx file."""
    doc = docx.Document(doc_path)
    sections: list[dict] = []
    current_header = ""
    current_body_parts: list[str] = []

    for para in doc.paragraphs:
        text = para.text.strip()
        if not text:
            continue

        style = para.style.name.lower() if para.style else ""
        is_heading = "heading" in style or (
            para.runs and para.runs[0].bold and len(text) < 120 and not text.endswith(".")
        )

        if is_heading:
            if current_body_parts:
                sections.append({"header": current_header, "body": " ".join(current_body_parts)})
            current_header = text
            current_body_parts = []
        else:
            current_body_parts.append(text)

    if current_body_parts:
        sections.append({"header": current_header, "body": " ".join(current_body_parts)})

    return sections


def atomize_section(header: str, body: str) -> list[dict]:
    """Ask the LLM to split one section into atomic idea chunks."""
    combined = f"[Section heading: {header}]\n\n{body}" if header else body

    # Skip very short sections — they're already atomic
    if len(body) < 200:
        return [{"header": header or "Note", "body": body}]

    try:
        msg = client.messages.create(
            model=MODEL_EXPERT,
            max_tokens=2048,
            messages=[{"role": "user", "content": ATOMIZE_PROMPT + combined}],
        )
        raw = msg.content[0].text.strip()
        # Strip markdown fences if present
        raw = re.sub(r"^```(?:json)?\s*", "", raw)
        raw = re.sub(r"\s*```$", "", raw)
        chunks = json.loads(raw)
        if isinstance(chunks, list):
            return chunks
    except Exception as e:
        print(f"    atomize error: {e}")

    # Fallback: return section as-is
    return [{"header": header or "Section", "body": body}]


def process_report(con: sqlite3.Connection, filename: str, doc_path: Path) -> int:
    pillar_id, expert_name, affiliation = REPORT_MAP[filename]
    report_title = filename.replace("_EN.docx", "").replace("_", " ")

    # Skip if already processed
    existing = con.execute(
        "SELECT COUNT(*) FROM chunks WHERE source='expert' AND report_filename=?",
        (filename,),
    ).fetchone()[0]
    if existing > 0:
        print(f"  Already processed ({existing} chunks) — skipping.")
        return 0

    print(f"  Extracting sections from {filename} …")
    sections = extract_sections(doc_path)
    print(f"  {len(sections)} sections found. Atomizing with LLM …")

    total = 0
    for i, section in enumerate(sections):
        header = section.get("header", "")
        body   = section.get("body",   "").strip()
        if not body or len(body) < 30:
            continue

        atoms = atomize_section(header, body)
        for atom in atoms:
            atom_header = atom.get("header", header)
            atom_body   = atom.get("body",   "").strip()
            if not atom_body:
                continue
            con.execute(
                """
                INSERT INTO chunks
                    (pillar_id, source, expert_name, affiliation, report_filename,
                     report_title, header, body)
                VALUES (?, 'expert', ?, ?, ?, ?, ?, ?)
                """,
                (pillar_id, expert_name, affiliation, filename, report_title, atom_header, atom_body),
            )
            total += 1

        time.sleep(0.2)  # rate-limit courtesy pause

    con.commit()
    return total


def main() -> None:
    con = sqlite3.connect(DB_PATH)

    for filename, (pillar_id, expert_name, affiliation) in REPORT_MAP.items():
        doc_path = REPORTS_DIR / filename
        if not doc_path.exists():
            print(f"[WARN] Report not found: {doc_path}")
            continue

        print(f"\n→ {expert_name} / {pillar_id}")
        n = process_report(con, filename, doc_path)
        print(f"  Inserted {n} atomic chunks.")

    total = con.execute("SELECT COUNT(*) FROM chunks WHERE source='expert'").fetchone()[0]
    print(f"\nPass 1 complete. {total:,} expert chunks in DB.")
    con.close()


if __name__ == "__main__":
    main()
