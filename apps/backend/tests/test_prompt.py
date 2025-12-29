"""
Unit tests for prompt building in rag/prompt.py
"""
import pytest
from rag.prompt import build_context, build_prompt
from schemas.chat import Section, CalculationAnswer, CalculationToolResult


class TestBuildContext:
    """Tests for build_context function"""
    
    def test_build_context_with_dict_chunks(self):
        """Test building context from dictionary chunks"""
        chunks = [
            {"section": "Eligibility", "text": "You must be 18 or older."},
            {"section": "Contributions", "text": "Annual limits apply."}
        ]
        
        context = build_context(chunks)
        
        assert "[Section: Eligibility]" in context
        assert "You must be 18 or older." in context
        assert "[Section: Contributions]" in context
        assert "Annual limits apply." in context
        assert "\n\n" in context
    
    def test_build_context_with_section_objects(self):
        """Test building context from Section objects"""
        sections = [
            Section(
                id="1",
                section="TFSA Basics",
                topic="Introduction",
                text="A TFSA is a registered savings account.",
                document="CRA",
                jurisdiction="Canada",
                year=2025
            ),
            Section(
                id="2",
                section="Contribution Limits",
                topic="Limits",
                text="Annual contribution limits are set by CRA.",
                document="CRA",
                jurisdiction="Canada",
                year=2025
            )
        ]
        
        context = build_context(sections)
        
        assert "[Section: TFSA Basics]" in context
        assert "A TFSA is a registered savings account." in context
        assert "[Section: Contribution Limits]" in context
        assert "Annual contribution limits are set by CRA." in context
    
    def test_build_context_empty_list(self):
        """Test building context with empty list"""
        chunks = []
        context = build_context(chunks)
        
        assert context == ""
    
    def test_build_context_single_chunk(self):
        """Test building context with single chunk"""
        chunks = [{"section": "Test", "text": "Test content"}]
        context = build_context(chunks)
        
        assert context == "[Section: Test]\nTest content"
    
    def test_build_context_formatting(self):
        """Test context formatting separates sections correctly"""
        chunks = [
            {"section": "Section 1", "text": "Content 1"},
            {"section": "Section 2", "text": "Content 2"},
            {"section": "Section 3", "text": "Content 3"}
        ]
        
        context = build_context(chunks)
        
        parts = context.split("\n\n")
        assert len(parts) == 3
        assert parts[0] == "[Section: Section 1]\nContent 1"
        assert parts[1] == "[Section: Section 2]\nContent 2"
        assert parts[2] == "[Section: Section 3]\nContent 3"


class TestBuildPrompt:
    """Tests for build_prompt function"""
    
    def test_build_prompt_basic(self):
        """Test building basic prompt without tool result"""
        context = "[Section: Test]\nTest content"
        question = "What is a TFSA?"
        
        prompt = build_prompt(context, question)
        
        assert "regulatory knowledge assistant" in prompt
        assert "CRA TFSA source excerpts" in prompt
        assert context in prompt
        assert question in prompt
        assert "Sources" in prompt
    
    def test_build_prompt_with_chat_history(self):
        """Test building prompt with chat history"""
        context = "[Section: Test]\nTest content"
        question = "What is a TFSA?"
        chat_history = "User: Hello\nAssistant: Hi there"
        
        prompt = build_prompt(context, question, chat_history=chat_history)
        
        assert "PREVIOUS CONVERSATION:" in prompt
        assert chat_history in prompt
    
    def test_build_prompt_with_tool_result(self):
        """Test building prompt with calculation tool result"""
        context = "[Section: Limits]\nAnnual limits apply."
        question = "What is my contribution room?"
        
        calculation = CalculationToolResult(
            total_contribution_room=50000,
            yearly_breakdown={2020: 6000, 2021: 6000},
            assumptions=["No contributions", "No withdrawals"]
        )
        
        tool_result = CalculationAnswer(
            type="calculation_result",
            sections=[],
            calculation=calculation
        )
        
        prompt = build_prompt(context, question, tool_result=tool_result)
        
        assert "computed using deterministic CRA rules" in prompt
        assert str(tool_result) in prompt
        assert "Use this result when answering" in prompt
    
    def test_build_prompt_instructions(self):
        """Test that prompt contains key instructions"""
        context = "Test context"
        question = "Test question"
        
        prompt = build_prompt(context, question)
        
        # Check for key instruction elements
        assert "ONLY using the provided CRA TFSA source excerpts" in prompt
        assert "not use outside knowledge" in prompt
        assert "plain language" in prompt
        assert "Cite the relevant sections" in prompt
        assert "NOT" in prompt.upper()
        assert "Invent rules" in prompt
    
    def test_build_prompt_fallback_message(self):
        """Test that prompt includes fallback message instruction"""
        context = ""
        question = "Unknown question"
        
        prompt = build_prompt(context, question)
        
        assert "don't have enough information" in prompt
    
    def test_build_prompt_warnings(self):
        """Test that prompt includes warnings about what NOT to do"""
        context = "Test"
        question = "Test"
        
        prompt = build_prompt(context, question)
        
        assert "Do NOT:" in prompt
        assert "Invent rules" in prompt
        assert "Guess eligibility" in prompt
        assert "optimization strategies" in prompt
        assert "professional tax advice" in prompt
    
    def test_build_prompt_with_all_parameters(self):
        """Test building prompt with all parameters"""
        context = "[Section: Test]\nTest content"
        question = "Test question"
        chat_history = "User: Hi\nAssistant: Hello"
        
        calculation = CalculationToolResult(
            total_contribution_room=10000,
            yearly_breakdown={2024: 7000},
            assumptions=["Test assumption"]
        )
        tool_result = CalculationAnswer(
            type="calculation_result",
            sections=[],
            calculation=calculation
        )
        
        prompt = build_prompt(context, question, tool_result=tool_result, chat_history=chat_history)
        
        assert context in prompt
        assert question in prompt
        assert chat_history in prompt
        assert str(tool_result) in prompt
        assert "PREVIOUS CONVERSATION:" in prompt
        assert "computed using deterministic CRA rules" in prompt
    
    def test_build_prompt_empty_chat_history(self):
        """Test that empty chat history is handled correctly"""
        context = "Test context"
        question = "Test question"
        chat_history = ""
        
        prompt = build_prompt(context, question, chat_history=chat_history)
        
        assert "PREVIOUS CONVERSATION:" in prompt
        assert question in prompt
