import { Component, Input } from '@angular/core';

@Component({
  selector: 'app-company-products',
  imports: [],
  templateUrl: './company-products.component.html',
  styleUrl: './company-products.component.css'
})
export class CompanyProductsComponent {
  @Input() companyProductData: any; 
}
