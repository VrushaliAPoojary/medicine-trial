import { ComponentFixture, TestBed } from '@angular/core/testing';

import { UtilitiesBorderComponent } from './utilities-border.component';

describe('UtilitiesBorderComponent', () => {
  let component: UtilitiesBorderComponent;
  let fixture: ComponentFixture<UtilitiesBorderComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [UtilitiesBorderComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(UtilitiesBorderComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
