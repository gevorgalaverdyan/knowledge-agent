export type Message = {
  id: string;
  text: string;
  chat_id: string;
  created_at: Date;
  sent_by: 'user' | 'system';
};

export type Chat = {
  id: string;
  chat_title: string;
  created_at: Date;
};