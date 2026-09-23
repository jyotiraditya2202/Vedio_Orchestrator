from dataclasses import dataclass, field
from typing import Any
from google import genai
from dotenv import load_dotenv
import os
import json

from ..Prompts import GENERAL_CATEGORY_INFORMATION
from .Orchestrator.Helper.WorkflowDesigner import workflow_designer


load_dotenv()


@dataclass
class Task:
    id: str
    category: str
    description: str
    dependencies: list[str] = field(default_factory=list)


@dataclass
class VideoGenerationPlan:
    goal: str
    tasks: list[Task] = field(default_factory=list)


class InitialPlanner:

    def __init__(self):
        self.client = genai.Client(
            api_key=os.getenv("GEMINI_API_KEY")
        )

    def create_plan(
        self,
        prompt: str,
        video_specification: str
    ) -> VideoGenerationPlan:

        planning_prompt = f"""
        You are the High-Level Planner of a video-generation orchestrator.

        USER REQUEST:
        {prompt}

        VIDEO SPECIFICATION:
        {video_specification}

        AVAILABLE CATEGORIES:
        {GENERAL_CATEGORY_INFORMATION}

        The USER REQUEST is the primary source of requirements.
        VIDEO SPECIFICATION only provides additional context about duration,
        complexity, style, scenes, resolution, audio, and other constraints.

        YOUR ROLE:

        Create the smallest effective category-level workflow required to
        satisfy the user request.

        You decide:
        - which categories are required
        - what each category must accomplish
        - dependencies between categories

        The selected category's own orchestrator decides:
        - which workers to use
        - how to perform the task
        - detailed internal steps

        Do NOT plan individual workers.
        Do NOT execute tasks.
        Do NOT generate the final video.

        PLANNING RULES:

        1. Satisfy the USER REQUEST first.
        2. Select only categories that are actually required.
        3. Keep simple requests simple.
        4. Use additional categories only when the request requires them.
        5. Consider video duration and complexity when deciding whether
        specialized categories are necessary.
        6. Respect dependencies between categories.
        7. Independent categories should not depend on each other unnecessarily.
        8. Optimize for quality while minimizing unnecessary cost and steps.
        9. Never omit a genuinely required category just to reduce cost.
        10. The resulting workflow must be executable.
        11. Use only categories listed in AVAILABLE CATEGORIES.
        12. VIDEO_ASSEMBLER is required when separately generated video,
            audio, dialogue, or SFX must be synchronized or combined.

        OUTPUT:

        Return valid JSON only.

        Schema:

        {{
        "tasks": [
            {{
            "id": "T0",
            "category": "CATEGORY_NAME",
            "description": "What this category must accomplish",
            "dependencies": []
            }}
        ]
        }}
        """

        # -----------------------------
        # 1. Ask LLM to create plan
        # -----------------------------

        response = self.client.models.generate_content(
            model="gemini-3.5-flash-lite",
            contents=planning_prompt,
            config={
                "response_mime_type": "application/json"
            }
        )

        # -----------------------------
        # 2. Convert JSON to objects
        # -----------------------------

        data = json.loads(response.text)

        tasks = [
            Task(
                id=task["id"],
                category=task["category"],
                description=task["description"],
                dependencies=task.get("dependencies", [])
            )
            for task in data["tasks"]
        ]

        plan = VideoGenerationPlan(
            goal=prompt,
            tasks=tasks
        )

        # -----------------------------
        # 3. Convert plan to LangGraph
        # -----------------------------

        workflow = workflow_designer(plan)
        # -----------------------------
        # 4. Return both
        # -----------------------------

        return plan, workflow, video_specification
