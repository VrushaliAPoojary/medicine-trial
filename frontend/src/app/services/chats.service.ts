import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { endPoint, REQUESTS } from '../constants/api-constants';

@Injectable({
  providedIn: 'root'
})
export class ChatsService {

  private apiUrl = `${endPoint}${REQUESTS}`;

  constructor(private http: HttpClient) {}

  getRequests(): Observable<any> {
    return this.http.get<any>(this.apiUrl);
  }

  
}
