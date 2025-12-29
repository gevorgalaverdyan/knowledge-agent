import { Chat, Message } from '@/models/chat';
import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root',
})
export class ChatService {
  public API_URL = 'http://localhost:8000/chat/';
  
  constructor(private http: HttpClient) { }

  public getChats() : Observable<Chat[]>{
    return this.http.get<Chat[]>(`${this.API_URL}chats`);
  }

  public askChat(chat_id: string, message: string) : Observable<Message>{
    console.log('Sending message to chat service:', { chat_id, message });
    return this.http.post<Message>(`${this.API_URL}${chat_id}/message`, {}, { params: { question: message } });
  }
}
