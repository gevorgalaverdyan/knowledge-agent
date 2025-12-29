"""
Unit tests for TFSA agent in agents/tfsa_agent.py
"""
import os
os.environ["DB_URL"] = "sqlite:///:memory:"
os.environ["GEMINI_API_KEY"] = "test-api-key-for-testing"

import pytest
from unittest.mock import patch, Mock
from agents.tfsa_agent import TFSAAagent
from schemas.chat import CalculationAnswer, ToolError


class TestTFSAAagent:
    """Tests for TFSAAagent class"""
    
    def setup_method(self):
        """Setup test agent instance"""
        self.agent = TFSAAagent()
    
    @patch('agents.tfsa_agent.find_relevant_sections')
    @patch('agents.tfsa_agent.calculate_tfsa_contribution_room')
    @patch('agents.tfsa_agent.extract_year')
    def test_handle_contribution_question_with_year(self, mock_extract, mock_calculate, mock_sections):
        """Test handling contribution question with valid year"""
        from schemas.chat import CalculationToolResult, Section
        
        mock_extract.return_value = 2010
        mock_calculate.return_value = CalculationToolResult(
            total_contribution_room=100000,
            yearly_breakdown={2010: 5000},
            assumptions=["Test assumption"]
        )
        mock_sections.return_value = [
            Section(id="1", section="Test", topic="Test", text="Test text",
                 document="CRA", jurisdiction="Canada", year=2025)
        ]
        
        question = "What is my contribution room if I turned 18 in 2010?"
        result = self.agent.handle_question(question)
        
        assert isinstance(result, CalculationAnswer)
        assert result.type == "calculation_result"
        assert len(result.sections) > 0
        assert result.calculation.total_contribution_room == 100000
        
        mock_extract.assert_called_once_with(question)
        mock_calculate.assert_called_once_with(year_turned_18=2010)
        mock_sections.assert_called_once_with(question)
    
    @patch('agents.tfsa_agent.extract_year')
    def test_handle_contribution_question_without_year(self, mock_extract):
        """Test handling contribution question without year"""
        mock_extract.return_value = -1
        
        question = "What is my contribution room?"
        result = self.agent.handle_question(question)
        
        assert isinstance(result, ToolError)
        assert result.type == "error"
        assert "specify the year you turned 18" in result.message
        
        mock_extract.assert_called_once_with(question)
    
    def test_handle_non_contribution_question(self):
        """Test handling question that doesn't trigger contribution tool"""
        question = "What is a TFSA?"
        result = self.agent.handle_question(question)
        
        assert result is None
    
    @patch('agents.tfsa_agent.find_relevant_sections')
    @patch('agents.tfsa_agent.calculate_tfsa_contribution_room')
    @patch('agents.tfsa_agent.extract_year')
    def test_handle_contribution_case_insensitive(self, mock_extract, mock_calculate, mock_sections):
        """Test that contribution detection is case insensitive"""
        from schemas.chat import CalculationToolResult
        
        mock_extract.return_value = 2015
        mock_calculate.return_value = CalculationToolResult(
            total_contribution_room=50000,
            yearly_breakdown={2015: 10000},
            assumptions=["Test"]
        )
        mock_sections.return_value = []
        
        questions = [
            "What is my CONTRIBUTION room?",
            "Tell me about my Contribution limits",
            "contribution room for 2015"
        ]
        
        for question in questions:
            result = self.agent.handle_question(question)
            assert isinstance(result, CalculationAnswer)
    
    def test_handle_eligibility_question(self):
        """Test handling eligibility question (no tool triggered)"""
        question = "Am I eligible for a TFSA?"
        result = self.agent.handle_question(question)
        
        assert result is None
    
    def test_handle_withdrawal_question(self):
        """Test handling withdrawal question (no tool triggered)"""
        question = "Can I withdraw from my TFSA?"
        result = self.agent.handle_question(question)
        
        assert result is None
    
    @patch('agents.tfsa_agent.find_relevant_sections')
    @patch('agents.tfsa_agent.calculate_tfsa_contribution_room')
    @patch('agents.tfsa_agent.extract_year')
    def test_handle_complex_contribution_question(self, mock_extract, mock_calculate, mock_sections):
        """Test handling complex question with contribution keyword"""
        from schemas.chat import CalculationToolResult
        
        mock_extract.return_value = 2020
        mock_calculate.return_value = CalculationToolResult(
            total_contribution_room=35000,
            yearly_breakdown={2020: 6000, 2021: 6000, 2022: 6000, 2023: 6500, 2024: 7000, 2025: 7000},
            assumptions=["Canadian resident", "No contributions", "No withdrawals", "CRA limits"]
        )
        mock_sections.return_value = []
        
        question = "I turned 18 in 2020, what's my total contribution space available?"
        result = self.agent.handle_question(question)
        
        assert isinstance(result, CalculationAnswer)
        assert result.calculation.total_contribution_room == 35000
        assert len(result.calculation.assumptions) == 4
    
    @patch('agents.tfsa_agent.extract_year')
    def test_handle_contribution_missing_year_error_message(self, mock_extract):
        """Test error message when year is missing"""
        mock_extract.return_value = -1
        
        question = "What is my contribution limit?"
        result = self.agent.handle_question(question)
        
        assert isinstance(result, ToolError)
        assert result.message == "Please specify the year you turned 18."
    
    @patch('agents.tfsa_agent.find_relevant_sections')
    @patch('agents.tfsa_agent.calculate_tfsa_contribution_room')
    @patch('agents.tfsa_agent.extract_year')
    def test_handle_retrieves_sections_for_context(self, mock_extract, mock_calculate, mock_sections):
        """Test that relevant sections are retrieved for context"""
        from schemas.chat import CalculationToolResult, Section
        
        mock_extract.return_value = 2018
        mock_calculate.return_value = CalculationToolResult(
            total_contribution_room=50000,
            yearly_breakdown={},
            assumptions=[]
        )
        
        section_mock = Section(
            id="test-id",
            section="Test Section",
            topic="Test Topic",
            text="Test content",
            document="CRA",
            jurisdiction="Canada",
            year=2025
        )
        mock_sections.return_value = [section_mock]
        
        question = "contribution room 2018"
        result = self.agent.handle_question(question)
        
        assert isinstance(result, CalculationAnswer)
        assert len(result.sections) == 1
        assert result.sections[0].id == "test-id"
        
        mock_sections.assert_called_once_with(question)
