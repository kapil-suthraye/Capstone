import {
  Component,
  computed,
  inject,
  signal
} from '@angular/core';

import { RouterLink } from '@angular/router';

import { EvidenceCardComponent } from '../../shared/components/evidence-card/evidence-card';
import { SuggestionCardComponent } from '../../shared/components/suggestion-card/suggestion-card';
import { PromptService } from '../../core/services/prompt';
import { ReviewService } from '../../core/services/review';
import { NursePrompt } from '../../core/models/prompt';
import { EvaluationResult } from '../../core/models/evaluation-result';
import { SessionService } from '../../core/services/session';

@Component({
  selector: 'app-review',
  standalone: true,
  imports: [
    RouterLink,
    EvidenceCardComponent,
    SuggestionCardComponent
  ],
  templateUrl: './review.html',
  styleUrl: './review.scss'
})
export class ReviewComponent {

  private readonly promptService = inject(PromptService);
  private readonly reviewService = inject(ReviewService);
  readonly session = inject(SessionService);

  prompts = signal<NursePrompt[]>([]);
  selectedPrompt = signal<NursePrompt | null>(null);
  result = signal<EvaluationResult | null>(null);
  reviewHistory = signal<EvaluationResult[]>([]);
  loading = signal(false);
  errorMessage = signal('');

  reviewedCount = computed(() => this.reviewHistory().length);

  claimReady = computed(() => Boolean(this.session.namespace));

  constructor() {
    this.loadPrompts();
    this.reviewHistory.set(this.session.evaluations);
  }

  loadPrompts(): void {
    this.promptService
      .getPrompts()
      .subscribe({
        next: data => this.prompts.set(data),
        error: () => this.errorMessage.set('Clinical prompts could not be loaded.')
      });
  }

  selectPrompt(prompt: NursePrompt): void {
    this.errorMessage.set('');

    if (!this.session.namespace) {
      this.errorMessage.set('Upload a medical record before running AI review.');
      return;
    }

    this.selectedPrompt.set(prompt);
    this.loading.set(true);

    this.reviewService.evaluate(
      this.session.namespace,
      prompt.prompt_id
    ).subscribe({
      next: result => {
        this.result.set(result);
        this.session.addEvaluation(result);
        this.reviewHistory.set(this.session.evaluations);
        this.loading.set(false);
      },
      error: () => {
        this.errorMessage.set('The AI review failed. Check backend logs and retry.');
        this.loading.set(false);
      }
    });
  }

  verdictLabel(verdict: string): string {
    return verdict === 'insufficient_evidence'
      ? 'Insufficient evidence'
      : verdict;
  }

}
