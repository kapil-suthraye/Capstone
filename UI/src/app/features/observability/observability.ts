import { Component, OnInit, OnDestroy, signal, computed, inject } from '@angular/core';
import { DecimalPipe, DatePipe, PercentPipe } from '@angular/common';
import { Router, RouterLink } from '@angular/router';
import { interval, Subscription, of } from 'rxjs';
import { switchMap, startWith, catchError } from 'rxjs/operators';

import { ObservabilityService } from '../../core/services/observability';
import { SessionService } from '../../core/services/session';
import { ObservabilitySnapshot } from '../../core/models/observability';

interface MetricCard {
  label: string;
  value: string | number;
  unit?: string;
  icon: string;
  description: string;
  trend?: 'up' | 'down' | 'neutral';
}

interface BarSegment {
  label: string;
  value: number;
  color: string;
  pct: number;
}

@Component({
  selector: 'app-observability',
  standalone: true,
  imports: [DecimalPipe, DatePipe, PercentPipe, RouterLink],
  templateUrl: './observability.html',
  styleUrl: './observability.scss',
})
export class ObservabilityComponent implements OnInit, OnDestroy {
  private readonly obsService = inject(ObservabilityService);
  private readonly session = inject(SessionService);
  private readonly router = inject(Router);

  snapshot = signal<ObservabilitySnapshot | null>(null);
  loading = signal(true);
  /** Set when a fetch fails — shown as a quiet status line, not a blocking banner */
  backendReachable = signal(true);
  lastRefreshed = signal<Date | null>(null);

  private pollSub?: Subscription;

  // ── Derived metrics ────────────────────────────────────────────────

  systemCards = computed((): MetricCard[] => {
    const s = this.snapshot();
    if (!s) return [];
    const { traffic, review } = s.system;
    return [
      {
        label: 'Total Requests',
        value: traffic.requests_total,
        icon: 'http',
        description: 'Cumulative API calls handled since server start.',
      },
      {
        label: 'Error Rate',
        value: (traffic.error_rate * 100).toFixed(1),
        unit: '%',
        icon: 'error_outline',
        description: 'Percentage of requests that resulted in a 5xx error.',
        trend: traffic.error_rate === 0 ? 'neutral' : traffic.error_rate < 0.05 ? 'up' : 'down',
      },
      {
        label: 'Avg Request Latency',
        value: traffic.latency_ms.avg,
        unit: 'ms',
        icon: 'timer',
        description: 'Mean API response time across all endpoints.',
      },
      {
        label: 'P95 Request Latency',
        value: traffic.latency_ms.p95,
        unit: 'ms',
        icon: 'speed',
        description: '95th-percentile latency — only 5 % of requests are slower.',
      },
      {
        label: 'Total Evaluations',
        value: review.evaluations_total,
        icon: 'fact_check',
        description: 'Number of nurse-prompt evaluations completed end-to-end.',
      },
      {
        label: 'Avg Confidence',
        value: review.average_confidence,
        unit: '%',
        icon: 'verified',
        description: 'Mean LLM confidence score across all evaluated claims.',
      },
      {
        label: 'Avg Eval Latency',
        value: review.latency_ms.avg,
        unit: 'ms',
        icon: 'model_training',
        description: 'Mean end-to-end latency for a single LLM evaluation call.',
      },
      {
        label: 'Avg Retrieved Chunks',
        value: review.average_retrieved_chunks,
        icon: 'layers',
        description: 'Average number of vector-store chunks surfaced per evaluation.',
      },
    ];
  });

  verdictSegments = computed((): BarSegment[] => {
    const s = this.snapshot();
    if (!s) return [];
    const r = s.system.review;
    const total = r.evaluations_total || 1;
    return [
      { label: 'Valid', value: r.valid_total, color: '#22c55e', pct: (r.valid_total / total) * 100 },
      { label: 'Doubtful', value: r.doubtful_total, color: '#f59e0b', pct: (r.doubtful_total / total) * 100 },
      {
        label: 'Insuff. Evidence',
        value: r.insufficient_evidence_total,
        color: '#ef4444',
        pct: (r.insufficient_evidence_total / total) * 100,
      },
    ];
  });

