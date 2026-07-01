import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root'
})
export class SessionService {

  documentId = '';

  namespace = '';

  filename = '';

  pdfPath = '';

  clear(): void {
    this.documentId = '';
    this.namespace = '';
    this.filename = '';
    this.pdfPath = '';
  }

}