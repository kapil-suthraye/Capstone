import { Injectable, inject } from '@angular/core';
import { Observable } from 'rxjs';

import { ApiService } from './api';
import { UploadResponse } from '../models/upload-response';

@Injectable({ providedIn: 'root' })
export class UploadService {
  private readonly api = inject(ApiService);

  upload(file: File): Observable<UploadResponse> {
    return this.api.upload(file);
  }
}
