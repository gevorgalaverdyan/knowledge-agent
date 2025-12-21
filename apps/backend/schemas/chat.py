from datetime import datetime
from typing import Dict, List, Literal, Union

from pydantic import BaseModel, Field

class Chat(BaseModel):
    id: str
    messages: List[str]
    created_at: datetime

class GeminiResponse(BaseModel):
    answer: str

class Section(BaseModel):
    id: str
    section: str
    topic: str
    text: str
    document: str
    jurisdiction: str
    year: int

class CalculationToolResult(BaseModel):
    total_contribution_room: int
    yearly_breakdown: Dict[int, int]
    assumptions: List[str]

class ToolAnswer(BaseModel):
    type: Literal["calculation_result", "search_result", "error"]
    sections: List[Section] = Field(default_factory=list)

class CalculationAnswer(ToolAnswer):
    type: Literal["calculation_result"] = "calculation_result"
    calculation: CalculationToolResult

class ToolError(BaseModel):
    type: Literal["error"] = "error"
    message: str


