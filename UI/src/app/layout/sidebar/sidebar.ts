import { Component, signal } from '@angular/core';

import { RouterLink, RouterLinkActive } from '@angular/router';

@Component({

selector:'app-sidebar',

standalone:true,

imports:[
RouterLink,
RouterLinkActive
],

templateUrl:'./sidebar.html',

styleUrl:'./sidebar.scss'

})

export class SidebarComponent{

menu = signal([

  {
    icon: 'dashboard',
    title: 'Dashboard',
    route: '/dashboard'
  },

  {
    icon: 'upload_file',
    title: 'Upload PDF',
    route: '/upload'
  },

  {
    icon: 'fact_check',
    title: 'AI Review',
    route: '/review'
  },

  {
    icon: 'summarize',
    title: 'Claim Summary',
    route: '/summary'
  }
  // ,

  // {
  //   icon: 'monitoring',
  //   title: 'Observability',
  //   route: '/observability'
  // }

]);

}
