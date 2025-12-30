import { Component, inject, Input, PLATFORM_ID } from '@angular/core';
import { ZardIconComponent } from '../icon/icon.component';
import { HeaderComponent } from '../layout/header.component';
import { ZardDarkMode } from '@/shared/services/dark-mode';
import { AsyncPipe, isPlatformBrowser } from '@angular/common';
import { AuthService } from '@auth0/auth0-angular';
import { ZardButtonComponent } from '../button/button.component';

@Component({
  selector: 'app-navbar',
  imports: [HeaderComponent, ZardIconComponent, ZardButtonComponent, AsyncPipe],
  templateUrl: './navbar.html',
})
export class Navbar {
  @Input() auth: AuthService = inject(AuthService);
  private platformId = inject(PLATFORM_ID);

  private readonly darkModeService = inject(ZardDarkMode);

  toggleTheme(): void {
    this.darkModeService.toggleTheme();
  }

  login() {
    if (isPlatformBrowser(this.platformId)) {
      this.auth.loginWithRedirect();
    }
  }

  logout() {
    if (isPlatformBrowser(this.platformId)) {
      this.auth.logout();
    }
  }
}
