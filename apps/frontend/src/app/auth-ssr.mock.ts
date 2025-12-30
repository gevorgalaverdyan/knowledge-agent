import { Injectable } from '@angular/core';
import { of } from 'rxjs';

@Injectable()
export class AuthServiceMock {
  isAuthenticated$ = of(false);
  user$ = of(null);
  isLoading$ = of(false);
  loginWithRedirect() { return of(void 0); }
  logout() { return; }
}