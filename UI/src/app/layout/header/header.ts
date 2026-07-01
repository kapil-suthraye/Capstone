import { Component, computed, inject, signal } from '@angular/core';

import { NavigationEnd, Router } from '@angular/router';

import { filter } from 'rxjs';

@Component({

selector:'app-header',

standalone:true,

imports:[],

templateUrl:'./header.html',

styleUrl:'./header.scss'

})

export class HeaderComponent{

private readonly router = inject(Router);

private readonly currentUrl = signal(this.router.url);

readonly title = computed(() => {
  const url = this.currentUrl();

  if (url.includes('upload')) return 'Upload Claim';
  if (url.includes('review')) return 'AI Review';
  if (url.includes('summary')) return 'Claim Summary';
  if (url.includes('observability')) return 'Observability';
  return 'Dashboard';
});

readonly subtitle = computed(() => {
  const url = this.currentUrl();

  if (url.includes('observability')) return 'Live system, model, and RAGAS metrics';
  if (url.includes('summary')) return 'Final adjudication view for the selected claim';
  if (url.includes('review')) return 'Evidence-first medical necessity review';
  if (url.includes('upload')) return 'Ingest a medical record and build retrieval context';
  return 'Medical AI Reviewer command center';
});

constructor(){
  this.router.events
    .pipe(filter((event): event is NavigationEnd => event instanceof NavigationEnd))
    .subscribe(event => this.currentUrl.set(event.urlAfterRedirects));
}

}
