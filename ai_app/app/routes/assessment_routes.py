"""
Assessment generation API routes.
"""

from fastapi import APIRouter, HTTPException, status
from app.schemas.assessment_schemas import GenerateAssessmentRequest, AssessmentResponse
from app.schemas.common_schemas import ErrorResponse
from app.services.assessment_service import assessment_service
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/assessment",
    tags=["Assessment Generation"],
    responses={
        500: {"model": ErrorResponse, "description": "Internal Server Error"},
        400: {"model": ErrorResponse, "description": "Bad Request"},
    },
)


@router.post(
    "",
    response_model=AssessmentResponse,
    status_code=status.HTTP_200_OK,
    summary="Generate Assessment",
    description="Generate a classroom assessment (MCQ, short answer, and/or essay) from a topic.",
)
async def generate_assessment(request: GenerateAssessmentRequest) -> AssessmentResponse:
    """
    Generate assessment endpoint.

    Args:
        request: GenerateAssessmentRequest containing subject, class level, topic, and parameters

    Returns:
        AssessmentResponse with structured assessment questions

    Raises:
        HTTPException: If generation fails
    """
    try:
        logger.info(f"Generating {request.num_questions} assessment questions on: {request.topic}")

        result = await assessment_service.generate_assessment(
            subject=request.subject,
            class_level=request.class_level,
            topic=request.topic,
            assessment_type=request.assessment_type,
            num_questions=request.num_questions,
            difficulty=request.difficulty
        )

        return AssessmentResponse(
            subject=result.get("subject", request.subject),
            class_level=result.get("class_level", request.class_level),
            topic=result.get("topic", request.topic),
            assessment_type=result.get("assessment_type", request.assessment_type),
            difficulty=result.get("difficulty", request.difficulty),
            questions=result["questions"],
            timestamp=datetime.now()
        )

    except Exception as e:
        logger.error(f"Error in generate_assessment endpoint: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate assessment: {str(e)}"
        )


@router.get(
    "/health",
    status_code=status.HTTP_200_OK,
    summary="Assessment Service Health Check",
    description="Check if the assessment generation service is operational.",
)
async def health_check():
    """
    Health check endpoint for assessment service.

    Returns:
        Dict with health status
    """
    return {
        "status": "healthy",
        "service": "Assessment Generation Service",
        "timestamp": datetime.now()
    }
