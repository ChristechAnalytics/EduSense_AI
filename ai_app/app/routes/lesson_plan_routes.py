"""
Lesson plan generation API routes.
"""

from fastapi import APIRouter, HTTPException, status
from app.schemas.lesson_plan_schemas import GenerateLessonPlanRequest, LessonPlanResponse
from app.schemas.common_schemas import ErrorResponse
from app.services.lesson_plan_service import lesson_plan_service
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/lesson-plan",
    tags=["Lesson Plan Generation"],
    responses={
        500: {"model": ErrorResponse, "description": "Internal Server Error"},
        400: {"model": ErrorResponse, "description": "Bad Request"},
    },
)


@router.post(
    "",
    response_model=LessonPlanResponse,
    status_code=status.HTTP_200_OK,
    summary="Generate Lesson Plan",
    description="Generate a single classroom lesson plan from a topic.",
)
async def generate_lesson_plan(request: GenerateLessonPlanRequest) -> LessonPlanResponse:
    """
    Generate lesson plan endpoint.

    Args:
        request: GenerateLessonPlanRequest containing topic and optional objectives

    Returns:
        LessonPlanResponse with structured lesson plan

    Raises:
        HTTPException: If generation fails
    """
    try:
        logger.info(f"Generating lesson plan for topic: {request.topic}")

        result = await lesson_plan_service.generate_lesson_plan(
            topic=request.topic,
            objectives=request.objectives
        )

        return LessonPlanResponse(
            topic=result.get("topic", request.topic),
            grade_level=result["grade_level"],
            subject=result["subject"],
            duration_minutes=result["duration_minutes"],
            title=result["title"],
            learning_objectives=result["learning_objectives"],
            introduction=result["introduction"],
            main_activities=result["main_activities"],
            assessment_methods=result["assessment_methods"],
            materials_needed=result["materials_needed"],
            timestamp=datetime.now()
        )

    except Exception as e:
        logger.error(f"Error in generate_lesson_plan endpoint: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate lesson plan: {str(e)}"
        )


@router.get(
    "/health",
    status_code=status.HTTP_200_OK,
    summary="Lesson Plan Service Health Check",
    description="Check if the lesson plan generation service is operational.",
)
async def health_check():
    """
    Health check endpoint for lesson plan service.

    Returns:
        Dict with health status
    """
    return {
        "status": "healthy",
        "service": "Lesson Plan Generation Service",
        "timestamp": datetime.now()
    }
