"""
Assessment service for generating topic-based classroom assessments
(as opposed to the content-based MCQ generator).
"""

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from app.config import settings
from app.services.json_utils import parse_json_response
from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)


class AssessmentService:
    """
    Service class for topic-based assessment generation functionality.
    """

    def __init__(self):
        """Initialize the assessment service with Gemini model."""
        try:
            self.llm = ChatGoogleGenerativeAI(
                model=settings.model_name,
                google_api_key=settings.google_api_key,
                temperature=settings.temperature,
                max_output_tokens=settings.max_tokens,
            )
            logger.info("Assessment Service initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize Assessment Service: {str(e)}")
            raise

    async def generate_assessment(
        self,
        subject: str,
        class_level: str,
        topic: str,
        assessment_type: str = "Mixed (MCQ + Short Answer)",
        num_questions: int = 10,
        difficulty: str = "Medium"
    ) -> Dict[str, Any]:
        """
        Generate a classroom assessment from a topic.

        Args:
            subject: Subject area
            class_level: Class/grade level
            topic: Assessment topic
            assessment_type: Multiple Choice | Short Answer | Essay Questions | Mixed (MCQ + Short Answer)
            num_questions: Number of questions to generate
            difficulty: Easy | Medium | Hard | Mixed

        Returns:
            Dict containing structured assessment data

        Raises:
            Exception: If assessment generation fails
        """
        try:
            prompt_template = """You are an expert African educator creating a classroom assessment.

Generate a {difficulty} difficulty {assessment_type} assessment with {num_questions} questions
for {subject}, Class {class_level}, on the topic "{topic}".

Generate the assessment in JSON format with exactly this structure:
{{
  "subject": "{subject}",
  "class_level": "{class_level}",
  "topic": "{topic}",
  "assessment_type": "{assessment_type}",
  "difficulty": "{difficulty}",
  "questions": [
    {{
      "question_number": 1,
      "question_type": "multiple_choice",
      "question": "question text",
      "options": [
        {{"option": "A", "text": "option A text"}},
        {{"option": "B", "text": "option B text"}},
        {{"option": "C", "text": "option C text"}},
        {{"option": "D", "text": "option D text"}}
      ],
      "correct_answer": "A",
      "suggested_answer": null
    }}
  ]
}}

Rules:
1. question_type must be one of "multiple_choice", "short_answer", or "essay".
2. For "multiple_choice" questions: include exactly 4 "options" (A-D) and set "correct_answer"; leave "suggested_answer" null.
3. For "short_answer" and "essay" questions: set "options" and "correct_answer" to null, and provide "suggested_answer" with suggested answer points.
4. If assessment_type is "Multiple Choice", every question must be "multiple_choice".
5. If assessment_type is "Short Answer", every question must be "short_answer".
6. If assessment_type is "Essay Questions", every question must be "essay".
7. If assessment_type is "Mixed (MCQ + Short Answer)", use a mix of "multiple_choice" and "short_answer".

JSON Response:"""

            prompt = PromptTemplate(
                input_variables=["subject", "class_level", "topic", "assessment_type", "num_questions", "difficulty"],
                template=prompt_template
            )

            chain = prompt | self.llm

            result = await chain.ainvoke({
                "subject": subject,
                "class_level": class_level,
                "topic": topic,
                "assessment_type": assessment_type,
                "num_questions": num_questions,
                "difficulty": difficulty
            })

            assessment_data = parse_json_response(result.content)

            return assessment_data

        except Exception as e:
            logger.error(f"Error in generate_assessment: {str(e)}")
            raise Exception(f"Failed to generate assessment: {str(e)}")


# Global assessment service instance
assessment_service = AssessmentService()
