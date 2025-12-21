from rag.prompt import build_context, build_prompt

def ask_llm(chunks, question, client, model):
    context = build_context(chunks)
    prompt = build_prompt(context, question)

    response = client.models.generate_content(
        model=model,
        contents=prompt
    )

    return response.text
