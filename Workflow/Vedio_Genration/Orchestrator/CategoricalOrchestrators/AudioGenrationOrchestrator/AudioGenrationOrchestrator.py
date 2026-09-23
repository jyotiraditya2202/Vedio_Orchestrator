def audio_generator_orchestrator(state, task, original_prompt, video_specification):
    print("AUDIO ORCHESTRATOR")

    script = state["artifacts"]["script"]

    audio = "Generated audio..."

    return {
        "artifacts": {
            "audio": audio
        }
    }