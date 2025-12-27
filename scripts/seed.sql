CREATE EXTENSION IF NOT EXISTS "uuid-ossp";


INSERT INTO chats (id, chat_title)
VALUES ('0c10df15-c1c3-4d86-9e09-392ffcdc9cb8', 'Test Chat Session 1'),
       ('1e193920-9cdc-4607-acfe-21623f78ab41', 'Test Chat Session 2'),
       ('91275dd1-7808-44c2-939d-160f9e05107a', 'Test Chat Session 3');


INSERT INTO messages(id, chat_id, text, sent_by)
VALUES  ('18decab1-e095-4eba-a86b-363685b40455', '0c10df15-c1c3-4d86-9e09-392ffcdc9cb8', 'What is a tfsa account', 'USER'::messagesendertype),
        ('bf3f5743-baa8-44fc-9706-e2656eab755b', '0c10df15-c1c3-4d86-9e09-392ffcdc9cb8', '# TFSA ACCOUNT OVERVIEW

A TFSA (Tax-Free Savings Account) is a Canadian registered account 
that allows your money to grow tax-exempt. Despite its name, it 
functions as an investment "bucket" rather than just a savings account.

### KEY ADVANTAGES
* Tax-Free Earnings: You pay $0 tax on interest, dividends, or capital gains.
* Flexible Access: Withdraw funds at any time without paying tax or penalties.
* Contribution Room: For 2025, the annual limit is $7,000. Unused room rolls over annually.

### IMPORTANT RULE
If you withdraw money, you gain that contribution room back, 
but only on January 1st of the following year.', 'SYSTEM'::messagesendertype),
        ('446cdadf-4292-4fb8-bdb7-795ae4319e02', '1e193920-9cdc-4607-acfe-21623f78ab41', 'What are your business hours?', 'USER'::messagesendertype),
        ('20b5616d-91a3-4a47-a82d-2e6ba3b3e397', '1e193920-9cdc-4607-acfe-21623f78ab41', 'We are open from 9 AM to 5 PM, Monday to Friday.', 'SYSTEM'::messagesendertype),
        ('7dae6e86-1bb3-4d01-8fbe-7381ab9de9dd', '91275dd1-7808-44c2-939d-160f9e05107a', 'Can you tell me about your services?', 'USER'::messagesendertype),
        ('a33ef4e9-2ea4-433d-9d69-5056e3e60d13', '91275dd1-7808-44c2-939d-160f9e05107a', 'We offer a variety of services including...', 'SYSTEM'::messagesendertype);