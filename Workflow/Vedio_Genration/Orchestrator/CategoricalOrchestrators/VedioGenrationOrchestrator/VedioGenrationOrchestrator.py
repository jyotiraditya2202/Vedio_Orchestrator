def video_generator_orchestrator(state, task, original_prompt, video_specification):
    print("VIDEO ORCHESTRATOR")

    script = state["artifacts"]["script"]

    video = "Generated video..."

    return {
        "artifacts": {
            "video": video
        }
    }