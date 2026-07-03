import { Component, DestroyRef, computed, effect, inject, signal } from '@angular/core';
import { takeUntilDestroyed } from '@angular/core/rxjs-interop';
import { RouterLink } from '@angular/router';

import { EvidenceCardComponent } from '../../shared/components/evidence-card/evidence-card';
import { SuggestionCardComponent } from '../../shared/components/suggestion-card/suggestion-card';
import { PromptService } from '../../core/services/prompt';
import { ReviewService } from '../../core/services/review';
import { SessionService } from '../../core/services/session';
import { NursePrompt } from '../../core/models/prompt';
import { EvaluationResult } from '../../core/models/evaluation-result';

@Component({
  selector: 'app-review',
  standalone: true,
  imports: [RouterLink, EvidenceCardComponent, SuggestionCardComponent],
  templateUrl: './review.html',
  styleUrl: './review.scss',
})
export class ReviewComponent {
  private readonly promptService = inject(PromptService);
  private readonly reviewService = inject(ReviewService);
  private readonly destroyRef = inject(DestroyRef);
  readonly session = inject(SessionService);

  prompts = signal<NursePrompt[]>([]);
  selectedPrompt = signal<NursePrompt | null>(null);
  result = signal<EvaluationResult | null>(null);
  loading = signal(false);
  errorMessage = signal('');
  /** True when the prompts shown are filtered by diagnosis (not the full library) */
  isFiltered = signal(false);

  reviewedCount = computed(() => this.session.evaluations().length);
  claimReady = computed(() => Boolean(this.session.namespace()));

  constructor() {
    // Watch for diagnosis changes (e.g., when user navigates from dashboard to review)
    // and reload prompts automatically so the filter is always current.
    effect(() => {
      const diagnosis = this.session.diagnosis();
      const namespace = this.session.namespace();
      // Trigger reload whenever diagnosis or namespace changes
      this.loadPrompts(diagnosis);
    });
  }

  private loadPrompts(diagnosis: string | null): void {
    this.promptService
      .getPrompts(diagnosis)
      .pipe(takeUntilDestroyed(this.destroyRef))
      .subscribe({
        next: data => {
          this.prompts.set(data);
          // Mark as filtered only when a diagnosis was requested AND the API
          // returned a non-empty subset (the backend falls back to all when
          // no match is found, so a match is indicated by a smaller list).
          this.isFiltered.set(Boolean(diagnosis && data.length > 0));
        },
        error: () => this.errorMessage.set('Clinical prompts could not be loaded.'),
      });
  }

  /** Clear the diagnosis filter and reload all prompts */
  showAllPrompts(): void {
    this.isFiltered.set(false);
    this.promptService
      .getPrompts()
      .pipe(takeUntilDestroyed(this.destroyRef))
      .subscribe({
        next: data => this.prompts.set(data),
        error: () => this.errorMessage.set('Clinical prompts could not be loaded.'),
      });
  }

  selectPrompt(prompt: NursePrompt): void {
    this.errorMessage.set('');
    this.result.set(null);

    if (!this.session.namespace()) {
      this.errorMessage.set('Upload a medical record before running AI review.');
      return;
    }

    this.selectedPrompt.set(prompt);
    this.loading.set(true);

    this.reviewService
      .evaluate(this.session.namespace(), prompt.prompt_id)
      .pipe(takeUntilDestroyed(this.destroyRef))
      .subscribe({
        next: res => {
          this.result.set(res);
          this.session.addEvaluation(res);
          this.loading.set(false);
        },
        error: () => {
          this.errorMessage.set('The AI review failed. Check backend logs and retry.');
          this.loading.set(false);
        },
      });
  }

  verdictLabel(verdict: string): string {
    return verdict === 'insufficient_evidence' ? 'Insufficient evidence' : verdict;
  }
}
