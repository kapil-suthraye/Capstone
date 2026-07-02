import { ComponentFixture, TestBed } from '@angular/core/testing';

import { PageTitle } from './page-title';

describe('PageTitle', () => {
  let component: PageTitle;
  let fixture: ComponentFixture<PageTitle>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [PageTitle],
    }).compileComponents();

    fixture = TestBed.createComponent(PageTitle);
    component = fixture.componentInstance;
    await fixture.whenStable();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
