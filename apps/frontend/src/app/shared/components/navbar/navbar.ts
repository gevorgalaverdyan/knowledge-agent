import { Component, inject } from '@angular/core';
import { ZardIconComponent } from '../icon/icon.component';
import { HeaderComponent } from '../layout/header.component';
import { ZardDarkMode } from '@/shared/services/dark-mode';

@Component({
  selector: 'app-navbar',
  imports: [HeaderComponent, ZardIconComponent],
  templateUrl: './navbar.html',
})
export class Navbar {
  private readonly darkModeService = inject(ZardDarkMode);
 
  toggleTheme(): void {
    this.darkModeService.toggleTheme();
  }
}
