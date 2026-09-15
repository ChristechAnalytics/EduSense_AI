"""
Schemas for topic-based assessment generation functionality (teacher-facing,
as opposed to the content-based MCQ generator).
"""

from pydantic import BaseModel, Field, field_validator
from typing import Optional, List
from datetime import datetime


class GenerateAssessmentRequest(BaseModel):
    """
    Request schema for generating a classroom assessment from a topic.

    Attributes:
        subject: Subject area
        class_level: Class/grade level (e.g. JS1, SS2)
        topic: Assessment topic
        assessment_type: Multiple Choice | Short Answer | Essay Questions | Mixed (MCQ + Short Answer)
        num_questions: Number of questions to generate
        difficulty: Easy | Medium | Hard | Mixed
    """
    subject: str = Field(..., description="Subject area")
    class_level: str = Field(..., description="Class/grade level, e.g. JS1, SS2")
    topic: str = Field(..., description="Assessment topic", min_length=3)
    assessment_type: str = Field(
        "Mixed (MCQ + Short Answer)",
        description="Multiple Choice | Short Answer | Essay Questions | Mixed (MCQ + Short Answer)"
    )
    num_questions: int = Field(10, description="Number of questions to generate", ge=5, le=50)
    difficulty: str = Field("Medium", description="Easy | Medium | Hard | Mixed")

    class Config:
        json_schema_extra = {
            "example": {
                "subject": "Biology",
                "class_level": "SS2",
                "topic": "Photosynthesis",
                "assessment_type": "Mixed (MCQ + Short Answer)",
                "num_questions": 10,
                "difficulty": "Medium"
            }
        }


class AssessmentOption(BaseModel):
    """Schema for a multiple choice option."""
    option: str = Field(..., description="Option label")
    text: str = Field(..., description="Option text")


class AssessmentQuestion(BaseModel):
    """
    Schema for a single assessment question, covering MCQ, short answer, and essay types.
    """
    question_number: int = Field(..., description="Question number")
    question_type: str = Field(..., description="multiple_choice | short_answer | essay")
    question: str = Field(..., description="Question text")
    options: Optional[List[AssessmentOption]] = Field(None, description="Answer options (multiple_choice only)")
    correct_answer: Optional[str] = Field(None, description="Correct option label (multiple_choice only)")
    suggested_answer: Optional[str] = Field(None, description="Suggested answer points (short_answer/essay only)")

    @field_validator("question", "suggested_answer", mode="before")
    @classmethod
    def _join_if_list(cls, value):
        """The model sometimes returns these as a list of bullet points instead of a string."""
        if isinstance(value, list):
            return "\n".join(str(item) for item in value)
        return value


class AssessmentResponse(BaseModel):
    """
    Response schema for assessment generation endpoint.
    """
    subject: str = Field(..., description="Subject area")
    class_level: str = Field(..., description="Class/grade level")
    topic: str = Field(..., description="Assessment topic")
    assessment_type: str = Field(..., description="Assessment type")
    difficulty: str = Field(..., description="Difficulty level")
    questions: List[AssessmentQuestion] = Field(..., description="Generated questions")
    timestamp: datetime = Field(default_factory=datetime.now, description="Response timestamp")
