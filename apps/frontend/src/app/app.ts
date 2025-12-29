import { Component, inject, OnInit, signal, ViewChild } from '@angular/core';
import { FormsModule } from '@angular/forms';
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
import { ZardDividerComponent } from './shared/components/divider/divider.component';

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
    ZardDividerComponent,
    Navbar,
    Footer,
    ContentComponent,
    MessageComponent,
    FormsModule,
  ],
  templateUrl: './app.html',
  styleUrl: './app.css'
})
export class App implements OnInit {
  @ViewChild(MessageComponent) messageComponent!: MessageComponent;
  chats = signal<Chat[]>([]);
  chatsService = inject(ChatService);
  selectedChat = signal<Chat | null>(null);
  answering = signal<boolean>(false);
  message = '';

  ngOnInit() {
    this.chatsService.getChats().subscribe((data: any) => {
      this.chats.set(data.chats);
      this.selectedChat.set(data.chats.length > 0 ? data.chats[0] : null);
    });
  }

  askChat(message: string) {
    if (!this.selectedChat()) return;
    this.answering.set(true);
    this.chatsService.askChat(this.selectedChat()!.id, message).subscribe((data: any) => {
        this.messageComponent.fetchMessages(true);
        this.answering.set(false);
        this.message = '';
    });
  }
}
