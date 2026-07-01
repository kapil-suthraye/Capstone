import { Injectable } from '@angular/core';

import { EvaluationResult } from '../models/evaluation-result';

@Injectable({
  providedIn: 'root'
})
export class SessionService {

  documentId = '';

  namespace = '';

  filename = '';

  pdfPath = '';

  evaluations: EvaluationResult[] = [];

  addEvaluation(result: EvaluationResult): void {
    this.evaluations = [
      ...this.evaluations.filter(item => item.prompt_id !== result.prompt_id),
      result
    ];
  }

  clear(): void {
    this.documentId = '';
    this.namespace = '';
    this.filename = '';
    this.pdfPath = '';
    this.evaluations = [];
  }

}
