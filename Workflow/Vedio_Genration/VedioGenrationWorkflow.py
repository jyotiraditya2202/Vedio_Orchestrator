from .VideoIntentDescriber import describe_video_intent
from .VedioGenrationPlanner import InitialPlanner


class VideoWorkflow:

    def __init__(self):
        self.intent_model = "gemini-3.5-flash-lite"
        self.planner = InitialPlanner()

    def run(self, prompt, intent):

        print("Running video workflow...")

        # 1. Describe video-specific requirements
        video_specification = describe_video_intent(
            prompt=prompt,
            intent=intent,
            model=self.intent_model
        )

        # 2. Create initial workflow plan + compiled LangGraph
        plan, workflow, video_specification = self.planner.create_plan(
            prompt,
            video_specification
        )

        print("\nInitial Plan:")
        print(plan)

        # 3. Execute the LangGraph workflow
        result = workflow.invoke({
            "original_prompt": prompt,
            "completed_tasks": [],
            "artifacts": {},
            "vedio_specification": video_specification
        })

        print("\nWorkflow completed.")
        return result