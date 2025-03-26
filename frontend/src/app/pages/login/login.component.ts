import { Component } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import {Router} from '@angular/router';
import Web3 from 'web3';
import { endPoint, LOGIN } from '../../constants/api-constants';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css']
})
export class LoginComponent {
  web3: Web3 | undefined;
  userAddress: string | null = null;

  constructor(private http: HttpClient, private router: Router) {  
    this.initWeb3();
  }

  async initWeb3() {
    if ((window as any).ethereum) {
      this.web3 = new Web3((window as any).ethereum);
      
      try {
        const accounts = await this.web3.eth.getAccounts();
        if (accounts.length > 0) {
          this.userAddress = accounts[0]; 
        } else {
          await (window as any).ethereum.request({ method: 'eth_requestAccounts' });
          const newAccounts = await this.web3.eth.getAccounts();
          this.userAddress = newAccounts[0];
        }
      } catch (error) {
        console.error('User denied MetaMask access', error);
      }
    } else {
      console.error('MetaMask not detected!');
      alert('MetaMask is required to login.');
    }
  }
  
  loginWithMetaMask() {
    if (!this.userAddress) {
      alert('Please connect MetaMask.');
      return;
    }
  
    const apiUrl = `${endPoint}${LOGIN}`;
    const userData = { user_address: this.userAddress };  // ✅ Use correct key
  
    this.http.post<{ user_address: string; role: string; success: boolean }>(apiUrl, userData)
      .subscribe({
        next: (response) => {
          if (response.success) {  // ✅ Check success flag
            document.cookie = `user_address=${response.user_address}; path=/`;  // ✅ Set cookie
            alert('Login successful!');  
            this.router.navigate(['/']); 
          } else {
            alert('Login failed. Please try again.');
          }
        },
        error: (error) => {
          console.error('Login failed:', error);
          alert('Login failed. Please try again.');
        }
      });
  }
  
}
