"""
Assistant service for open-domain, persona-based chat.

Unlike ChatService (which strictly answers only from provided class notes),
this service answers general questions using the model's own knowledge,
guided by a role/persona description rather than a source document.
"""

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from app.config import settings
from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)


class AssistantService:
    """
    Service class for open-domain persona chat functionality.
    """

    def __init__(self):
        """Initialize the assistant service with Gemini model."""
        try:
            self.llm = ChatGoogleGenerativeAI(
                model=settings.model_name,
                google_api_key=settings.google_api_key,
                temperature=settings.temperature,
                max_output_tokens=settings.max_tokens,
            )
            logger.info("Assistant Service initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize Assistant Service: {str(e)}")
            raise

    async def chat(
        self,
        role_context: str,
        question: str,
        context: str = None
    ) -> Dict[str, Any]:
        """
        Answer an open-domain question guided by a persona/role description.

        Args:
            role_context: Persona/role instructions for the assistant
            question: User's question or message
            context: Optional previous exchange for continuity

        Returns:
            Dict containing the answer

        Raises:
            Exception: If AI generation fails
        """
        try:
            prompt_template = """{role_context}

{context_section}

User Question: {question}

Provide a helpful, detailed response using your own knowledge, following the persona and guidance above:"""

            context_section = f"Previous exchange:\n{context}\n" if context else ""

            prompt = PromptTemplate(
                input_variables=["role_context", "question", "context_section"],
                template=prompt_template
            )

            chain = prompt | self.llm

            result = await chain.ainvoke({
                "role_context": role_context,
                "question": question,
                "context_section": context_section
            })

            return {
                "answer": result.content.strip()
            }

        except Exception as e:
            logger.error(f"Error in assistant chat: {str(e)}")
            raise Exception(f"Failed to generate answer: {str(e)}")


# Global assistant service instance
assistant_service = AssistantService()
