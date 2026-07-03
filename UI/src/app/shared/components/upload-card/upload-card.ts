import { Component, DestroyRef, inject, signal } from '@angular/core';
import { takeUntilDestroyed } from '@angular/core/rxjs-interop';

import { UploadService } from '../../../core/services/upload';

@Component({
  selector: 'app-upload-card',
  standalone: true,
  templateUrl: './upload-card.html',
  styleUrl: './upload-card.scss',
})
export class UploadCardComponent {
  private readonly service = inject(UploadService);
  private readonly destroyRef = inject(DestroyRef);

  uploading = signal(false);
  errorMessage = signal('');

  select(event: Event): void {
    const input = event.target as HTMLInputElement;
    const file = input.files?.[0];

    if (!file || this.uploading()) return;

    this.uploading.set(true);
    this.errorMessage.set('');

    this.service
      .upload(file)
      .pipe(takeUntilDestroyed(this.destroyRef))
      .subscribe({
        next: () => this.uploading.set(false),
        error: () => {
          this.errorMessage.set('Upload failed. Please try again.');
          this.uploading.set(false);
        },
      });
  }
}
