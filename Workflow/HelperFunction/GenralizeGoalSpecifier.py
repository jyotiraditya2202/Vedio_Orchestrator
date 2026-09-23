from google import genai
from pydantic import BaseModel
from typing import Literal
from dotenv import load_dotenv
import os
from ..Prompts import GENERALIZE_GOAL_SPECIFIER_SYSTEM_PROMPT

# Load .env
load_dotenv()


# Environment variables
api_key = os.getenv("GEMINI_API_KEY")
default_system_prompt = GENERALIZE_GOAL_SPECIFIER_SYSTEM_PROMPT

#validating global variables
if not api_key:
    raise ValueError("GEMINI_API_KEY is not set")

if not default_system_prompt:
    raise ValueError(
        "GENERALIZE_GOAL_SPECIFIER_SYSTEM_PROMPT is not set"
    )


class PromptIntent(BaseModel):
    goal: str

    domain: Literal[
        "video_generation",
        "image_generation",
        "text_generation",
        "code_generation",
        "data_analysis",
        "web_research",
        "automation",
        "other"
    ]

    task_type: str
    confidence: float


client = genai.Client(api_key=api_key)


def analyze_prompt(
    prompt: str,
    model: str,
    system_prompt: str = default_system_prompt
) -> PromptIntent:

    full_prompt = f"""
    {system_prompt}

    User Prompt:
    {prompt}
    """

    response = client.models.generate_content(
        model=model,
        contents=full_prompt,
        config={
            "response_mime_type": "application/json",
            "response_json_schema": PromptIntent.model_json_schema(),
        }
    )

    return PromptIntent.model_validate_json(response.text)