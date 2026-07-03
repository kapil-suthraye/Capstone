import { Injectable, inject } from '@angular/core';
import { HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';

import { ApiService } from './api';
import { NursePrompt } from '../models/prompt';

@Injectable({
  providedIn: 'root',
})
export class PromptService {
  private readonly api = inject(ApiService);

  /**
   * Fetch clinical prompts from the backend.
   *
   * When `diagnosis` is provided the API filters prompts by their
   * sheet / job-aid using fuzzy matching and falls back to all prompts
   * when no match is found — so the caller never needs to handle an empty list.
   */
  getPrompts(diagnosis?: string | null): Observable<NursePrompt[]> {
    if (diagnosis) {
      return this.api.getWithParams<NursePrompt[]>('prompts', new HttpParams().set('diagnosis', diagnosis));
    }
    return this.api.get<NursePrompt[]>('prompts');
  }
}
