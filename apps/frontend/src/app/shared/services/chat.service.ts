import { Chat, Message } from '@/models/chat';
import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { environment } from 'src/environments/environment';

@Injectable({
  providedIn: 'root',
})
export class ChatService {
  public API_URL = `${environment.API_URL}/chat/`;
  
  constructor(private http: HttpClient) { }

  public getChats() : Observable<Chat[]>{
    return this.http.get<Chat[]>(`${this.API_URL}chats`);
  }

  public askChat(chat_id: string, message: string) : Observable<Message>{
    return this.http.post<Message>(`${this.API_URL}${chat_id}/message`, {}, { params: { question: message } });
  }

  public createChat(chat_title: string) : Observable<Chat>{
    return this.http.post<Chat>(`${this.API_URL}create`, {}, { params: { chat_title : chat_title } });
  }

  public deleteChat(chat_id: string) : Observable<any>{
    return this.http.delete<any>(`${this.API_URL}${chat_id}/delete`);
  }
}
