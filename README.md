# Agentic AI Workbench

An LLM-powered software engineering workbench that autonomously executes repository-level coding tasks using constrained tools, persistent task management, independent verification, automated review, and structured handoffs.

## 1. Overview

Agentic AI Workbench automates coding tasks across existing GitHub repositories.

Given a repository URL and a clearly defined coding task, the workbench initializes the execution environment, registers the task, and delegates implementation to an LLM-powered agent.

The agent interacts with the repository through controlled tools, modifies permitted files, and executes relevant commands. Its execution results pass through independent verification and review before a structured handoff is generated.

The system maintains persistent task and agent state to support execution tracking and failure diagnosis.

## 2. Key Features

- **Autonomous Coding Agent:** Uses an LLM to inspect repositories, understand coding tasks, and execute multi-step development workflows.
- **Constrained Tool Execution:** Restricts file modifications using allowed-file and forbidden-file rules.
- **Persistent Task Board:** Tracks task IDs, descriptions, and execution statuses.
- **Agent State Management:** Maintains active task information, modified files, blockers, and next actions.
- **Independent Verification:** Checks execution evidence against task acceptance criteria.
- **Automated Review:** Evaluates verification results and scope violations before approving or rejecting a task.
- **Failure Handling:** Records failures during agent execution, verification, review, and handoff generation.
- **Structured Handoff:** Produces a final packet containing task summary, modified files, blockers, and next action.
- **Command-Line Interface:** Supports repository-level task execution through configurable CLI arguments.

## 3. Architecture

The workbench follows a modular architecture in which individual components handle distinct stages of the software engineering workflow.

| Component | Responsibility |
|---|---|
| `agent.py` | Executes the LLM-driven coding agent and manages its tool interaction loop. |
| `llm.py` | Handles Groq API communication. |
| `tools.py` | Implements tools exposed to the agent. |
| `tool_guard.py` | Enforces restrictions on permitted repository operations. |
| `constraints.py` | Handles task-level execution constraints. |
| `task_input.py` | Validates, creates, and registers coding tasks. |
| `task_board.py` | Maintains persistent task records and execution statuses. |
| `state.py` | Manages persistent agent execution state. |
| `verifier.py` | Checks execution results against acceptance criteria. |
| `reviewer.py` | Independently reviews execution and verification outcomes. |
| `handoff.py` | Generates structured handoff packets. |
| `orchestrator.py` | Coordinates the agent, verifier, reviewer, and handoff stages. |
| `github.py` | Handles GitHub repository cloning. |
| `initializer.py` | Initializes workbench state and task board. |
| `workbench.py` | Provides the public workbench execution interface. |
| `cli.py` | Exposes workbench functionality through a command-line interface. |

## 4. Execution Workflow

1. **Task Input:** The user provides a repository URL, task description, allowed files, forbidden files, and acceptance criteria.
2. **Initialization:** The workbench checks for `AGENTS.md` and initializes persistent task and agent state.
3. **Task Registration:** A validated task is added to the persistent task board.
4. **Repository Preparation:** The specified GitHub repository is cloned into the requested workspace.
5. **Agent Execution:** The coding agent inspects the repository, plans the implementation, and interacts with controlled tools.
6. **Verification:** The verifier evaluates execution evidence against acceptance criteria.
7. **Review:** The reviewer assesses scope violations and verification outcomes.
8. **Handoff:** A structured handoff packet is generated with the task outcome, modified files, blockers, and next action.

## 5. Technology Stack

- **Language:** Python 3.11+
- **LLM Integration:** Groq API
- **Model:** `openai/gpt-oss-120b`
- **Agent Framework:** Custom tool-calling agent loop
- **Version Control:** Git and GitHub
- **Testing:** Pytest
- **Linting:** Ruff
- **Type Checking:** Mypy

## 6. Project Structure

