import { CompanyService } from '../../services/company.service';
import { Router } from '@angular/router';
import { MessagesComponent } from '../../components/messages/messages.component';
import { RequestComponent } from '../../components/request/request.component';
import { CompanyComponent } from '../../components/company/company.component';
import { SidebarComponent } from '../../components/sidebar/sidebar.component';
import { FooterComponent } from '../../components/footer/footer.component';
import { Component } from '@angular/core';

@Component({
  selector: 'app-role-based',
  standalone: true,
  imports: [FooterComponent, SidebarComponent, CompanyComponent, MessagesComponent, RequestComponent],
  templateUrl: './role-based.component.html',
  styleUrl: './role-based.component.css'
})
export class RoleBasedComponent {


  ngOnInit() {
   
    // Fetch requests
    this.requestService.getRequests().subscribe({
      next: (data) => {
        this.requests = data;
      },
      error: (err) => {
        console.error('Error fetching requests:', err);
      }
    });
  }


 approveRequest() {
    alert("Role request approved!");
   
}

rejectRequest() {
    alert("Role request rejected!");

}

}
