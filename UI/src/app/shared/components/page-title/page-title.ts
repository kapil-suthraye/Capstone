import { Component, Input } from '@angular/core';

@Component({
  selector: 'app-page-title',
  standalone: true,
  templateUrl: './page-title.html',
  styleUrls: ['./page-title.scss']
})
export class PageTitleComponent {

  @Input() title = '';

  @Input() subtitle = '';

}