from ..Vedio_Genration.VedioGenrationWorkflow import VideoWorkflow
from .GenralizeGoalSpecifier import PromptIntent

def route_workflow(intent: PromptIntent):

    if intent.domain == "video_generation":
        return VideoWorkflow()

    # elif intent.domain == "image_generation":
    #     return image_workflow()

    else:
        raise ValueError(
            f"No workflow available for domain: {intent.domain}"
        )