from google import genai
from pydantic import BaseModel, Field
from typing import Dict, Any, List
from dotenv import load_dotenv
import os

from ..HelperFunction.GenralizeGoalSpecifier import PromptIntent
from ..Prompts import VIDEO_INTENT_DESCRIBER_SYSTEM_PROMPT


# Load environment variables
load_dotenv()


# Configuration
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY is not set")


# Video Deliverable Schema
class VideoDeliverable(BaseModel):
    audio: bool = True
    sfx: bool = False


# Video Specification Schema
class VideoSpecification(BaseModel):

    # Core Goal
    goal: str

    # Core Content Understanding
    core_topic: str = "unspecified"

    content_type: str = "unspecified"
    # Examples:
    # educational
    # entertainment
    # advertisement
    # storytelling
    # documentary
    # cinematic
    # tutorial

    knowledge_level: str = "general"
    # Examples:
    # beginner
    # intermediate
    # advanced
    # general

    # Narrative / Script Requirements
    pace: str = "normal"
    # slow / normal / fast / very_fast

    tone: List[str] = Field(
        default_factory=lambda: ["neutral"]
    )
    # Examples:
    # dramatic
    # curious
    # entertaining
    # emotional
    # humorous
    # serious

    # Video Constraints
    video_duration: str = "5 seconds"

    quality: str = "720p"

    aspect_ratio: str = "16:9"

    visual_style: str = "unspecified"

    character_consistency_required: bool = True

    language: str = "English"

    deliverable: VideoDeliverable = Field(
        default_factory=VideoDeliverable
    )

    script_provided: bool = False

    other_guidelines: Dict[str, Any] = Field(
        default_factory=dict
    )



# Gemini Client
client = genai.Client(api_key=api_key)


# Video Intent Describer
def describe_video_intent(
    prompt: str,
    intent: PromptIntent,
    model: str
) -> VideoSpecification:

    full_prompt = f"""

    General Intent:
    {intent.model_dump_json()}

    Original User Prompt:
    {prompt}

    {VIDEO_INTENT_DESCRIBER_SYSTEM_PROMPT}

    """

    response = client.models.generate_content(
        model=model,
        contents=full_prompt,
        config={
            "response_mime_type": "application/json",
            "response_json_schema": VideoSpecification.model_json_schema(),
        }
    )

    print("Vedio Specification Test")
    print(response)

    return VideoSpecification.model_validate_json(response.text)