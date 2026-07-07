"""
Load tests for Medical AI Reviewer (kapil-suthraye/Capstone) — v2
==================================================================

v2 changes (debuggability):
  - Prints a CONFIG banner at startup showing whether upload/evaluate are
    enabled and whether the test PDF was found.
  - Env vars are stripped, so `set ENABLE_UPLOAD=1 ` (trailing space in cmd)
    still works.
  - Upload/evaluate users use fixed_count so they ALWAYS spawn.
  - Skipped tasks log a reason once instead of failing silently.

Enable expensive endpoints (Windows cmd):
    set ENABLE_UPLOAD=1
    set ENABLE_EVALUATE=1
    set TEST_PDF_PATH=test_records/synthetic_record.pdf
    locust -f locustfile.py --host http://localhost:8000
"""

import os
import random

from locust import HttpUser, task, between, tag, events


def _env_flag(name: str) -> bool:
    return os.getenv(name, "0").strip() == "1"


# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------
ENABLE_UPLOAD = _env_flag("ENABLE_UPLOAD")
ENABLE_EVALUATE = _env_flag("ENABLE_EVALUATE")
TEST_PDF_PATH = os.getenv("TEST_PDF_PATH", "test_records/synthetic_record.pdf").strip()
SEED_NAMESPACE = os.getenv("SEED_NAMESPACE", "").strip()

# Resolve PDF path relative to this file, so cwd doesn't matter.
if not os.path.isabs(TEST_PDF_PATH):
    _here = os.path.dirname(os.path.abspath(__file__))
    _candidate = os.path.join(_here, TEST_PDF_PATH)
    if os.path.exists(_candidate):
        TEST_PDF_PATH = _candidate

PDF_EXISTS = os.path.exists(TEST_PDF_PATH)

DISCOVERED = {
    "prompt_ids": [],
    "namespaces": [],
}

_warned = set()


def warn_once(key: str, msg: str):
    if key not in _warned:
        _warned.add(key)
        print(f"\n[locustfile WARNING] {msg}\n")


@events.test_start.add_listener
def print_config(environment, **kwargs):
    print("=" * 62)
    print("LOAD TEST CONFIG")
    print(f"  ENABLE_UPLOAD   = {ENABLE_UPLOAD}   (raw: {os.getenv('ENABLE_UPLOAD')!r})")
    print(f"  ENABLE_EVALUATE = {ENABLE_EVALUATE}   (raw: {os.getenv('ENABLE_EVALUATE')!r})")
    print(f"  TEST_PDF_PATH   = {TEST_PDF_PATH}")
    print(f"  PDF found       = {PDF_EXISTS}")
    print(f"  SEED_NAMESPACE  = {SEED_NAMESPACE or '(none)'}")
    if ENABLE_UPLOAD and not PDF_EXISTS:
        print("  !! Upload enabled but PDF NOT FOUND -> uploads will be skipped.")
        print("  !! Run: python generate_test_pdf.py")
    if not ENABLE_UPLOAD and not ENABLE_EVALUATE:
        print("  NOTE: only GET endpoints will run. Set ENABLE_UPLOAD=1 /")
        print("        ENABLE_EVALUATE=1 to exercise the POST endpoints.")
    print("=" * 62)


@events.quitting.add_listener
def check_slos(environment, **kwargs):
    stats = environment.stats.total
    failed = []
    if stats.fail_ratio > 0.01:
        failed.append(f"error rate {stats.fail_ratio:.2%} > 1%")
    p95 = stats.get_response_time_percentile(0.95)
    if p95 and p95 > 2000:
        failed.append(f"p95 {p95:.0f}ms > 2000ms")
    if failed:
        print("\n*** SLO CHECK FAILED: " + "; ".join(failed) + " ***")
        environment.process_exit_code = 1
    else:
        print("\n*** SLO check passed ***")


