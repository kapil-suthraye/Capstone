import { Component, computed, inject, signal } from '@angular/core';

import { RouterLink } from '@angular/router';

import { DashboardService } from '../../core/services/dashboard';

import { DashboardClaim } from '../../core/models/dashboard';

@Component({
  selector: 'app-dashboard',

  standalone: true,

  imports: [
    RouterLink
  ],

  templateUrl: './dashboard.html',

  styleUrl: './dashboard.scss'
})
export class DashboardComponent {

  private readonly service = inject(DashboardService);

  claims = signal<DashboardClaim[]>([]);

  completed = computed(() => this.claims().filter(claim => claim.status === 'Completed').length);

  doubtful = computed(() => this.claims().filter(claim => claim.verdict === 'doubtful').length);

  averageConfidence = computed(() => {
    const claims = this.claims().filter(claim => claim.confidence);

    if (!claims.length) return 0;

    return Math.round(
      claims.reduce((total, claim) => total + claim.confidence, 0) / claims.length
    );
  });

  constructor() {

    this.service.getClaims().subscribe({

      next: data => this.claims.set(data),

      error: err => console.error(err)

    });

  }

  verdictLabel(verdict: string): string {
    return verdict === 'insufficient_evidence'
      ? 'Insufficient'
      : verdict;
  }

}
