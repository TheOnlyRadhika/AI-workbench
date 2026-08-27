from dataclasses import dataclass , field
from enum import Enum


class TaskStatus(Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"

@dataclass
class Task:
    id : str
    description : str
    allowed_files: list[str]
    forbidden_files : list[str]
    acceptance : list[str]
    status: TaskStatus = field(
        default_factory=lambda: TaskStatus.PENDING
    )

@dataclass
class RunResult:
    label : str
    files_touched : list[str] = field(default_factory = list)
    tests_run : bool = False
    declared_success : bool = False
    actually_passing : bool = False
    scope_violations: list[str] = field(default_factory = list)
    notes : list[str] = field(default_factory=list)
    command_results: list[dict] = field(default_factory=list)
        
    def summary(self)-> dict:
        return{
            "label" : self.label,
            "test_run" : self.tests_run,
            "declared_success" : self.declared_success,
            "actually_passing" : self.actually_passing,
            "notes" : self.notes
        }


@dataclass
class AgentState:
    active_task : str | None = None
    touched_files : list[str] = field(default_factory= list)
    next_action : str | None = None
    assumptions : list[str] = field(default_factory = list)
    blockers : list[str] = field(default_factory = list)
    last_updated: str | None = None


@dataclass
class TaskItem:
    id: str
    goal: str
    owner: str
    status: str
    acceptance: list[str] = field(default_factory=list)


@dataclass
class TaskBoard:
    tasks: list[TaskItem] = field(default_factory=list)

@dataclass
class ScopeContract:
    allowed_files: list[str] = field(default_factory=list)
    forbidden_files: list[str] = field(default_factory=list)


@dataclass
class ReviewResult:
    approved: bool
    issues: list[str] 
    notes : list[str]

@dataclass
class CommandResult:
    command : str
    stdout: str
    stderr: str
    exit_code: int

    @property
    def passed(self) -> bool:
        return self.exit_code == 0



@dataclass
class HandOffPacket:

    task_id: str
    summary: dict
    files_touched : list[str] = field(default_factory = list)
    blockers : list[str] = field(default_factory = list)
    next_action: str | None = None
    






