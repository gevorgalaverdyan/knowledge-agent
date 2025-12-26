import { Component, signal } from '@angular/core';
import { LayoutComponent } from './shared/components/layout/layout.component';
import { ZardIconComponent } from './shared/components/icon/icon.component';
import { SidebarComponent, SidebarGroupComponent, SidebarGroupLabelComponent } from './shared/components/layout/sidebar.component';
import { ZardButtonComponent } from './shared/components/button/button.component';
import { Navbar } from './shared/components/navbar/navbar';
import { Footer } from './shared/components/footer/footer';
import { ContentComponent } from './shared/components/layout/content.component';
import { ZardInputGroupComponent } from './shared/components/input-group/input-group.component';
import { Chat } from './models/chat';
import { MarkdownComponent } from 'ngx-markdown';
import { ZardCardComponent } from './shared/components/card/card.component';

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
    ZardCardComponent,
    MarkdownComponent
  ],
  templateUrl: './app.html',
  styleUrl: './app.css'
})
export class App {
  chats: Chat[] = [
    {
      chatTitle: 'Chat1',
      messages:
        [{
          text: `## Lorem Ipsum Section One

          Lorem ipsum dolor sit amet, **consectetur adipiscing elit**. 
          Sed non risus. Suspendisse lectus tortor, dignissim sit amet, 
          *adipiscing nec*, ultricies sed, dolor.

          - Lorem ipsum dolor sit amet
          - Consectetur adipiscing elit
          - Integer nec odio
          - Praesent libero`
        },
        {
          text: `## Lorem Ipsum Section Two

      ### Subheading

      Lorem ipsum dolor sit amet, consectetur adipiscing elit.
      Vestibulum lacinia arcu eget nulla.

      > Lorem ipsum dolor sit amet, consectetur adipiscing elit.
      > Integer nec odio. Praesent libero. Sed cursus ante dapibus diam.`
        }]
    },
    {
      chatTitle: 'Chat2',
      messages:
        [{
          text: `
          If you want, I can:
          - generate a **downloadable file**
          - make it **much longer**
          - or tailor it for **README / docs / UI placeholders**
          `
        }]
    }
  ]
}
