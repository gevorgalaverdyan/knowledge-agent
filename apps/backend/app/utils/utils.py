import re

def chunk_text(text: str):
    pattern = r"\[(.*?)\]"

    parts = re.split(pattern, text)

    chunks = []

    for i in range(1, len(parts), 2):
        section = parts[i].strip()
        content = parts[i + 1].strip()

        if content:
            chunks.append({
                "section": section,
                "text": content
            })

    return chunks

def extract_year(question: str) -> int:
    """
    Extracts a year from the question.
    Assumes the year refers to when the user turned 18.
    """
    match = re.search(r'\b20\d{2}\b', question)
    return int(match.group()) if match else -1

def format_chat_history(messages) -> str:
    formatted_messages = []
    for msg in messages:
        sender = "User" if msg.sent_by == "user" else "Assistant"
        formatted_messages.append(f"{sender}: {msg.text}")
    return "\n".join(formatted_messages)
