"""
Shared helpers for parsing JSON out of LLM text responses.
"""

from typing import Dict, Any
import json
import logging

logger = logging.getLogger(__name__)


def parse_json_response(response: str) -> Dict[str, Any]:
    """
    Parse JSON from an AI response, stripping markdown code fences if present.

    Args:
        response: Raw AI response text

    Returns:
        Parsed JSON dict

    Raises:
        ValueError: If JSON parsing fails
    """
    try:
        if "```json" in response:
            json_start = response.find("```json") + 7
            json_end = response.find("```", json_start)
            response = response[json_start:json_end].strip()
        elif "```" in response:
            json_start = response.find("```") + 3
            json_end = response.find("```", json_start)
            response = response[json_start:json_end].strip()

        return json.loads(response.strip())

    except json.JSONDecodeError as e:
        logger.error(f"Failed to parse JSON: {str(e)}\nResponse: {response}")
        raise ValueError(f"Invalid JSON response from AI: {str(e)}")
