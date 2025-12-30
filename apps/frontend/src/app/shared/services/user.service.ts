import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs/internal/Observable';

@Injectable({
  providedIn: 'root',
})
export class UserService {
  public API_URL = 'http://localhost:8000/user/';

  constructor(private http: HttpClient) { }

  public getUser() : Observable<any>{
    return this.http.get<any>(`${this.API_URL}profile`);
  }
}
