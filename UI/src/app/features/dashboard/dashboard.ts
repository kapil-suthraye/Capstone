import { Component, DestroyRef, computed, inject, signal } from '@angular/core';
import { takeUntilDestroyed } from '@angular/core/rxjs-interop';
import { Router, RouterLink } from '@angular/router';

import { DashboardService } from '../../core/services/dashboard';
import { SessionService } from '../../core/services/session';
import { DashboardClaim } from '../../core/models/dashboard';

@Component({
  selector: 'app-dashboard',
  standalone: true,
  imports: [RouterLink],
  templateUrl: './dashboard.html',
  styleUrl: './dashboard.scss',
})
export class DashboardComponent {
  private readonly service = inject(DashboardService);
  private readonly session = inject(SessionService);
  private readonly router = inject(Router);
  private readonly destroyRef = inject(DestroyRef);

  claims = signal<DashboardClaim[]>([]);
  loading = signal(true);
  errorMessage = signal('');

  completed = computed(() =>
    this.claims().filter(c => c.status === 'Completed').length,
  );
  doubtful = computed(() =>
    this.claims().filter(c => c.verdict === 'doubtful').length,
  );
  averageConfidence = computed(() => {
    const withConfidence = this.claims().filter(c => c.confidence);
    if (!withConfidence.length) return 0;
    return Math.round(
      withConfidence.reduce((total, c) => total + c.confidence, 0) /
        withConfidence.length,
    );
  });

  constructor() {
    this.service
      .getClaims()
      .pipe(takeUntilDestroyed(this.destroyRef))
      .subscribe({
        next: data => {
          this.claims.set(data);
          this.loading.set(false);
        },
        error: () => {
          this.errorMessage.set('Could not load claims. Check backend connection and refresh.');
          this.loading.set(false);
        },
      });
  }

  /** Restore session state for a claim and navigate to its summary page */
  viewClaim(claim: DashboardClaim): void {
    this.session.restoreClaim(
      claim.namespace,
      claim.filename || claim.claim_id,
      claim.pdf_path || '',
      claim.detected_diagnosis ?? null,
    );
    this.router.navigate(['/summary', claim.namespace]);
  }

  verdictLabel(verdict: string): string {
    return verdict === 'insufficient_evidence' ? 'Insufficient' : verdict;
  }
}
