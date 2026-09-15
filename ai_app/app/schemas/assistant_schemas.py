"""
Schemas for the open-domain AI assistant (persona-based chat), as opposed
to the strictly notes-grounded chat endpoint.
"""

from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class AssistantChatRequest(BaseModel):
    """
    Request schema for open-domain persona chat.

    Attributes:
        role_context: Persona/role instructions for the assistant (e.g. "You are a
            friendly AI tutor for African students...")
        question: The user's question or message
        context: Optional previous exchange for conversational continuity
    """
    role_context: str = Field(..., description="Persona/role instructions for the assistant", min_length=10)
    question: str = Field(..., description="User's question or message", min_length=1)
    context: Optional[str] = Field(None, description="Previous exchange for continuity")

    class Config:
        json_schema_extra = {
            "example": {
                "role_context": "You are a friendly AI tutor for African students. Be encouraging and patient.",
                "question": "What is photosynthesis?",
                "context": None
            }
        }


class AssistantChatResponse(BaseModel):
    """
    Response schema for the assistant chat endpoint.
    """
    answer: str = Field(..., description="AI-generated answer")
    timestamp: datetime = Field(default_factory=datetime.now, description="Response timestamp")
