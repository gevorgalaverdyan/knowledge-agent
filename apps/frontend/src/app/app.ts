import { Component, inject, OnInit, signal } from '@angular/core';
import { LayoutComponent } from './shared/components/layout/layout.component';
import { ZardIconComponent } from './shared/components/icon/icon.component';
import { SidebarComponent, SidebarGroupComponent, SidebarGroupLabelComponent } from './shared/components/layout/sidebar.component';
import { ZardButtonComponent } from './shared/components/button/button.component';
import { Navbar } from './shared/components/navbar/navbar';
import { Footer } from './shared/components/footer/footer';
import { ContentComponent } from './shared/components/layout/content.component';
import { ZardInputGroupComponent } from './shared/components/input-group/input-group.component';
import { Chat } from './models/chat';
import { ChatService } from './shared/services/chat.service';
import { MessageComponent } from './shared/components/message.component/message.component';
import { ZardTooltipModule } from './shared/components/tooltip/tooltip';
import { ZardSkeletonComponent } from './shared/components/skeleton/skeleton.component';

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
    ZardTooltipModule,
    ZardSkeletonComponent,
    Navbar,
    Footer,
    ContentComponent,
    MessageComponent,
  ],
  templateUrl: './app.html',
  styleUrl: './app.css'
})
export class App implements OnInit {
  chats = signal<Chat[]>([]);
  chatsService = inject(ChatService);
  selectedChatId = signal<string>('');

  ngOnInit() {
    this.chatsService.getChats().subscribe((data: any) => {
      this.chats.set(data.chats);
    });
  }
}
