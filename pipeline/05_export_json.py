"""
Export — Compute final normalized scores and export JSON files for the frontend.

Outputs (to src/data/):
  topics.json          — canonical topics per pillar with normalized scores
  quotes.json          — top public quotes per topic (keyed by topic_id)
  expert_chunks.json   — expert chunks per topic (keyed by topic_id)

Usage:
    python pipeline/05_export_json.py
"""
import json
import sqlite3
import sys
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from config import DB_PATH, EXPORT_DIR

QUOTES_PER_TOPIC = 5      # max public quotes to include per topic
MIN_BODY_LENGTH  = 40     # minimum body length for a quote to be included


def normalize_scores(raw_scores: list[float]) -> list[float]:
    """Normalize a list of raw scores to a 0–10 scale."""
    if not raw_scores:
        return []
    max_val = max(raw_scores) or 1
    return [round((s / max_val) * 10, 1) for s in raw_scores]


def load_rating_scores(con: sqlite3.Connection) -> dict[str, float]:
    """Return {pillar_id: avg_score} from direct rating columns, normalized to 0–10."""
    try:
        rows = con.execute("SELECT pillar_id, avg_score FROM rating_scores").fetchall()
    except Exception:
        return {}
    if not rows:
        return {}
    raw = {r[0]: r[1] for r in rows}
    max_val = max(raw.values()) or 1
    return {pid: round((v / max_val) * 10, 1) for pid, v in raw.items()}


def export_topics(con: sqlite3.Connection, rating_scores: dict[str, float] | None = None) -> list[dict]:
    """Build and normalize canonical topic records.

    rating_scores: {pillar_id: normalized_score} from direct XLSX rating columns.
    When present, the pillar-level rating score replaces the LLM-derived public
    priority score for topics in that pillar (spec: use direct scores directly).
    """
    rating_scores = rating_scores or {}
    rows = con.execute(
        """
        SELECT pillar_id, topic_id, label,
               public_score, expert_score,
               dominant_public_sentiment, dominant_expert_sentiment,
               public_chunk_count, expert_chunk_count
        FROM canonical_topics
        ORDER BY pillar_id, public_score DESC
        """
    ).fetchall()

    # Group by pillar for within-pillar normalization
    by_pillar: dict[str, list[dict]] = defaultdict(list)
    for r in rows:
        by_pillar[r[0]].append({
            "pillarId": r[0], "id": r[1], "label": r[2],
            "_pub_raw": r[3] or 0, "_exp_raw": r[4] or 0,
            "dominantPublicSentiment": r[5] or "neutral",
            "dominantExpertSentiment": r[6] or "neutral",
            "publicChunkCount": r[7] or 0,
            "expertChunkCount": r[8] or 0,
        })

    all_topics: list[dict] = []
    for pillar_id, topics in by_pillar.items():
        pub_raws = [t["_pub_raw"] for t in topics]
        exp_raws = [t["_exp_raw"] for t in topics]
        pub_norm = normalize_scores(pub_raws)
        exp_norm = normalize_scores(exp_raws)

        for i, topic in enumerate(topics):
            # Use direct rating score if available for this pillar (spec requirement)
            ps = rating_scores.get(pillar_id, pub_norm[i])
            es = exp_norm[i]
            delta = round(es - ps, 1)
            # Alignment is driven by sentiment comparison (spec), not score gap.
            # Score delta distinguishes tension from diverges when sentiments differ.
            dom_pub = topic["dominantPublicSentiment"]
            dom_exp = topic["dominantExpertSentiment"]
            if dom_pub == dom_exp:
                alignment = "aligned"
            elif abs(delta) < 1.0:
                alignment = "tension"
            else:
                alignment = "diverges"

            del topic["_pub_raw"]
            del topic["_exp_raw"]
            topic["publicScore"]     = ps
            topic["expertScore"]     = es
            topic["delta"]           = delta
            topic["alignmentStatus"] = alignment
            all_topics.append(topic)

    return all_topics


