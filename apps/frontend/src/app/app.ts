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
import { ZardDialogService } from './shared/components/dialog/dialog.service';
import { CreateChatDialog, iDialogData } from "./shared/components/create-chat-dialog/create-chat-dialog";

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
  private chatsService = inject(ChatService);
  private dialogService = inject(ZardDialogService);
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

  openDialog() {
    this.dialogService.create({
      zTitle: 'Create New Chat',
      zDescription: `Ask your question. Click save when you're done.`,
      zContent: CreateChatDialog,
      zData: {
        chat_title: '',
      } as iDialogData,
      zOkText: 'Save changes',
      zOnOk: instance => {
        console.log('Form submitted:', instance.form.value);
        if (instance.form.value.chat_title) {
          this.chatsService.createChat(instance.form.value.chat_title).subscribe((newChat: any) => {
            this.chats.update(chats => [...chats, newChat.chat]);
            this.selectedChat.set(newChat);
          });
        }
      },
      zWidth: '425px',
    });
  }

  deleteChat(chat_id: string) {
    if(!chat_id) return;
    this.chatsService.deleteChat(chat_id).subscribe(() => {
      this.chats.update(chats => chats.filter(chat => chat.id !== chat_id));
      if (this.selectedChat() && this.selectedChat()!.id === chat_id) {
        this.selectedChat.set(this.chats().length > 0 ? this.chats()[0] : null);
      }
    });
  }
}
