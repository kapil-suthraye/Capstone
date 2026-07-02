import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ClaimSummary } from './claim-summary';

describe('ClaimSummary', () => {
  let component: ClaimSummary;
  let fixture: ComponentFixture<ClaimSummary>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [ClaimSummary],
    }).compileComponents();

    fixture = TestBed.createComponent(ClaimSummary);
    component = fixture.componentInstance;
    await fixture.whenStable();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
