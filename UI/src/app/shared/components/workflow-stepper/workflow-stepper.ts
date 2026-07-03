import { Component } from '@angular/core';

@Component({
  selector: 'app-workflow-stepper',
  standalone: true,
  imports: [],
  templateUrl: './workflow-stepper.html',
  styleUrls: ['./workflow-stepper.scss'],
})
export class WorkflowStepperComponent {
  steps = ['Upload PDF', 'AI Review', 'Evidence', 'Suggestion'];
}
