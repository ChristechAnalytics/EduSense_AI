"""
Flashcard service for generating study flashcards from content.
"""

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from app.config import settings
from app.services.json_utils import parse_json_response
from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)


class FlashcardService:
    """
    Service class for flashcard generation functionality.
    
    Handles AI-powered creation of study flashcards.
    """
    
    def __init__(self):
        """Initialize the flashcard service with Gemini model."""
        try:
            self.llm = ChatGoogleGenerativeAI(
                model=settings.model_name,
                google_api_key=settings.google_api_key,
                temperature=settings.temperature,
                max_output_tokens=settings.max_tokens,
            )
            logger.info("Flashcard Service initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize Flashcard Service: {str(e)}")
            raise
    
    async def generate_flashcards(
        self,
        content: str,
        num_flashcards: int = 10,
        focus_areas: str = None
    ) -> Dict[str, Any]:
        """
        Generate flashcards from content.
        
        Args:
            content: Content to generate flashcards from
            num_flashcards: Number of flashcards to generate
            focus_areas: Optional specific areas to focus on
            
        Returns:
            Dict containing flashcard data
            
        Raises:
            Exception: If flashcard generation fails
        """
        try:
            prompt_template = """You are an expert at creating educational flashcards. Generate {num_flashcards} flashcards from the following content.

Content:
{content}

{focus_section}

Generate flashcards in JSON format with this structure:
{{
  "total_cards": {num_flashcards},
  "focus_areas": "{focus_areas}",
  "flashcards": [
    {{
      "card_number": 1,
      "front": "Question or term (concise)",
      "back": "Answer or definition (clear and complete)",
      "category": "topic category",
      "difficulty": "easy/medium/hard"
    }}
  ]
}}

Ensure:
1. Front of card is concise (question/term)
2. Back provides clear, complete answer
3. Cards cover key concepts
4. Mix of difficulty levels
5. Logical categorization

JSON Response:"""
            
            focus_section = f"Focus Areas: {focus_areas}" if focus_areas else "Focus Areas: Cover all key concepts"
            
            prompt = PromptTemplate(
                input_variables=["content", "num_flashcards", "focus_section", "focus_areas"],
                template=prompt_template
            )
            
            chain = LLMChain(llm=self.llm, prompt=prompt)
            
            result = await chain.ainvoke({
                "content": content,
                "num_flashcards": num_flashcards,
                "focus_section": focus_section,
                "focus_areas": focus_areas or "general"
            })
            
            # Parse JSON response
            flashcard_data = parse_json_response(result["text"])

            return flashcard_data

        except Exception as e:
            logger.error(f"Error in generate_flashcards: {str(e)}")
            raise Exception(f"Failed to generate flashcards: {str(e)}")


# Global flashcard service instance
flashcard_service = FlashcardService()

