from typing import List, Literal

from pydantic import BaseModel, Field, field_validator

class MCQQuestion(BaseModel):
    question: str = Field(description="The question text")
    options: List[str] = Field(description="List of 4 options")
    correct_answer: str = Field(description="The correct answer from the options")
    type: Literal["MCQ", "FiTB"] = Field(description="The question type", default="MCQ")
    
    @field_validator('question', mode="before")
    def clean_question(cls, value) -> str:
        if isinstance(value, dict):
            return value.get("description", str(value))
        return str(value)
    
class FillBlankQuestion(BaseModel):
    question: str = Field(description="The question text with '_____' for the blank")
    correct_answer: str = Field(description="The correct word or phrase for the blank")
    type: Literal["MCQ", "FiTB"] = Field(description="The question type", default="FiTB")
    
    @field_validator('question', mode="before")
    def clean_question(cls, value) -> str:
        if isinstance(value, dict):
            return value.get("description", str(value))
        return str(value)
