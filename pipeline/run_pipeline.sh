#!/usr/bin/env bash
# GovAI Dashboard V2 — Full pipeline runner
# Requires: ANTHROPIC_API_KEY set in environment
#
# Usage:
#   export ANTHROPIC_API_KEY=sk-ant-...
#   bash pipeline/run_pipeline.sh
#
# Individual steps can be re-run independently.
# The DB is incremental — already-processed records are skipped.

set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR/.."

if [[ -z "${ANTHROPIC_API_KEY:-}" ]]; then
  echo "Error: ANTHROPIC_API_KEY is not set."
  echo "Run: export ANTHROPIC_API_KEY=sk-ant-..."
  exit 1
fi

echo "========================================"
echo " GovAI Dashboard V2 Pipeline"
echo "========================================"
echo ""

echo "Step 1/5: Loading public XLSX into chunk store …"
python3 pipeline/01_load_xlsx.py

echo ""
echo "Step 2/5: Pass 1 — Atomizing expert reports …"
python3 pipeline/02_pass1_atomize.py

echo ""
echo "Step 3/5: Pass 2 — LLM-labeling all chunks …"
python3 pipeline/03_pass2_label.py

echo ""
echo "Step 4/5: Pass 3 — Canonicalizing topics per pillar …"
python3 pipeline/04_pass3_canonicalize.py

echo ""
echo "Step 5/5: Exporting JSON for frontend …"
python3 pipeline/05_export_json.py

echo ""
echo "========================================"
echo " Pipeline complete! Start the dev server:"
echo "   npm run dev"
echo "========================================"
