import { Component, inject, Input, OnInit, signal } from '@angular/core';
import { ZardCardComponent } from '../card/card.component';
import { MarkdownComponent } from 'ngx-markdown';
import { ZardSkeletonComponent } from '../skeleton/skeleton.component';
import { MessageService } from '@/shared/services/message.service';
import { Message } from '@/models/chat';

@Component({
  selector: 'app-message',
  imports: [ZardCardComponent, ZardSkeletonComponent, MarkdownComponent],
  templateUrl: './message.component.html',
})
export class MessageComponent implements OnInit {
  @Input() chat_id: string = '';
  messageService = inject(MessageService);
  loading: boolean = false;
  messages = signal<Message[]>([]);

  ngOnInit() {
    this.messageService.getMessages(this.chat_id).subscribe((data: any) => {
      this.messages.set(data.messages);
    });
  }
}
