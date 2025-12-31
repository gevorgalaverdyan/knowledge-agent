from models.chat import Chat
from models.message import Message
from core.db import engine
Chat.metadata.create_all(bind=engine)
Message.metadata.create_all(bind=engine)
