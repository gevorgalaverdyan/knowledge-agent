from typing import Dict
from schemas.chat import CalculationAnswer, ToolAnswer, ToolError
from tools.calculations import calculate_tfsa_contribution_room
from utils.utils import extract_year
from tools.retrieval import find_relevant_sections


class TFSAAagent:

    def handle_question(self, question: str) -> ToolAnswer | ToolError | None:
        question_lower = question.lower()

        # --- Tool decision ---
        if "contribution" in question_lower:
            year_turned_18 = extract_year(question)

            if year_turned_18 == -1:
                return ToolError(
                    type="error", 
                    message="Please specify the year you turned 18.") 


            calculation = calculate_tfsa_contribution_room(
                year_turned_18=year_turned_18,
            )

            # Retrieve relevant CRA sections for explanation
            sections = find_relevant_sections(question)

            return CalculationAnswer(type="calculation_result", sections=sections, calculation=calculation) 

        return None