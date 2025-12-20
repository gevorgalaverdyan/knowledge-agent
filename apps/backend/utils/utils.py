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