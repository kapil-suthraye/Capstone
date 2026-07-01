import { Injectable, inject } from '@angular/core';

import { Observable } from 'rxjs';

import { ObservabilitySnapshot } from '../models/observability';
import { ApiService } from './api';

@Injectable({
  providedIn: 'root'
})
export class ObservabilityService {

  private readonly api = inject(ApiService);

  getSnapshot(): Observable<ObservabilitySnapshot> {

    return this.api.get<ObservabilitySnapshot>('observability');

  }

}
