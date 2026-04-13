"""
Pass 2 — LLM-label all chunks with topic, sentiment, salience, depth.

Runs per pillar, batching 50–100 chunks at a time.
Uses claude-haiku for public chunks, claude-sonnet for expert chunks.

Usage:
    python pipeline/03_pass2_label.py [--pillar PILLAR_ID] [--source public|expert]
"""
import argparse
import json
import re
import sqlite3
import sys
import time
from pathlib import Path

import os
import groq

sys.path.insert(0, str(Path(__file__).parent))
from config import DB_PATH, MODEL_EXPERT, MODEL_PUBLIC, SALIENCE_WEIGHTS, DEPTH_WEIGHTS

client = groq.Groq(api_key=os.environ["GROQ_API_KEY"])

BATCH_SIZE = 60

LABEL_PROMPT = """You are analyzing chunks of text from Canada's national AI strategy consultation.
Each chunk is a response (public comment or expert report section) about AI policy in the pillar: "{pillar}".

For each chunk, return:
- topic: a 3–6 word plain-English label describing the specific subtopic (e.g. "Graduate student funding gaps", "Sovereign compute infrastructure")
- sentiment: one of supportive / opposed / concerned / neutral
- salience: one of primary (central argument) / secondary (supporting point) / passing (brief mention)
- depth: one of evidence-based (cites data/research) / reasoned (structured argument) / assertion (opinion stated without support)

Return ONLY a JSON array — one object per input chunk, in the same order.
Each object: {{"id": <chunk_id>, "topic": "...", "sentiment": "...", "salience": "...", "depth": "..."}}

Chunks to label:
{chunks_json}
"""


def build_prompt(pillar_id: str, chunks: list[dict]) -> str:
    chunks_json = json.dumps(
        [{"id": c["id"], "text": (c["header"] + " — " + c["body"] if c["header"] else c["body"])[:500]}
         for c in chunks],
        ensure_ascii=False, indent=2,
    )
    pillar_label = pillar_id.replace("-", " ").title()
    return LABEL_PROMPT.format(pillar=pillar_label, chunks_json=chunks_json)


def parse_labels(raw: str) -> list[dict]:
    raw = re.sub(r"^```(?:json)?\s*", "", raw.strip())
    raw = re.sub(r"\s*```$", "",  raw)
    return json.loads(raw)


def label_batch(chunks: list[dict], model: str) -> list[dict]:
    prompt = build_prompt(chunks[0]["pillar_id"], chunks)
    try:
        msg = client.chat.completions.create(
            model=model,
            max_tokens=4096,
            messages=[{"role": "user", "content": prompt}],
        )
        return parse_labels(msg.choices[0].message.content)
    except Exception as e:
        print(f"    [ERROR] label_batch: {e}")
        return []


def run_pillar(con: sqlite3.Connection, pillar_id: str, source: str | None = None) -> int:
    source_filter = f"AND source = '{source}'" if source else ""
    rows = con.execute(
        f"""
        SELECT id, pillar_id, source, header, body
        FROM chunks
        WHERE pillar_id = ? AND labeled = 0
        {source_filter}
        ORDER BY id
        """,
        (pillar_id,),
    ).fetchall()

    if not rows:
        print(f"  No unlabeled chunks for {pillar_id}.")
        return 0

    chunks = [{"id": r[0], "pillar_id": r[1], "source": r[2], "header": r[3], "body": r[4]}
              for r in rows]

    print(f"  {len(chunks):,} chunks to label in {pillar_id} …")
    labeled_count = 0

    for i in range(0, len(chunks), BATCH_SIZE):
        batch = chunks[i: i + BATCH_SIZE]
        # Use haiku for public, sonnet for expert
        model = MODEL_PUBLIC if all(c["source"] == "public" for c in batch) else MODEL_EXPERT

        labels = label_batch(batch, model)
        id_to_label = {item["id"]: item for item in labels}

        for chunk in batch:
            label = id_to_label.get(chunk["id"])
            if not label:
                con.execute("UPDATE chunks SET labeled=-1, label_error='missing' WHERE id=?", (chunk["id"],))
                continue

            VALID_SENTIMENT = {"supportive", "opposed", "concerned", "neutral"}
            VALID_SALIENCE  = {"primary", "secondary", "passing"}
            VALID_DEPTH     = {"evidence-based", "reasoned", "assertion"}

            sent = label.get("sentiment", "neutral")
            sal  = label.get("salience",  "passing")
            dep  = label.get("depth",     "assertion")

            # Normalize common LLM variants before constraint check
            sent_map = {"positive": "supportive", "negative": "opposed",
                        "mixed": "concerned", "critical": "opposed"}
            sent = sent_map.get(sent, sent)

            if sent not in VALID_SENTIMENT: sent = "neutral"
            if sal  not in VALID_SALIENCE:  sal  = "passing"
            if dep  not in VALID_DEPTH:     dep  = "assertion"
            score = SALIENCE_WEIGHTS.get(sal, 1) * DEPTH_WEIGHTS.get(dep, 1)

            con.execute(
                """
                UPDATE chunks
                SET raw_topic=?, sentiment=?, salience=?, depth=?, priority_score=?, labeled=1
                WHERE id=?
                """,
                (label.get("topic", ""), sent, sal, dep, score, chunk["id"]),
            )
            labeled_count += 1

        con.commit()
        print(f"    [{i + len(batch):,}/{len(chunks):,}] labeled")
        time.sleep(0.3)

    return labeled_count


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--pillar", help="Limit to one pillar ID")
    parser.add_argument("--source", choices=["public", "expert"], help="Limit to one source")
    args = parser.parse_args()

    con = sqlite3.connect(DB_PATH)

    pillars = con.execute("SELECT DISTINCT pillar_id FROM chunks ORDER BY pillar_id").fetchall()
    pillar_ids = [p[0] for p in pillars]

    if args.pillar:
        pillar_ids = [p for p in pillar_ids if p == args.pillar]

    total = 0
    for pid in pillar_ids:
        print(f"\n→ Pillar: {pid}")
        n = run_pillar(con, pid, args.source)
        total += n
        print(f"  {n:,} labeled.")

    print(f"\nPass 2 complete. {total:,} total chunks labeled.")
    con.close()


if __name__ == "__main__":
    main()
