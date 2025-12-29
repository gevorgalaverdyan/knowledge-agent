import pytest
from unittest.mock import Mock, patch
from agents.tfsa_agent import TFSAAagent
from schemas.chat import CalculationAnswer, ToolError, CalculationToolResult, Section


class TestTFSAAagent:
    """Test cases for TFSAAagent."""

    def setup_method(self):
        """Set up test fixtures."""
        self.agent = TFSAAagent()

    def test_handle_contribution_question_with_year(self):
        """Should handle contribution question with year."""
        question = "What is my TFSA contribution room if I turned 18 in 2020?"
        
        with patch('agents.tfsa_agent.calculate_tfsa_contribution_room') as mock_calc, \
             patch('agents.tfsa_agent.find_relevant_sections') as mock_sections:
            
            mock_calc.return_value = CalculationToolResult(
                total_contribution_room=30000,
                yearly_breakdown={2020: 6000, 2021: 6000},
                assumptions=["test"]
            )
            mock_sections.return_value = []
            
            result = self.agent.handle_question(question)
            
            assert isinstance(result, CalculationAnswer)
            assert result.type == "calculation_result"
            assert mock_calc.called
            assert mock_sections.called

    def test_handle_contribution_question_without_year(self):
        """Should return error when year is missing."""
        question = "What is my TFSA contribution room?"
        
        result = self.agent.handle_question(question)
        
        assert isinstance(result, ToolError)
        assert result.type == "error"
        assert "year" in result.message.lower() or "18" in result.message

    def test_handle_non_contribution_question(self):
        """Should return None for questions not about contributions."""
        question = "What is a TFSA?"
        
        result = self.agent.handle_question(question)
        
        assert result is None

    def test_handle_contribution_question_case_insensitive(self):
        """Should detect contribution question regardless of case."""
        question = "What is my CONTRIBUTION room if I turned 18 in 2020?"
        
        with patch('agents.tfsa_agent.calculate_tfsa_contribution_room') as mock_calc, \
             patch('agents.tfsa_agent.find_relevant_sections') as mock_sections:
            
            mock_calc.return_value = CalculationToolResult(
                total_contribution_room=30000,
                yearly_breakdown={2020: 6000},
                assumptions=["test"]
            )
            mock_sections.return_value = []
            
            result = self.agent.handle_question(question)
            
            assert isinstance(result, CalculationAnswer)

    def test_handle_question_extracts_year_correctly(self):
        """Should extract year and pass to calculator."""
        question = "I turned 18 in 2018, what's my contribution room?"
        
        with patch('agents.tfsa_agent.calculate_tfsa_contribution_room') as mock_calc, \
             patch('agents.tfsa_agent.find_relevant_sections') as mock_sections:
            
            mock_calc.return_value = CalculationToolResult(
                total_contribution_room=40000,
                yearly_breakdown={2018: 5500},
                assumptions=["test"]
            )
            mock_sections.return_value = []
            
            result = self.agent.handle_question(question)
            
            # Verify the calculator was called with the correct year
            mock_calc.assert_called_once_with(year_turned_18=2018)

    def test_handle_question_retrieves_sections(self):
        """Should retrieve relevant sections for contribution questions."""
        question = "What is my TFSA contribution room if I turned 18 in 2020?"
        
        with patch('agents.tfsa_agent.calculate_tfsa_contribution_room') as mock_calc, \
             patch('agents.tfsa_agent.find_relevant_sections') as mock_sections:
            
            test_section = Section(
                id="1",
                section="Test Section",
                topic="TFSA",
                text="Test text",
                document="CRA",
                jurisdiction="Canada",
                year=2025
            )
            mock_sections.return_value = [test_section]
            mock_calc.return_value = CalculationToolResult(
                total_contribution_room=30000,
                yearly_breakdown={2020: 6000},
                assumptions=["test"]
            )
            
            result = self.agent.handle_question(question)
            
            # Verify sections were retrieved
            mock_sections.assert_called_once_with(question)
            assert isinstance(result, CalculationAnswer)
            assert len(result.sections) == 1
            assert result.sections[0].section == "Test Section"

    def test_handle_general_question_returns_none(self):
        """Should return None for general questions."""
        questions = [
            "What is a TFSA?",
            "Tell me about savings accounts",
            "How does investment work?",
            "Can I withdraw from my TFSA?"
        ]
        
        for question in questions:
            result = self.agent.handle_question(question)
            assert result is None, f"Expected None for question: {question}"
