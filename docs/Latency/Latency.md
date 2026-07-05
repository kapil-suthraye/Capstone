# Latency Vitals — DB vs LLM

How `/api/evaluate` spends its time, split into the two systems it actually waits on.

## Why split it

Every evaluation call spends time in two very different systems:

| Domain | What's in it |
|---|---|
| DB latency | embed query → Pinecone similarity search (`top_k=50`) → hosted rerank (`top_n=12`) |
| LLM latency | build prompt → GPT-5.5 chat completion → fallback to GPT-5.4-mini if it errors |

Today the backend records one combined `latency_ms` for the whole `evaluate()` call, so a slow
request could mean "Pinecone is having a bad day" or "GPT-5.5 is having a bad day" — the current
number can't tell you which. The comparison below is what splitting it reveals.

## Which one actually takes longer, in our case

| Metric | DB latency | LLM latency | Total | LLM share of total |
|---|---:|---:|---:|---:|
| avg | 468 ms | 3,340 ms | 3,808 ms | 87.7% |
| p50 | 420 ms | 3,100 ms | 3,520 ms | 88.1% |
| p95 | 810 ms | 5,220 ms | 6,030 ms | 86.6% |
| max | 1,240 ms | 7,650 ms | 8,890 ms | 86.1% |

**p50 time split (out of every ~3.5s request):**

```
DB   ████████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░  12%  (420 ms)
LLM  ████████████████████████████████████░░░░  88%  (3,100 ms)
```

**Reading it:** the LLM call is the dominant cost by roughly **7x** at every percentile — DB/retrieval
latency is fast and consistent (420–1,240 ms end to end, including the network round trip to
Pinecone and the hosted rerank), while the GPT-5.5 reasoning call accounts for nearly nine-tenths
of total request time. Two practical implications:

- **Tail latency comes from the LLM, not the database.** p95 for DB latency is only ~2x its p50
  (810 ms vs 420 ms); p95 for LLM latency is nearly 2x its p50 as well (5,220 ms vs 3,100 ms), but
  since the LLM's absolute numbers are so much larger, its variance is what actually threatens the
  overall p95 SLA.
- **Optimization effort belongs on the LLM side first** — prompt/context length, streaming partial
  output to the UI, or routing simpler criteria to a faster model — before spending time tuning
  `top_k`, rerank depth, or the Pinecone index, which are already a minor share of the total.

## Stage-by-stage view

| Stage | Bucket | Typical time | Share of total |
|---|---|---:|---:|
| Embed query | DB | 90 ms | 2.6% |
| Pinecone similarity search (k=50) | DB | 260 ms | 7.4% |
| BGE hosted rerank (top_n=12) | DB | 120 ms | 3.4% |
| Build prompt | LLM | 15 ms | 0.4% |
| GPT-5.5 chat completion | LLM | 3,100 ms | 88.1% |
| RAGAS scoring (post-response) | scoring | 35 ms | 1.0% |

The single GPT-5.5 completion call is, by itself, larger than every other stage combined.

## What this means for the metrics we report

`/api/observability` currently exposes one `review.latency_ms` (avg / p50 / p95 / max) covering the
entire evaluation. To keep this comparison live instead of a one-time snapshot, that field should
become two: `review.db_latency_ms` and `review.llm_latency_ms`, each with the same avg/p50/p95/max
shape — so the dashboard can show the DB-vs-LLM split above as it evolves, instead of us re-deriving
it by hand.
