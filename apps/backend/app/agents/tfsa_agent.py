import logging

from app.schemas.chat import ToolAnswer, ToolError, CalculationAnswer
from app.tools.calculations import calculate_tfsa_contribution_room
from app.utils.utils import extract_year
from app.tools.retrieval import find_relevant_sections

logger = logging.getLogger(__name__)

class TFSAAagent:

    def handle_question(self, question: str) -> ToolAnswer | ToolError | None:
        question_lower = question.lower()

        # --- Tool decision ---
        if "contribution" in question_lower:
            logger.info("TFSA contribution question detected. Using calculation tool.")
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