# ---------------------------------------------------------------------------
# Reviewer user: read-heavy browsing (dashboard traffic)
# ---------------------------------------------------------------------------
class ReviewerUser(HttpUser):
    wait_time = between(1, 4)
    weight = 8

    def on_start(self):
        with self.client.get("/api/prompts", name="/api/prompts [on_start]",
                             catch_response=True) as resp:
            if resp.status_code == 200:
                try:
                    data = resp.json()
                    items = data if isinstance(data, list) else data.get("prompts", [])
                    ids = [p.get("prompt_id") or p.get("id")
                           for p in items if isinstance(p, dict)]
                    DISCOVERED["prompt_ids"] = [i for i in ids if i]
                    resp.success()
                except Exception:
                    resp.failure("prompts response was not parseable JSON")
        if SEED_NAMESPACE and SEED_NAMESPACE not in DISCOVERED["namespaces"]:
            DISCOVERED["namespaces"].append(SEED_NAMESPACE)

    @tag("cheap")
    @task(10)
    def health(self):
        self.client.get("/api/health")

    @tag("cheap")
    @task(8)
    def dashboard(self):
        with self.client.get("/api/dashboard", catch_response=True) as resp:
            if resp.status_code == 200:
                try:
                    data = resp.json()
                    claims = data if isinstance(data, list) else data.get("claims", [])
                    for c in claims:
                        if isinstance(c, dict):
                            ns = c.get("namespace") or c.get("document_id")
                            if ns and ns not in DISCOVERED["namespaces"]:
                                DISCOVERED["namespaces"].append(ns)
                except Exception:
                    pass
                resp.success()

    @tag("cheap")
    @task(6)
    def prompts(self):
        self.client.get("/api/prompts")

    @tag("cheap")
    @task(4)
    def metrics(self):
        self.client.get("/api/metrics")

    @tag("cheap")
    @task(3)
    def observability(self):
        self.client.get("/api/observability")

    @tag("cheap")
    @task(5)
    def claim_summary(self):
        if not DISCOVERED["namespaces"]:
            warn_once("no-ns-summary",
                      "Skipping /api/claims/[ns]/summary — no namespaces known yet "
                      "(upload a document, or set SEED_NAMESPACE=<document_id>).")
            return
        ns = random.choice(DISCOVERED["namespaces"])
        self.client.get(f"/api/claims/{ns}/summary",
                        name="/api/claims/[ns]/summary")


# ---------------------------------------------------------------------------
# Ingestion user: POST /api/upload (expensive — gated by ENABLE_UPLOAD)
# ---------------------------------------------------------------------------
class IngestionUser(HttpUser):
    wait_time = between(20, 40)
    # fixed_count guarantees exactly this many spawn regardless of weights,
    # so uploads can't be crowded out at low user counts.
    fixed_count = 1 if ENABLE_UPLOAD else 0
    weight = 1

    def on_start(self):
        self.pdf_bytes = None
        if ENABLE_UPLOAD and PDF_EXISTS:
            with open(TEST_PDF_PATH, "rb") as f:
                self.pdf_bytes = f.read()
            print(f"[IngestionUser] loaded test PDF "
                  f"({len(self.pdf_bytes)} bytes) — uploads ACTIVE")

    @tag("expensive", "upload")
    @task
    def upload_pdf(self):
        if not ENABLE_UPLOAD:
            warn_once("upload-off", "ENABLE_UPLOAD is not 1 — uploads skipped.")
            return
        if not self.pdf_bytes:
            warn_once("no-pdf",
                      f"Test PDF not found at {TEST_PDF_PATH} — uploads skipped. "
                      "Run: python generate_test_pdf.py")
            return
        files = {"file": ("load_test_record.pdf", self.pdf_bytes, "application/pdf")}
        with self.client.post("/api/upload", files=files, timeout=120,
                              catch_response=True) as resp:
            if resp.status_code == 200:
                try:
                    ns = resp.json().get("namespace")
                    if ns:
                        DISCOVERED["namespaces"].append(ns)
                        print(f"[IngestionUser] uploaded OK -> namespace {ns}")
                    resp.success()
                except Exception:
                    resp.failure("upload returned non-JSON body")
            else:
                resp.failure(f"upload failed: HTTP {resp.status_code} "
                             f"{resp.text[:200]}")


# ---------------------------------------------------------------------------
# Evaluation user: POST /api/evaluate (very expensive — gated)
# ---------------------------------------------------------------------------
class EvaluationUser(HttpUser):
    wait_time = between(30, 60)
    fixed_count = 1 if ENABLE_EVALUATE else 0
    weight = 1

    @tag("expensive", "evaluate")
    @task
    def evaluate(self):
        if not ENABLE_EVALUATE:
            warn_once("eval-off", "ENABLE_EVALUATE is not 1 — evaluations skipped.")
            return
        if not DISCOVERED["namespaces"]:
            warn_once("no-ns-eval",
                      "No namespace available for /api/evaluate yet — waiting for "
                      "an upload to finish, or set SEED_NAMESPACE=<document_id>.")
            return
        if not DISCOVERED["prompt_ids"]:
            warn_once("no-prompts",
                      "No prompt IDs discovered from /api/prompts — cannot evaluate. "
                      "Check the shape of that endpoint's response.")
            return
        payload = {
            "namespace": random.choice(DISCOVERED["namespaces"]),
            "prompt_id": random.choice(DISCOVERED["prompt_ids"]),
        }
        with self.client.post("/api/evaluate", json=payload, timeout=180,
                              name="/api/evaluate", catch_response=True) as resp:
            if resp.status_code == 200:
                resp.success()
            elif resp.status_code == 429:
                resp.failure("429 rate-limited (upstream LLM quota)")
            else:
                resp.failure(f"evaluate failed: HTTP {resp.status_code} "
                             f"{resp.text[:200]}")