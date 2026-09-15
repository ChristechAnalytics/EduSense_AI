"""
Open-domain assistant chat API routes.
"""

from fastapi import APIRouter, HTTPException, status
from app.schemas.assistant_schemas import AssistantChatRequest, AssistantChatResponse
from app.schemas.common_schemas import ErrorResponse
from app.services.assistant_service import assistant_service
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/assistant",
    tags=["Assistant Chat"],
    responses={
        500: {"model": ErrorResponse, "description": "Internal Server Error"},
        400: {"model": ErrorResponse, "description": "Bad Request"},
    },
)


@router.post(
    "",
    response_model=AssistantChatResponse,
    status_code=status.HTTP_200_OK,
    summary="Chat with the AI Assistant",
    description="Ask an open-domain question, guided by a persona/role description rather than source notes.",
)
async def assistant_chat(request: AssistantChatRequest) -> AssistantChatResponse:
    """
    Assistant chat endpoint.

    Args:
        request: AssistantChatRequest containing role context, question, and optional prior context

    Returns:
        AssistantChatResponse with the answer

    Raises:
        HTTPException: If processing fails
    """
    try:
        logger.info(f"Processing assistant chat request: {request.question[:50]}...")

        result = await assistant_service.chat(
            role_context=request.role_context,
            question=request.question,
            context=request.context
        )

        return AssistantChatResponse(
            answer=result["answer"],
            timestamp=datetime.now()
        )

    except Exception as e:
        logger.error(f"Error in assistant_chat endpoint: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to process assistant chat request: {str(e)}"
        )


@router.get(
    "/health",
    status_code=status.HTTP_200_OK,
    summary="Assistant Service Health Check",
    description="Check if the assistant chat service is operational.",
)
async def health_check():
    """
    Health check endpoint for assistant service.

    Returns:
        Dict with health status
    """
    return {
        "status": "healthy",
        "service": "Assistant Chat Service",
        "timestamp": datetime.now()
    }
