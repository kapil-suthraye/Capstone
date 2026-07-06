#!/usr/bin/env bash
# Load-test scenarios for Medical AI Reviewer.
# Usage: ./run_load_tests.sh <smoke|load|stress|spike|soak> [host]
#
# Results (HTML report + CSVs) land in ./results/<scenario>-<timestamp>/

set -euo pipefail

SCENARIO="${1:-smoke}"
HOST="${2:-http://localhost:8000}"
STAMP="$(date +%Y%m%d-%H%M%S)"
OUT="results/${SCENARIO}-${STAMP}"
mkdir -p "$OUT"

COMMON=(-f locustfile.py --host "$HOST" --headless
        --html "$OUT/report.html" --csv "$OUT/stats"
        --only-summary)

case "$SCENARIO" in
  smoke)
    # Sanity check: does everything respond correctly under trivial load?
    locust "${COMMON[@]}" -u 5 -r 1 -t 2m --tags cheap
    ;;
  load)
    # Expected normal traffic: ~30 concurrent reviewers for 10 minutes.
    locust "${COMMON[@]}" -u 30 -r 3 -t 10m --tags cheap
    ;;
  stress)
    # Push until it degrades: ramp to 200 users. Watch where p95 breaks.
    locust "${COMMON[@]}" -u 200 -r 10 -t 15m --tags cheap
    ;;
  spike)
    # Sudden burst: 100 users arriving almost at once, short window.
    locust "${COMMON[@]}" -u 100 -r 50 -t 3m --tags cheap
    ;;
  soak)
    # Endurance: moderate load for 1 hour. Catches memory leaks — important
    # here because the ReviewStore is IN-MEMORY and grows unbounded.
    locust "${COMMON[@]}" -u 20 -r 2 -t 60m --tags cheap
    ;;
  full)
    # Includes expensive endpoints. COSTS OPENAI/PINECONE MONEY.
    echo "WARNING: this hits /api/upload and /api/evaluate (real API costs)."
    read -rp "Continue? [y/N] " ok; [[ "$ok" == "y" ]] || exit 1
    ENABLE_UPLOAD=1 ENABLE_EVALUATE=1 \
      locust "${COMMON[@]}" -u 15 -r 2 -t 10m
    ;;
  *)
    echo "unknown scenario: $SCENARIO (use smoke|load|stress|spike|soak|full)"
    exit 1
    ;;
esac

echo
echo "Report: $OUT/report.html"