```text
AI-workbench/
│
├── agent.py
├── llm.py
├── tools.py
├── tool_guard.py
├── constraints.py
├── feedback.py
│
├── task_input.py
├── task_board.py
├── state.py
│
├── verifier.py
├── reviewer.py
├── handoff.py
│
├── orchestrator.py
├── github.py
├── initializer.py
├── workbench.py
├── cli.py
│
├── AGENTS.md
├── pyproject.toml
├── .gitignore
│
├── test_files/
│   ├── test_agent_robustness.py
│   ├── test_workbench_e2e.py
│   ├── test_task_board.py
│   ├── test_tool_guard.py
│   ├── test_verifier.py
│   ├── test_reviewer.py
│   └── ...
│
└── workdir/
    ├── task_board.json
    ├── agent_state.json
    └── repository workspaces/
```

## 7. Installation and Setup

### Clone the repository

```bash
git clone <YOUR-WORKBENCH-REPOSITORY-URL>
cd AI-workbench
```

### Create a virtual environment

```bash
python3 -m venv agentic-ai
source agentic-ai/bin/activate
```

### Install dependencies

```bash
pip install -e ".[dev]"
```

### Configure the Groq API key

Create a `.env` file in the project root:

```env
GROQ_API_KEY=your_groq_api_key
```

Never commit API keys or other secrets to version control.

### Verify installation

```bash
python cli.py --help
```

## 8. Usage

The workbench can be executed through its command-line interface.

### Example

```bash
python cli.py \
  --repo-url https://github.com/OWNER/REPOSITORY.git \
  --workspace workdir/demo_repo \
  --task-id add-input-validation \
  --description "Add input validation to the data processing module" \
  --allowed-files src/data.py tests/test_data.py \
  --acceptance "Invalid input is rejected" "All tests pass" \
  --forbidden-files config/secrets.py
```

### CLI Arguments

| Argument | Description |
|---|---|
| `--repo-url` | GitHub repository URL. |
| `--workspace` | Local destination for the repository clone. |
| `--task-id` | Unique task identifier. |
| `--description` | Coding task description. |
| `--allowed-files` | Files the agent is permitted to modify. |
| `--acceptance` | Acceptance criteria used during verification. |
| `--forbidden-files` | Files the agent must not modify. |

The CLI displays three outputs:

- Execution Result
- Review
- Handoff

It returns a successful exit code when the reviewer approves the task.

## 9. Persistent State

The workbench maintains runtime information under `workdir/`.

- `task_board.json`: Stores registered tasks and their execution statuses.
- `agent_state.json`: Stores the active task, touched files, blockers, and next action.

These files are generated at runtime and should not be committed as project source files.

## 10. Safety and Reliability

The workbench incorporates multiple safeguards:

- File-level access restrictions through allowed and forbidden file lists.
- Controlled tool execution.
- Task acceptance criteria for verification.
- Independent review of verification outcomes.
- Exception handling across agent execution, verification, review, and handoff generation.
- Persistent recording of task failures and execution blockers.

A successful agent response alone does not guarantee task approval. The result must pass verification and review.

## 11. Testing

The project uses Pytest for automated testing.

Run the automatically discovered test suite:

```bash
pytest -q
```

Run the end-to-end tests separately:

```bash
pytest test_files/test_workbench_e2e.py -q
```

Run a specific test:

```bash
pytest test_files/test_workbench_e2e.py::test_workbench_end_to_end_approved_task -q
```

The end-to-end tests cover successful execution, rejected tasks, and exceptions during agent execution, verification, review, and handoff generation.

Some manually invoked demonstration scripts may contact external APIs or execute real repository tasks. Review them before running.

## 12. Current Limitations

- The current LLM integration uses the Groq API.
- Execution quality depends on the selected model and task description.
- The system requires explicit file-level scope and acceptance criteria.
- Automated verification depends on the availability and quality of repository tests.
- Handoff generation is currently returned to the caller rather than persisted as a separate artifact.
- A successful demonstration on one repository does not guarantee compatibility with every repository or development environment.

## 13. Future Improvements

- Persistent handoff artifact storage.
- Support for additional LLM providers.
- More advanced planning and retry strategies.
- Improved repository-level context retrieval.
- Richer execution logs and observability.
- Automated recovery and task resumption.

## Project Goal

The goal of Agentic AI Workbench is to move beyond simple code generation toward a structured autonomous software engineering workflow in which coding agents can inspect repositories, implement scoped changes, validate their work, undergo independent review, and produce actionable handoffs.