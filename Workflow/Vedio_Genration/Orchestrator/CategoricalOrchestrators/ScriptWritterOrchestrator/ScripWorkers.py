from pydantic import BaseModel, Field
from typing import List, Literal
import os
from google import genai
from typing import Optional
import os
import uuid
import base64
from pathlib import Path

from google import genai
from .....Prompts import (
    ASSET_DISCOVERY_SYSTEM_PROMPT,
    INITIAL_SCRIPT_GENERATOR_SYSTEM_PROMPT,
)

# ============================================================
# INITIAL SCRIPT SCHEMA
# ============================================================

class StoryBeat(BaseModel):
    beat_id: str
    title: str
    description: str
    purpose: str


class InitialScript(BaseModel):
    title: str
    logline: str
    hook: str
    premise: str
    main_characters: List[str]
    story_arc: List[StoryBeat]
    climax: str
    ending: str
    emotional_arc: List[str]
    estimated_duration: float
    estimated_scene_count: int
    overall_story: str


# ============================================================
# CHARACTER VERSION
# ============================================================

class CharacterVersion(BaseModel):

    version_id: str = Field(
        description=(
            "Unique ID for this visual evolution/version "
            "of the character."
        )
    )

    name: str = Field(
        description=(
            "Human-readable name of this character version."
        )
    )

    age_or_stage: str = Field(
        description=(
            "Approximate age, life stage, historical period, "
            "or evolution stage represented by this version."
        )
    )

    appearance: str = Field(
        description=(
            "Visual appearance of the character in this version. "
            "Describe age-related facial changes, hair, beard, "
            "body appearance, and other visual characteristics."
        )
    )

    outfit: str = Field(
        description=(
            "Typical clothing and accessories for this version. "
            "Describe only the outfit characteristics that should "
            "remain consistent within this version."
        )
    )

    appears_in: List[str] = Field(
        description=(
            "Story beat IDs where this character version appears."
        )
    )


# ============================================================
# ASSET
# ============================================================

class Asset(BaseModel):

    asset_id: str = Field(
        description=(
            "Stable identity ID for the real entity. "
            "This ID must remain the same across all visual "
            "evolution versions."
        )
    )

    name: str = Field(
        description="Human-readable name of the asset."
    )

    asset_type: Literal[
        "character",
        "location",
        "object"
    ]

    description: str = Field(
        description=(
            "Stable identity description of the asset. "
            "For characters, describe identity-defining features "
            "that should remain consistent even when age, outfit, "
            "or appearance evolves."
        )
    )

    consistency_importance: Literal[
        "high",
        "medium"
    ]

    appears_in: List[str]

    # --------------------------------------------------------
    # CHARACTER EVOLUTION
    # --------------------------------------------------------

    versions: List[CharacterVersion] = Field(
        default_factory=list,
        description=(
            "Visual evolution versions. Used primarily for "
            "characters whose age, outfit, role, or appearance "
            "changes throughout the story."
        )
    )


# ============================================================
# ASSET BOOK
# ============================================================

class AssetBook(BaseModel):
    assets: List[Asset]


# ============================================================
# GEMINI CLIENT
# ============================================================

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


# ============================================================
# INITIAL SCRIPT GENERATOR
# ============================================================

def generate_initial_script(
    original_prompt: str,
    video_specification: dict
) -> InitialScript:

    system_prompt = INITIAL_SCRIPT_GENERATOR_SYSTEM_PROMPT

    user_prompt = f"""
    Create an initial story blueprint for the following video.

    ORIGINAL USER PROMPT:
    {original_prompt}

    VIDEO SPECIFICATION:
    {video_specification}

    Create a compelling story suitable for this exact request.

    Pay particular attention to:

    - hook strength
    - story originality
    - character motivation
    - conflict
    - escalation
    - emotional journey
    - pacing
    - climax
    - ending
    - suitability for the requested duration

    Return only the structured story blueprint.
    """

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=user_prompt,
        config={
            "system_instruction": system_prompt,
            "response_mime_type": "application/json",
            "response_schema": InitialScript,
        }
    )

    return response.parsed


# ============================================================
# ASSET DISCOVERY
# ============================================================

def generate_asset_book(
    original_prompt: str,
    video_specification: dict,
    initial_script: InitialScript
) -> AssetBook:

    system_prompt = ASSET_DISCOVERY_SYSTEM_PROMPT

    user_prompt = f"""
    Discover the persistent visual assets required for this video.

    ORIGINAL USER PROMPT:
    {original_prompt}

    VIDEO SPECIFICATION:
    {video_specification}

    INITIAL STORY BLUEPRINT:
    {initial_script.model_dump_json(indent=2)}

    Analyze the entire story.

    Identify only visual assets whose identity needs to remain
    consistent during production.

    For characters:

    - create ONE stable asset identity
    - create versions for meaningful age/life-stage/appearance
    evolution
    - keep the underlying facial identity consistent
    - do not create separate unrelated character identities
    merely because the character ages or changes outfit

    For locations and objects:

    - create only important continuity-critical assets

    Be selective.

    Return only the structured AssetBook.
    """

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=user_prompt,
        config={
            "system_instruction": system_prompt,
            "response_mime_type": "application/json",
            "response_schema": AssetBook,
        }
    )

    return response.parsed
