import {
  Component,
  computed,
  inject,
  signal
} from '@angular/core';

import { ActivatedRoute, RouterLink } from '@angular/router';

import { ClaimSummary } from '../../core/models/claim-summary';
import { ReviewService } from '../../core/services/review';
import { SessionService } from '../../core/services/session';

@Component({
  selector: 'app-claim-summary',
  standalone: true,
  imports: [
    RouterLink
  ],
  templateUrl: './claim-summary.html',
  styleUrl: './claim-summary.scss'
})
export class ClaimSummaryComponent {

  private readonly route = inject(ActivatedRoute);
  private readonly reviewService = inject(ReviewService);
  private readonly session = inject(SessionService);

  summary = signal<ClaimSummary | null>(null);
  loading = signal(false);
  errorMessage = signal('');

  namespace = computed(() => {
    return this.route.snapshot.paramMap.get('namespace') || this.session.namespace;
  });

  constructor() {
    this.load();
  }

  load(): void {
    const namespace = this.namespace();

    if (!namespace) {
      this.errorMessage.set('No claim is selected. Upload or open a reviewed claim first.');
      return;
    }

    this.loading.set(true);
    this.errorMessage.set('');

    this.reviewService.getSummary(namespace).subscribe({
      next: summary => {
        this.summary.set(summary);
        this.loading.set(false);
      },
      error: () => {
        this.errorMessage.set('Claim summary is not available yet. Run at least one AI review criterion.');
        this.loading.set(false);
      }
    });
  }

  verdictLabel(verdict: string): string {
    return verdict === 'insufficient_evidence'
      ? 'Insufficient evidence'
      : verdict;
  }

  metric(value: number | null | undefined): string {
    if (value === null || value === undefined) return '0.00';

    return value.toFixed(2);
  }

}
