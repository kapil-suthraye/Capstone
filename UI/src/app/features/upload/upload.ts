import { Component, inject, signal } from '@angular/core';

import { UploadService } from '../../core/services/upload';

@Component({
  selector: 'app-upload',

  standalone: true,

  templateUrl: './upload.html',

  styleUrl: './upload.scss'
})
export class UploadComponent {

  private readonly uploadService = inject(UploadService);

  uploading = signal(false);

  progressText = signal('Drop a PDF or browse');

  uploadedFile = signal<File | null>(null);

  onFileSelected(event: Event): void {

    const input = event.target as HTMLInputElement;

    if (!input.files?.length) return;

    const file = input.files[0];

    this.uploadedFile.set(file);

    this.upload(file);

  }

  upload(file: File): void {

    this.uploading.set(true);

    this.progressText.set('Uploading PDF...');

    this.uploadService.upload(file).subscribe({

      next: (response) => {

        console.log(response);

        this.progressText.set('Upload Complete');

        this.uploading.set(false);

      },

      error: (err) => {

        console.error(err);

        this.progressText.set('Upload Failed');

        this.uploading.set(false);

      }

    });

  }

}