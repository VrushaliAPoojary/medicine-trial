import { ComponentFixture, TestBed } from '@angular/core/testing';

import { UtilitiesColorComponent } from './utilities-color.component';

describe('UtilitiesColorComponent', () => {
  let component: UtilitiesColorComponent;
  let fixture: ComponentFixture<UtilitiesColorComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [UtilitiesColorComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(UtilitiesColorComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
