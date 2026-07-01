import { Component, inject, signal } from '@angular/core';

import { DashboardService } from '../../core/services/dashboard';

import { DashboardClaim } from '../../core/models/dashboard';

@Component({
  selector: 'app-dashboard',

  standalone: true,

  templateUrl: './dashboard.html',

  styleUrl: './dashboard.scss'
})
export class DashboardComponent {

  private readonly service = inject(DashboardService);

  claims = signal<DashboardClaim[]>([]);

  constructor() {

    this.service.getClaims().subscribe({

      next: data => this.claims.set(data),

      error: err => console.error(err)

    });

  }

}