def export_quotes(con: sqlite3.Connection) -> dict[str, list[dict]]:
    """Select representative public quotes per topic."""
    rows = con.execute(
        """
        SELECT c.canonical_topic, ct.topic_id, c.id, c.body,
               c.sentiment, c.salience, c.depth, c.priority_score,
               c.respondent_type, c.province
        FROM chunks c
        JOIN canonical_topics ct ON ct.pillar_id = c.pillar_id AND ct.label = c.canonical_topic
        WHERE c.source = 'public'
          AND c.labeled = 1
          AND c.canonical_topic IS NOT NULL
          AND LENGTH(c.body) >= ?
        ORDER BY ct.topic_id, c.priority_score DESC
        """,
        (MIN_BODY_LENGTH,),
    ).fetchall()

    by_topic: dict[str, list[dict]] = defaultdict(list)
    seen_per_topic: dict[str, int] = defaultdict(int)

    for row in rows:
        canonical_topic, topic_id, chunk_id, body, sentiment, salience, depth, score, resp_type, province = row
        if seen_per_topic[topic_id] >= QUOTES_PER_TOPIC:
            continue
        by_topic[topic_id].append({
            "id": str(chunk_id),
            "text": body[:600],
            "sentiment": sentiment or "neutral",
            "salience": salience or "passing",
            "depth": depth or "assertion",
            "respondentType": resp_type or "Individual",
            "province": province,
            "score": score or 0,
        })
        seen_per_topic[topic_id] += 1

    return dict(by_topic)


def export_expert_chunks(con: sqlite3.Connection) -> dict[str, list[dict]]:
    """Export all expert chunks per topic."""
    rows = con.execute(
        """
        SELECT ct.topic_id, c.id, c.header, c.body,
               c.expert_name, c.affiliation, c.report_title,
               c.sentiment, c.salience, c.depth, c.priority_score
        FROM chunks c
        JOIN canonical_topics ct ON ct.pillar_id = c.pillar_id AND ct.label = c.canonical_topic
        WHERE c.source = 'expert'
          AND c.labeled = 1
          AND c.canonical_topic IS NOT NULL
        ORDER BY ct.topic_id, c.priority_score DESC
        """
    ).fetchall()

    by_topic: dict[str, list[dict]] = defaultdict(list)
    for row in rows:
        topic_id, chunk_id, header, body, expert_name, affiliation, report_title, \
            sentiment, salience, depth, score = row
        by_topic[topic_id].append({
            "id": str(chunk_id),
            "header": header or "",
            "body": body,
            "expertName": expert_name or "",
            "affiliation": affiliation or "",
            "reportTitle": report_title or "",
            "sentiment": sentiment or "neutral",
            "salience": salience or "passing",
            "depth": depth or "assertion",
            "score": score or 0,
        })

    return dict(by_topic)


def main() -> None:
    con = sqlite3.connect(DB_PATH)
    EXPORT_DIR.mkdir(parents=True, exist_ok=True)

    rating_scores = load_rating_scores(con)
    if rating_scores:
        print(f"  Using direct rating scores for {len(rating_scores)} pillar(s): {list(rating_scores)}")

    print("Exporting topics.json …")
    topics = export_topics(con, rating_scores)
    (EXPORT_DIR / "topics.json").write_text(
        json.dumps(topics, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(f"  {len(topics)} topics exported.")

    print("Exporting quotes.json …")
    quotes = export_quotes(con)
    (EXPORT_DIR / "quotes.json").write_text(
        json.dumps(quotes, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    topic_count = len(quotes)
    quote_count = sum(len(v) for v in quotes.values())
    print(f"  {quote_count} quotes across {topic_count} topics exported.")

    print("Exporting expert_chunks.json …")
    chunks = export_expert_chunks(con)
    (EXPORT_DIR / "expert_chunks.json").write_text(
        json.dumps(chunks, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    chunk_count = sum(len(v) for v in chunks.values())
    print(f"  {chunk_count} expert chunks across {len(chunks)} topics exported.")

    print("\nExport complete. Run `npm run dev` to see the updated dashboard.")
    con.close()


if __name__ == "__main__":
    main()
