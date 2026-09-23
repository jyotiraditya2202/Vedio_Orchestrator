from .ScripWorkers import (
    generate_initial_script,
    generate_asset_book,
)

def script_writer_orchestrator(state, task, original_prompt, video_specification):
    print("SCRIPT ORCHESTRATOR")
    print("=-=====================================================")

    initial_script = generate_initial_script(
        original_prompt=original_prompt,
        video_specification=video_specification
    )

    asset_book = generate_asset_book(
        original_prompt=original_prompt,
        video_specification=video_specification,
        initial_script=initial_script

    )
    

    print("Initial script generated:")
    print(initial_script)

    print("Asset genrated:")
    print(asset_book)
    # later:
    # retrieve workers
    # select worker
    # execute worker
    script = "Generated script..."

    return {
        "artifacts": {
            "script": script
        }
    }