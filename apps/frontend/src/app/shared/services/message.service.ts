import { Message } from '@/models/chat';
import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs/internal/Observable';
import { environment } from 'src/environments/environment';

@Injectable({
  providedIn: 'root',
})
export class MessageService {
  public API_URL = `${environment.API_URL}/chat/`;

  constructor(private http: HttpClient) { }

  public getMessages(chat_id: string) : Observable<Message[]>{
    return this.http.get<Message[]>(`${this.API_URL}${chat_id}/messages`);
  }

  //   public sendMessage(message: string) {
  //   return this.http.post<Message>(this.API_URL, {message: message}).pipe(
  //     map(res => res)
  //   );
  // }
}
