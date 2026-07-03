import { Component, DestroyRef, computed, effect, inject, signal } from '@angular/core';
import { takeUntilDestroyed, toSignal } from '@angular/core/rxjs-interop';
import { ActivatedRoute, RouterLink } from '@angular/router';
import { map } from 'rxjs';

import { ClaimSummary } from '../../core/models/claim-summary';
import { ReviewService } from '../../core/services/review';
import { SessionService } from '../../core/services/session';

@Component({
  selector: 'app-claim-summary',
  standalone: true,
  imports: [RouterLink],
  templateUrl: './claim-summary.html',
  styleUrl: './claim-summary.scss',
})
export class ClaimSummaryComponent {
  private readonly route = inject(ActivatedRoute);
  private readonly reviewService = inject(ReviewService);
  private readonly session = inject(SessionService);
  private readonly destroyRef = inject(DestroyRef);

  summary = signal<ClaimSummary | null>(null);
  loading = signal(false);
  errorMessage = signal('');

  private readonly routeNamespace = toSignal(
    this.route.paramMap.pipe(map(p => p.get('namespace') ?? '')),
    { initialValue: this.route.snapshot.paramMap.get('namespace') ?? '' },
  );

  readonly namespace = computed(
    () => this.routeNamespace() || this.session.namespace(),
  );

  constructor() {
    effect(() => {
      this.load(this.namespace());
    });
  }

  private load(namespace: string): void {
    if (!namespace) {
      this.errorMessage.set(
        'No claim is selected. Upload or open a reviewed claim first.',
      );
      return;
    }

    this.loading.set(true);
    this.errorMessage.set('');
    this.summary.set(null);

    this.reviewService
      .getSummary(namespace)
      // destroyRef passed explicitly because load() is called from effect(), not constructor
      .pipe(takeUntilDestroyed(this.destroyRef))
      .subscribe({
        next: s => {
          this.summary.set(s);
          this.loading.set(false);
        },
        error: () => {
          this.errorMessage.set(
            'Claim summary is not available yet. Run at least one AI review criterion.',
          );
          this.loading.set(false);
        },
      });
  }

  verdictLabel(verdict: string): string {
    return verdict === 'insufficient_evidence' ? 'Insufficient evidence' : verdict;
  }

  metric(value: number | null | undefined): string {
    return value == null ? '0.00' : value.toFixed(2);
  }
}
