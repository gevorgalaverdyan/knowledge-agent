import { Component, signal } from '@angular/core';
import { LayoutComponent } from './shared/components/layout/layout.component';
import { ZardIconComponent } from './shared/components/icon/icon.component';
import { SidebarComponent, SidebarGroupComponent, SidebarGroupLabelComponent } from './shared/components/layout/sidebar.component';
import { ZardButtonComponent } from './shared/components/button/button.component';
import { Navbar } from './shared/components/navbar/navbar';
import { Footer } from './shared/components/footer/footer';
import { ContentComponent } from './shared/components/layout/content.component';
import { ZardSkeletonComponent } from './shared/components/skeleton/skeleton.component';
import { ZardInputGroupComponent } from './shared/components/input-group/input-group.component';

@Component({
  selector: 'app-root',
  imports: [
    LayoutComponent,
    SidebarComponent,
    SidebarGroupComponent,
    SidebarGroupLabelComponent,
    ZardButtonComponent,
    ZardIconComponent,
    ZardInputGroupComponent,
    Navbar,
    Footer,
    ContentComponent,
    ZardSkeletonComponent
  ],
  templateUrl: './app.html',
  styleUrl: './app.css'
})
export class App {
}
