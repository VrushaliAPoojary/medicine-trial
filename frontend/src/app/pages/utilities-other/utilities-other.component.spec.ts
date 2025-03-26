import { ComponentFixture, TestBed } from '@angular/core/testing';

import { UtilitiesOtherComponent } from './utilities-other.component';

describe('UtilitiesOtherComponent', () => {
  let component: UtilitiesOtherComponent;
  let fixture: ComponentFixture<UtilitiesOtherComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [UtilitiesOtherComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(UtilitiesOtherComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
