import { ComponentFixture, TestBed } from '@angular/core/testing';

import { UtilitiesAnimationComponent } from './utilities-animation.component';

describe('UtilitiesAnimationComponent', () => {
  let component: UtilitiesAnimationComponent;
  let fixture: ComponentFixture<UtilitiesAnimationComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [UtilitiesAnimationComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(UtilitiesAnimationComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
