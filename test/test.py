from Workflow.HelperFunction.Orchestrator import Orchestrator


def main():

    print("========================================")
    print("          AI Workflow Orchestrator")
    print("========================================")
    print()

    prompt = input("Enter your prompt: ")

    if not prompt.strip():
        print("Error: Prompt cannot be empty.")
        return

    print("\nRunning orchestrator...\n")

    try:

        orchestrator = Orchestrator()

        result = orchestrator.run(prompt)

        print("\n========== Result ==========")
        print(result)
        print("============================")

    except Exception as e:

        print("\n========== Error ==========")
        print(e)
        print("===========================")


if __name__ == "__main__":
    main()
