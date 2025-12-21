from agents.tfsa_agent import TFSAAagent
from schemas.chat import CalculationAnswer
from rag.prompt import build_context, build_prompt

agent = TFSAAagent()

def ask_llm(chunks, question: str, client, model: str):
    agent_result = agent.handle_question(question)

    if agent_result:
        if isinstance(agent_result, CalculationAnswer):
            sections = agent_result.sections

            context = build_context(sections)

            prompt = build_prompt(context=context, question=question, tool_result=agent_result)

            response = client.models.generate_content(
                model=model,
                contents=prompt
            )

            return response.text

    context = build_context(chunks)
    prompt = build_prompt(context, question)

    response = client.models.generate_content(
        model=model,
        contents=prompt
    )

    return response.text
