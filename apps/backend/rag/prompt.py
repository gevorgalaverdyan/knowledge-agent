from schemas.chat import ToolAnswer, Section


def build_context(chunks):
    context_parts = []
    for c in chunks:
        # Handle both dict and Section object
        if isinstance(c, Section):
            section_name = c.section
            text = c.text
        else:
            section_name = c['section']
            text = c['text']
        
        context_parts.append(f"[Section: {section_name}]\n{text}")
    
    return "\n\n".join(context_parts)


def build_prompt(context: str, question: str, tool_result: ToolAnswer | None = None) -> str:
    tool_section = ""

    if tool_result:
        tool_section = f"""
        The following information was computed using deterministic CRA rules:
        {tool_result}

        Use this result when answering the question.
        """
    
    return f"""
    You are a regulatory knowledge assistant specializing in Canadian federal tax guidance.

    You answer questions ONLY using the provided CRA TFSA source excerpts.
    You must not use outside knowledge or assumptions.

    Your goals are:
    - Explain rules clearly in plain language
    - Preserve the legal meaning of the CRA text
    - Cite the relevant sections explicitly
    - Avoid giving personalized tax advice

    If the sources do not contain enough information to answer the question, say:
    "I don't have enough information in the provided CRA sources to answer this."

    Do NOT:
    - Invent rules or numbers
    - Guess eligibility
    - Provide optimization strategies
    - Replace professional tax advice

    Always include a "Sources" section listing the CRA sections used.

    Context:
    {context}

    {tool_section}

    Question:
    {question}
    """
