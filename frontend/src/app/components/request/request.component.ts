import { Component, Input } from '@angular/core';

@Component({
  selector: 'app-request',
  imports: [],
  templateUrl: './request.component.html',
  styleUrl: './request.component.css'
})
export class RequestComponent {
  @Input() requests: any; 
}
