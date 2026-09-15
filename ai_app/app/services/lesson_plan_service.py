"""
Lesson plan service for generating a single classroom lesson plan from a topic.
"""

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from app.config import settings
from app.services.json_utils import parse_json_response
from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)


class LessonPlanService:
    """
    Service class for lesson plan generation functionality.

    Handles AI-powered creation of a single classroom lesson plan from a topic.
    """

    def __init__(self):
        """Initialize the lesson plan service with Gemini model."""
        try:
            self.llm = ChatGoogleGenerativeAI(
                model=settings.model_name,
                google_api_key=settings.google_api_key,
                temperature=settings.temperature,
                max_output_tokens=settings.max_tokens,
            )
            logger.info("Lesson Plan Service initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize Lesson Plan Service: {str(e)}")
            raise

    async def generate_lesson_plan(
        self,
        topic: str,
        objectives: str = None
    ) -> Dict[str, Any]:
        """
        Generate a single lesson plan from a topic.

        Args:
            topic: Lesson topic to build a plan around
            objectives: Optional specific learning objectives to emphasize

        Returns:
            Dict containing structured lesson plan data

        Raises:
            Exception: If lesson plan generation fails
        """
        try:
            prompt_template = """You are an expert educator creating a practical, engaging lesson plan for African classrooms.

Topic: {topic}
{objectives_section}

Generate a lesson plan in JSON format with exactly this structure:
{{
  "topic": "{topic}",
  "grade_level": "suggested grade, e.g. Grade 8",
  "subject": "subject area, e.g. Mathematics, English, Science, or Social Studies",
  "duration_minutes": 45,
  "title": "engaging lesson title",
  "learning_objectives": "clear, measurable learning objectives",
  "introduction": "engaging hook to capture student interest (10 minutes)",
  "main_activities": "detailed step-by-step teaching activities with examples (25 minutes)",
  "assessment_methods": "how to evaluate student understanding",
  "materials_needed": "list of required resources"
}}

Make it practical and engaging, considering resource constraints common in African schools.

JSON Response:"""

            objectives_section = f"Learning Objectives to emphasize: {objectives}" if objectives else ""

            prompt = PromptTemplate(
                input_variables=["topic", "objectives_section"],
                template=prompt_template
            )

            chain = prompt | self.llm

            result = await chain.ainvoke({
                "topic": topic,
                "objectives_section": objectives_section
            })

            lesson_plan_data = parse_json_response(result.content)

            return lesson_plan_data

        except Exception as e:
            logger.error(f"Error in generate_lesson_plan: {str(e)}")
            raise Exception(f"Failed to generate lesson plan: {str(e)}")


# Global lesson plan service instance
lesson_plan_service = LessonPlanService()
