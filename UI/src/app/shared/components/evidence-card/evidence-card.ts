import {
  Component,
  EventEmitter,
  Input,
  Output
} from '@angular/core';

import { EvaluationResult } from '../../../core/models/evaluation-result';

@Component({
  selector: 'app-evidence-card',
  standalone: true,
  templateUrl: './evidence-card.html',
  styleUrl: './evidence-card.scss'
})
export class EvidenceCardComponent {

  @Input({ required: true })
  result!: EvaluationResult;

  @Output()
  openEvidence = new EventEmitter<number>();

  evidenceKey(index: number): string {
    const evidence = this.result.supporting_evidence[index];
    return evidence.chunk_id || `${evidence.page}-${evidence.heading}-${index}`;
  }

}
