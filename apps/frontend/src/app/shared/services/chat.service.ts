import { Chat, Message } from '@/models/chat';
import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { map, Observable } from 'rxjs';

@Injectable({
  providedIn: 'root',
})
export class ChatService {

  public API_URL = 'https://localhost:8000/api/chat/';
  
  constructor(private http: HttpClient) { }

  public getChats() : Observable<Chat[]>{
    return this.http.get<Chat[]>(this.API_URL);
  }

  public sendMessage(message: string) {
    return this.http.post<Message>(this.API_URL, {message: message}).pipe(
      map(res => res)
    );
  }
}
