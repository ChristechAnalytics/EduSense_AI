"""
Chat service for interacting with class notes using AI.
"""

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from app.config import settings
from typing import Dict, Any, List
import logging

logger = logging.getLogger(__name__)


class ChatService:
    """
    Service class for chat with notes functionality.
    
    Handles AI-powered question answering based on class notes.
    """
    
    def __init__(self):
        """Initialize the chat service with Gemini model."""
        try:
            self.llm = ChatGoogleGenerativeAI(
                model=settings.model_name,
                google_api_key=settings.google_api_key,
                temperature=settings.temperature,
                max_output_tokens=settings.max_tokens,
            )
            logger.info("Chat Service initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize Chat Service: {str(e)}")
            raise
    
    async def chat_with_notes(
        self,
        notes: str,
        question: str,
        context: str = None
    ) -> Dict[str, Any]:
        """
        Chat with class notes using AI.
        
        Args:
            notes: The class notes or knowledge base content
            question: User's question about the notes
            context: Optional previous conversation context
            
        Returns:
            Dict containing the answer and metadata
            
        Raises:
            Exception: If AI generation fails
        """
        try:
            prompt_template = """You are an expert educational assistant helping students understand their class notes.

Class Notes:
{notes}

{context_section}

Question: {question}

Provide a clear, accurate, and educational answer based on the notes provided. If the question cannot be answered from the notes, politely say so and suggest what additional information might be needed.

Answer:"""
            
            context_section = f"Previous Context:\n{context}\n" if context else ""
            
            prompt = PromptTemplate(
                input_variables=["notes", "question", "context_section"],
                template=prompt_template
            )
            
            chain = prompt | self.llm

            result = await chain.ainvoke({
                "notes": notes,
                "question": question,
                "context_section": context_section
            })

            return {
                "answer": result.content.strip(),
                "confidence": 0.85,
                "sources": self._extract_relevant_snippets(notes, question)
            }
            
        except Exception as e:
            logger.error(f"Error in chat_with_notes: {str(e)}")
            raise Exception(f"Failed to generate answer: {str(e)}")
    
    def _extract_relevant_snippets(self, notes: str, question: str, max_snippets: int = 3) -> List[str]:
        """
        Extract relevant snippets from notes based on question.
        
        Args:
            notes: The full notes text
            question: The question to match against
            max_snippets: Maximum number of snippets to return
            
        Returns:
            List of relevant text snippets
        """
        sentences = notes.split('. ')
        return sentences[:max_snippets] if len(sentences) > max_snippets else sentences


# Global chat service instance
chat_service = ChatService()

