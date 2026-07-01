import { ComponentFixture, TestBed } from '@angular/core/testing';

import { WorkflowStepper } from './workflow-stepper';

describe('WorkflowStepper', () => {
  let component: WorkflowStepper;
  let fixture: ComponentFixture<WorkflowStepper>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [WorkflowStepper],
    }).compileComponents();

    fixture = TestBed.createComponent(WorkflowStepper);
    component = fixture.componentInstance;
    await fixture.whenStable();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
