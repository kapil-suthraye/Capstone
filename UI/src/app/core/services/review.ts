import { Injectable, inject } from '@angular/core';

import { Observable } from 'rxjs';

import { ApiService } from './api';

import { EvaluationResult } from '../models/evaluation-result';

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

}