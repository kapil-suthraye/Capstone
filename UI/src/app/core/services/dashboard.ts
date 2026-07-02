import { Injectable, inject } from '@angular/core';

import { ApiService } from './api';

import { DashboardClaim } from '../models/dashboard';

@Injectable({
  providedIn: 'root'
})
export class DashboardService {

  private readonly api = inject(ApiService);

  getClaims() {

    return this.api.get<DashboardClaim[]>('dashboard');

  }

}