  ragasEntries = computed((): Array<{ key: string; value: number; label: string; desc: string }> => {
    const s = this.snapshot();
    if (!s) return [];
    const r = s.ragas as Record<string, number | undefined>;

    const meta: Record<string, { label: string; desc: string }> = {
      faithfulness: {
        label: 'Faithfulness',
        desc: 'How factually consistent the generated answer is with the retrieved context. 1 = fully grounded.',
      },
      answer_relevancy: {
        label: 'Answer Relevancy',
        desc: 'How relevant the answer is to the original question. Penalises off-topic or incomplete responses.',
      },
      context_precision: {
        label: 'Context Precision',
        desc: 'Proportion of retrieved context chunks that are actually relevant. Measures retrieval precision.',
      },
      context_recall: {
        label: 'Context Recall',
        desc: 'Fraction of ground-truth relevant information present in the retrieved context. Measures retrieval coverage.',
      },
      context_utilization: {
        label: 'Context Utilisation',
        desc: 'How well the model uses the retrieved context in its answer. Low scores indicate ignored evidence.',
      },
    };

    return Object.entries(meta)
      .map(([key, { label, desc }]) => ({
        key,
        value: typeof r[key] === 'number' ? (r[key] as number) : 0,
        label,
        desc,
      }))
      .filter(e => e.value > 0);
  });

  modelEntries = computed(() => {
    const s = this.snapshot();
    if (!s) return [];
    return Object.entries(s.system.review.model_counts).map(([model, count]) => ({
      model,
      count,
    }));
  });

  recentClaims = computed(() => {
    const s = this.snapshot();
    if (!s) return [];
    return s.claims.slice(0, 10);
  });

  // ── Lifecycle ──────────────────────────────────────────────────────

  ngOnInit(): void {
    // Poll every 30 seconds; fire immediately. Use catchError so the stream never dies.
    this.pollSub = interval(30_000)
      .pipe(
        startWith(0),
        switchMap(() =>
          this.obsService.getSnapshot().pipe(
            catchError(() => {
              // Silently record that the backend is unreachable, but don't kill the stream
              this.backendReachable.set(false);
              return of(null);
            }),
          ),
        ),
      )
      .subscribe(data => {
        if (data) {
          this.snapshot.set(data);
          this.backendReachable.set(true);
          this.lastRefreshed.set(new Date());
        }
        this.loading.set(false);
      });
  }

  ngOnDestroy(): void {
    this.pollSub?.unsubscribe();
  }

  refresh(): void {
    this.loading.set(true);
    this.obsService.getSnapshot().subscribe({
      next: data => {
        this.snapshot.set(data);
        this.backendReachable.set(true);
        this.loading.set(false);
        this.lastRefreshed.set(new Date());
      },
      error: () => {
        this.loading.set(false);
        this.backendReachable.set(false);
      },
    });
  }

  verdictClass(verdict: string): string {
    if (verdict === 'valid') return 'verdict-valid';
    if (verdict === 'doubtful') return 'verdict-doubtful';
    return 'verdict-insufficient';
  }

  /** Gauge bar width capped at 100 % */
  gaugeWidth(value: number): string {
    return `${Math.min(100, Math.max(0, value * 100)).toFixed(1)}%`;
  }

  gaugeColor(value: number): string {
    if (value >= 0.75) return '#22c55e';
    if (value >= 0.5) return '#f59e0b';
    return '#ef4444';
  }

  /**
   * Restore the session for the selected claim and navigate to its review /
   * summary page so AI Review shows the correct PDF and criteria count.
   */
  viewClaim(claim: { namespace: string; diagnosis: string; claim_id: string; filename?: string; pdf_path?: string; [key: string]: unknown }): void {
    const filename = claim.filename || claim.claim_id;
    const pdfPath = claim.pdf_path || '';
    this.session.restoreClaim(claim.namespace, filename, pdfPath, claim.diagnosis);
    this.router.navigate(['/summary', claim.namespace]);
  }
}
