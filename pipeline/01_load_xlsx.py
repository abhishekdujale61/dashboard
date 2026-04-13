"""
Pass 0 — Load public XLSX consultation responses into the chunk store.

Each non-empty open-text response (cols 27–52) becomes one chunk.
Metadata (respondent type, province) is captured for downstream filtering.

Usage:
    python pipeline/01_load_xlsx.py
"""
import sqlite3
import sys
from pathlib import Path

import openpyxl

sys.path.insert(0, str(Path(__file__).parent))
from config import (
    DB_PATH, PIPELINE_DIR, XLSX_PATH,
    QUESTION_MAP, QUESTION_TEXTS, RATING_COLS,
    COL_ID, COL_STATUS, COL_ORG_OR_IND, COL_PROVINCE,
)


def init_db(con: sqlite3.Connection) -> None:
    schema = (PIPELINE_DIR / "schema.sql").read_text()
    con.executescript(schema)
    con.commit()


def province_abbr(raw: str | None) -> str | None:
    """Map the full province/territory name to a 2-letter abbreviation."""
    if not raw:
        return None
    mapping = {
        "Alberta": "AB", "British Columbia": "BC", "Manitoba": "MB",
        "New Brunswick": "NB", "Newfoundland and Labrador": "NL",
        "Northwest Territories": "NT", "Nova Scotia": "NS", "Nunavut": "NU",
        "Ontario": "ON", "Prince Edward Island": "PE", "Quebec": "QC",
        "Saskatchewan": "SK", "Yukon": "YT",
    }
    for full, abbr in mapping.items():
        if full.lower() in raw.lower():
            return abbr
    return raw[:2].upper() if raw else None


def load_xlsx(con: sqlite3.Connection) -> tuple[int, dict[str, list[float]]]:
    """
    Load public XLSX into the chunk store.

    Returns:
        inserted        — number of open-text chunks inserted
        rating_scores   — {pillar_id: [score, ...]} for direct rating columns
                          (these bypass the LLM pipeline and are used directly
                          in the export as pillar-level scores)
    """
    print(f"Opening XLSX: {XLSX_PATH}")
    wb = openpyxl.load_workbook(XLSX_PATH, read_only=True)
    ws = wb.active
    rows = list(ws.iter_rows(values_only=True))

    inserted = 0
    rating_scores: dict[str, list[float]] = {}

    for row in rows[1:]:  # skip header
        respondent_id   = str(row[COL_ID]) if row[COL_ID] else None
        respondent_type = str(row[COL_ORG_OR_IND]).strip() if row[COL_ORG_OR_IND] else "Individual"
        province_raw    = str(row[COL_PROVINCE]).strip() if row[COL_PROVINCE] else None
        province        = province_abbr(province_raw)

        # Open-text questions → chunk store (goes through LLM pipeline)
        for col_idx, pillar_id in QUESTION_MAP.items():
            cell_value = row[col_idx]
            if not cell_value:
                continue
            body = str(cell_value).strip()
            if len(body) < 20:
                continue

            con.execute(
                """
                INSERT INTO chunks
                    (pillar_id, source, respondent_id, question_col, question_text,
                     respondent_type, province, body)
                VALUES (?, 'public', ?, ?, ?, ?, ?, ?)
                """,
                (
                    pillar_id, respondent_id, col_idx,
                    QUESTION_TEXTS.get(col_idx, ""),
                    respondent_type, province, body,
                ),
            )
            inserted += 1

        # Rating/ranking questions → collect raw scores, bypass LLM pipeline
        for col_idx, (pillar_id, _label) in RATING_COLS.items():
            cell_value = row[col_idx]
            if cell_value is None:
                continue
            try:
                score = float(cell_value)
                rating_scores.setdefault(pillar_id, []).append(score)
            except (ValueError, TypeError):
                pass

        if inserted % 5000 == 0 and inserted > 0:
            con.commit()
            print(f"  {inserted:,} chunks inserted …")

    con.commit()

    # Persist rating score averages to a lightweight table for the export script
    if rating_scores:
        con.executescript(
            "CREATE TABLE IF NOT EXISTS rating_scores "
            "(pillar_id TEXT PRIMARY KEY, avg_score REAL, n INTEGER);"
        )
        for pillar_id, scores in rating_scores.items():
            avg = sum(scores) / len(scores)
            con.execute(
                "INSERT OR REPLACE INTO rating_scores VALUES (?,?,?)",
                (pillar_id, round(avg, 2), len(scores)),
            )
        con.commit()
        print(f"Rating columns: {len(rating_scores)} pillars with direct scores.")

    print(f"Done. {inserted:,} public open-text chunks loaded.")
    return inserted, rating_scores


def main() -> None:
    con = sqlite3.connect(DB_PATH)
    init_db(con)

    existing = con.execute("SELECT COUNT(*) FROM chunks WHERE source='public'").fetchone()[0]
    if existing > 0:
        print(f"Public chunks already loaded ({existing:,}). Delete DB to reload.")
        con.close()
        return

    load_xlsx(con)
    con.close()



if __name__ == "__main__":
    main()
