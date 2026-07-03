import { Routes } from '@angular/router';

export const routes: Routes = [
  {
    path: '',
    loadComponent: () =>
      import('./layout/dashboard-layout/dashboard-layout').then(
        m => m.DashboardLayoutComponent,
      ),
    children: [
      {
        path: '',
        redirectTo: 'dashboard',
        pathMatch: 'full',
      },
      {
        path: 'dashboard',
        loadComponent: () =>
          import('./features/dashboard/dashboard').then(
            m => m.DashboardComponent,
          ),
      },
      {
        path: 'upload',
        loadComponent: () =>
          import('./features/upload/upload').then(m => m.UploadComponent),
      },
      {
        path: 'review',
        loadComponent: () =>
          import('./features/review/review').then(m => m.ReviewComponent),
      },
      {
        path: 'summary',
        loadComponent: () =>
          import('./features/claim-summary/claim-summary').then(
            m => m.ClaimSummaryComponent,
          ),
      },
      {
        path: 'summary/:namespace',
        loadComponent: () =>
          import('./features/claim-summary/claim-summary').then(
            m => m.ClaimSummaryComponent,
          ),
      },
      {
        path: 'observability',
        loadComponent: () =>
          import('./features/observability/observability').then(
            m => m.ObservabilityComponent,
          ),
      },
    ],
  },
];
