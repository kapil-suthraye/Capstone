import { Component, inject, signal } from '@angular/core';

import { UploadService } from '../../core/services/upload';

import { SessionService } from '../../core/services/session';
import { Router } from '@angular/router';

@Component({
  selector: 'app-upload',

  standalone: true,

  templateUrl: './upload.html',

  styleUrl: './upload.scss'
})
export class UploadComponent {

  constructor(

    private uploadService:UploadService,

    private router:Router,

    private session:SessionService

){}

  // private readonly uploadService = inject(UploadService);

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
      
      next:(response)=>{

     this.session.documentId = response.document_id;

    this.session.namespace = response.namespace;

    this.session.filename = response.filename;

    this.session.pdfPath = response.pdf_path;

    console.log('Upload Response', response);

    console.log('Namespace Saved', this.session.namespace);

    this.router.navigate(['/review']);

}
      ,

      error: (err) => {

        console.error(err);

        this.progressText.set('Upload Failed');

        this.uploading.set(false);

      }

    });

  }

}