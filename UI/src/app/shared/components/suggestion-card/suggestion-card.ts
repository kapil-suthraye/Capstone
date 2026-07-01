import {
  Component,
  Input
} from '@angular/core';

import {
  EvaluationResult
} from '../../../core/models/evaluation-result';

@Component({
  selector: 'app-suggestion-card',
  standalone: true,
  templateUrl: './suggestion-card.html',
  styleUrl: './suggestion-card.scss'
})
export class SuggestionCardComponent {

  @Input({ required: true })
  result!: EvaluationResult;

  verdictLabel(): string {
    return this.result.verdict === 'insufficient_evidence'
      ? 'Insufficient evidence'
      : this.result.verdict;
  }

  metric(value: number | null | undefined): string {
    if (value === null || value === undefined) return '0.00';

    return value.toFixed(2);
  }

}
