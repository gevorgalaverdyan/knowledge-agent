export type Message = {
  id: string;
  text: string;
  created_at: Date;
};

export type Chat = {
  id: string;
  chatTitle: string;
  created_at: Date;
  messages: Message[];
};