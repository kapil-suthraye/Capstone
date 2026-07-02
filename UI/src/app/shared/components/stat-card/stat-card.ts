import { Component, Input } from '@angular/core';
import { CommonModule } from '@angular/common';
import { MatCardModule } from '@angular/material/card';

@Component({
  selector: 'app-stat-card',
  standalone: true,
  imports: [CommonModule, MatCardModule],
  templateUrl: './stat-card.html',
  styleUrls: ['./stat-card.scss']
})
export class StatCardComponent {

  @Input() title = '';

  @Input() value = '';

  @Input() subtitle = '';

  @Input() icon = 'description';

  @Input() color: 'blue' | 'pink' = 'blue';

}