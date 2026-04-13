-- GovAI Dashboard V2 — chunk store schema
PRAGMA journal_mode=WAL;
PRAGMA foreign_keys=ON;

CREATE TABLE IF NOT EXISTS chunks (
    id               INTEGER PRIMARY KEY AUTOINCREMENT,
    pillar_id        TEXT    NOT NULL,
    source           TEXT    NOT NULL CHECK(source IN ('public','expert')),

    -- Public-only fields
    respondent_id    TEXT,
    question_col     INTEGER,
    question_text    TEXT,
    respondent_type  TEXT,   -- "Individual" / "Organization"
    province         TEXT,

    -- Expert-only fields
    expert_name      TEXT,
    affiliation      TEXT,
    report_filename  TEXT,
    report_title     TEXT,

    -- Content (both sources)
    header           TEXT,   -- generated for expert chunks; NULL for public
    body             TEXT    NOT NULL,

    -- Pass 2 LLM labels
    raw_topic        TEXT,
    sentiment        TEXT    CHECK(sentiment IN ('supportive','opposed','concerned','neutral')),
    salience         TEXT    CHECK(salience  IN ('primary','secondary','passing')),
    depth            TEXT    CHECK(depth     IN ('evidence-based','reasoned','assertion')),
    priority_score   REAL,   -- salience_weight * depth_weight, computed after labeling

    -- Pass 3 canonical topic
    canonical_topic  TEXT,

    -- Processing bookkeeping
    labeled          INTEGER DEFAULT 0,
    label_error      TEXT,
    created_at       TEXT    DEFAULT (datetime('now'))
);

CREATE INDEX IF NOT EXISTS idx_chunks_pillar  ON chunks(pillar_id);
CREATE INDEX IF NOT EXISTS idx_chunks_source  ON chunks(source);
CREATE INDEX IF NOT EXISTS idx_chunks_topic   ON chunks(canonical_topic);
CREATE INDEX IF NOT EXISTS idx_chunks_labeled ON chunks(labeled);

CREATE TABLE IF NOT EXISTS canonical_topics (
    id                         INTEGER PRIMARY KEY AUTOINCREMENT,
    pillar_id                  TEXT    NOT NULL,
    topic_id                   TEXT    NOT NULL,   -- slugified canonical label
    label                      TEXT    NOT NULL,   -- human-readable e.g. "Graduate funding & compute access"
    public_score               REAL,
    expert_score               REAL,
    delta                      REAL,
    alignment_status           TEXT    CHECK(alignment_status IN ('aligned','tension','diverges')),
    dominant_public_sentiment  TEXT,
    dominant_expert_sentiment  TEXT,
    public_chunk_count         INTEGER DEFAULT 0,
    expert_chunk_count         INTEGER DEFAULT 0,
    UNIQUE(pillar_id, topic_id)
);

CREATE TABLE IF NOT EXISTS raw_topic_map (
    id             INTEGER PRIMARY KEY AUTOINCREMENT,
    pillar_id      TEXT    NOT NULL,
    raw_label      TEXT    NOT NULL,
    canonical_label TEXT   NOT NULL,
    UNIQUE(pillar_id, raw_label)
);
