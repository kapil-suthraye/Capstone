import { Component, Input } from '@angular/core';
import { MatCardModule } from '@angular/material/card';
import { NgClass } from '@angular/common';

@Component({
  selector: 'app-stat-card',
  standalone: true,
  imports: [MatCardModule, NgClass],
  templateUrl: './stat-card.html',
  styleUrls: ['./stat-card.scss'],
})
export class StatCardComponent {
  @Input() title = '';
  @Input() value = '';
  @Input() subtitle = '';
  @Input() icon = 'description';
  @Input() color: 'blue' | 'pink' = 'blue';
}
