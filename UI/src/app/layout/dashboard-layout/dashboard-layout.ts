import { Component } from '@angular/core';
import { RouterOutlet } from '@angular/router';

import { SidebarComponent } from '../sidebar/sidebar';
import { HeaderComponent } from '../header/header';

@Component({
  selector: 'app-dashboard-layout',

  standalone: true,

  imports: [
    RouterOutlet,
    SidebarComponent,
    HeaderComponent
  ],

  templateUrl: './dashboard-layout.html',

  styleUrl: './dashboard-layout.scss'
})
export class DashboardLayoutComponent {}