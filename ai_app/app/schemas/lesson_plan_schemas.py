"""
Schemas for lesson plan generation functionality.
"""

from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class GenerateLessonPlanRequest(BaseModel):
    """
    Request schema for generating a single lesson plan from a topic.

    Attributes:
        topic: The lesson topic to build a plan around
        objectives: Optional specific learning objectives to emphasize
    """
    topic: str = Field(..., description="Lesson topic", min_length=3)
    objectives: Optional[str] = Field(None, description="Specific learning objectives to emphasize")

    class Config:
        json_schema_extra = {
            "example": {
                "topic": "Photosynthesis",
                "objectives": "Understand the inputs and outputs of photosynthesis"
            }
        }


class LessonPlanResponse(BaseModel):
    """
    Response schema for lesson plan generation endpoint.
    """
    topic: str = Field(..., description="Lesson topic")
    grade_level: str = Field(..., description="Suggested grade/class level")
    subject: str = Field(..., description="Subject area")
    duration_minutes: int = Field(..., description="Suggested lesson duration in minutes")
    title: str = Field(..., description="Engaging lesson title")
    learning_objectives: str = Field(..., description="Clear, measurable learning objectives")
    introduction: str = Field(..., description="Engaging hook to open the lesson")
    main_activities: str = Field(..., description="Detailed step-by-step activities")
    assessment_methods: str = Field(..., description="How to evaluate student understanding")
    materials_needed: str = Field(..., description="Required resources")
    timestamp: datetime = Field(default_factory=datetime.now, description="Response timestamp")
