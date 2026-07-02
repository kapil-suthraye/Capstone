import { Routes } from '@angular/router';

import { DashboardLayoutComponent } from './layout/dashboard-layout/dashboard-layout';

import { DashboardComponent } from './features/dashboard/dashboard';

import { UploadComponent } from './features/upload/upload';

import { ReviewComponent } from './features/review/review';

import { ClaimSummaryComponent } from './features/claim-summary/claim-summary';

// import { ObservabilityComponent } from './features/observability/observability';

export const routes: Routes = [

  {
    path: '',

    component: DashboardLayoutComponent,

    children: [

      {
        path: '',
        redirectTo: 'dashboard',
        pathMatch: 'full'
      },

      {
        path: 'dashboard',
        component: DashboardComponent
      },

      {
        path: 'upload',
        component: UploadComponent
      },

      {
        path: 'review',
        component: ReviewComponent
      },

      {
        path: 'summary',
        component: ClaimSummaryComponent
      },

      {
        path: 'summary/:namespace',
        component: ClaimSummaryComponent
      }

      // {
      //   path: 'observability',
      //   component: ObservabilityComponent
      // }

    ]
  }

];
