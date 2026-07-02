import { Injectable, inject } from '@angular/core';

import { Observable } from 'rxjs';

import { ApiService } from './api';

import { EvaluationResult } from '../models/evaluation-result';
import { ClaimSummary } from '../models/claim-summary';

@Injectable({
  providedIn: 'root'
})
export class ReviewService {

  private api = inject(ApiService);

  evaluate(
    namespace: string,
    promptId: string
  ): Observable<EvaluationResult> {

    return this.api.post<EvaluationResult>(
      'evaluate',
      {
        namespace: namespace,
        prompt_id: promptId
      }
    );

  }

  getSummary(namespace: string): Observable<ClaimSummary> {

    return this.api.get<ClaimSummary>(
      `claims/${namespace}/summary`
    );

  }

}
