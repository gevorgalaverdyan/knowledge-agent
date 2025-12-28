import { Component, inject, Input, OnInit, OnChanges, SimpleChanges, signal } from '@angular/core';
import { ZardCardComponent } from '../card/card.component';
import { MarkdownComponent } from 'ngx-markdown';
import { ZardSkeletonComponent } from '../skeleton/skeleton.component';
import { MessageService } from '@/shared/services/message.service';
import { Message } from '@/models/chat';
import { DatePipe } from '@angular/common';

@Component({
  selector: 'app-message',
  imports: [ZardCardComponent, ZardSkeletonComponent, MarkdownComponent, DatePipe],
  templateUrl: './message.component.html',
})
export class MessageComponent implements OnInit, OnChanges {
  @Input() chat_id: string = '';
  messageService = inject(MessageService);
  loading = signal(false);
  messages = signal<Message[]>([]);

  ngOnInit() {
    this.fetchMessages();
  }

  ngOnChanges(changes: SimpleChanges) {
    if (changes['chat_id'] && !changes['chat_id'].firstChange) {
      this.fetchMessages();
    }
  }

  fetchMessages() {
    if (!this.chat_id) return;
    this.loading.set(true);
    this.messageService.getMessages(this.chat_id).subscribe((data: any) => {
      this.messages.set(data.messages);
      this.loading.set(false);
    });
  }
}
