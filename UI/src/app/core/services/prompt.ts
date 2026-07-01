import { Injectable, inject } from '@angular/core';

import { ApiService } from './api';

import { NursePrompt } from '../models/prompt';

@Injectable({
  providedIn: 'root'
})
export class PromptService {

  private readonly api = inject(ApiService);

  getPrompts() {

    return this.api.get<NursePrompt[]>('prompts');

  }

}