from typing import TypedDict, Annotated
import operator

from langgraph.graph import StateGraph, START, END

from ..CategoricalOrchestrators.DilougeWriterOrchestrator.DilougeWriterOrchestrator import dialogue_writer_orchestrator
from ..CategoricalOrchestrators.SfxGenratorOrchestrator.SfxGenratorOrchestrator import sfx_generator_orchestrator
from ..CategoricalOrchestrators.AudioGenrationOrchestrator.AudioGenrationOrchestrator import audio_generator_orchestrator
from ..CategoricalOrchestrators.VedioGenrationOrchestrator.VedioGenrationOrchestrator import video_generator_orchestrator
from ..CategoricalOrchestrators.VedioAssemblerOrchestrator.VedioAssemblerOrchestrator import video_assembler_orchestrator
from ..CategoricalOrchestrators.ScriptWritterOrchestrator.ScriptWritterOrchestrator import script_writer_orchestrator


class WorkflowState(TypedDict, total=False):
    original_prompt: str
    completed_tasks: Annotated[list[str], operator.add]
    artifacts: Annotated[dict, operator.ior]
    vedio_specification: str

ORCHESTRATORS = {
        "SCRIPT_WRITER": script_writer_orchestrator,
        "DIALOGUE_WRITER": dialogue_writer_orchestrator,
        "AUDIO_GENERATOR": audio_generator_orchestrator,
        "SFX_GENERATOR": sfx_generator_orchestrator,
        "VIDEO_GENERATOR": video_generator_orchestrator,
        "VIDEO_ASSEMBLER": video_assembler_orchestrator,
    }

def validate_workflow(plan):

    tasks = plan.tasks
    task_ids = [task.id for task in tasks]

    if len(task_ids) != len(set(task_ids)):
        raise ValueError("Duplicate task ID found")

    for task in tasks:

        if task.category not in ORCHESTRATORS:
            raise ValueError(
                f"Invalid category '{task.category}' "
                f"for task {task.id}"
            )

        for dependency in task.dependencies:

            if dependency not in task_ids:
                raise ValueError(
                    f"{task.id} depends on unknown task {dependency}"
                )

            if dependency == task.id:
                raise ValueError(
                    f"{task.id} cannot depend on itself"
                )

    return True

def workflow_designer(plan):

    validate_workflow(plan)

    graph = StateGraph(WorkflowState)

    for task in plan.tasks:

        orchestrator = ORCHESTRATORS[task.category]

        def run_task(
            state,
            task=task,
            orchestrator=orchestrator
            
        ):

            print(f"Running {task.id} - {task.category}")

            original_prompt = state["original_prompt"]

            result = orchestrator(
                state,
                task,
                original_prompt,
                video_specification=state.get("vedio_specification")
                )

            return {
                **result,
                "completed_tasks": [task.id]
            }

        graph.add_node(task.id, run_task)

    for task in plan.tasks:

        if not task.dependencies:
            graph.add_edge(START, task.id)

        for dependency in task.dependencies:
            graph.add_edge(dependency, task.id)

    for task in plan.tasks:

        has_child = any(
            task.id in other_task.dependencies
            for other_task in plan.tasks
        )

        if not has_child:
            graph.add_edge(task.id, END)

    return graph.compile()