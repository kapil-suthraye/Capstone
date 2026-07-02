import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-workflow-stepper',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './workflow-stepper.html',
  styleUrls: ['./workflow-stepper.scss']
})
export class WorkflowStepperComponent {

  steps = [

    'Upload PDF',

    'AI Review',

    'Evidence',

    'Suggestion'

  ];

}