import { Component, inject, signal } from '@angular/core';
import { Router } from '@angular/router';

import { UploadService } from '../../core/services/upload';
import { SessionService } from '../../core/services/session';

@Component({
  selector: 'app-upload',
  standalone: true,
  templateUrl: './upload.html',
  styleUrl: './upload.scss',
})
export class UploadComponent {
  private readonly uploadService = inject(UploadService);
  private readonly router = inject(Router);
  private readonly session = inject(SessionService);

  uploading = signal(false);
  progressText = signal('Ready for medical record upload');
  uploadedFile = signal<File | null>(null);
  errorMessage = signal('');

  onFileSelected(event: Event): void {
    const input = event.target as HTMLInputElement;
    if (!input.files?.length) return;

    this.upload(input.files[0]);
  }

  upload(file: File): void {
    // Guard: prevent double-submit while a request is in flight
    if (this.uploading()) return;

    this.uploading.set(true);
    this.uploadedFile.set(file);
    this.errorMessage.set('');
    this.progressText.set('Uploading and indexing PDF...');

    this.uploadService.upload(file).subscribe({
      next: (response) => {
        this.session.setUpload(
          response.document_id,
          response.namespace,
          response.filename,
          response.pdf_path,
          response.detected_diagnosis,
        );
        this.router.navigate(['/review']);
      },
      error: () => {
        this.progressText.set('Upload failed');
        this.errorMessage.set(
          'The PDF could not be uploaded or indexed. Check backend logs and try again.',
        );
        this.uploading.set(false);
      },
    });
  }

  browse(fileInput: HTMLInputElement): void {
    fileInput.click();
  }
}
