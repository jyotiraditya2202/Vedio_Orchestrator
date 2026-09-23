from .GenralizeGoalSpecifier import analyze_prompt
from .WorkFlowRouter import route_workflow


class Orchestrator:

    def __init__(self):
        self.intent_model = "gemini-3.5-flash-lite"

    def run(self, prompt: str):

        intent = analyze_prompt(
            prompt=prompt,
            model=self.intent_model
        )

        workflow = route_workflow(intent)

        result = workflow.run(
            prompt=prompt,
            intent=intent
        )

        return result

