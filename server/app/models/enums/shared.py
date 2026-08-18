from enum import Enum


class AgentPermissionLevel(str, Enum):
    PROPOSE_ONLY = "propose_only"
    ACT_FREELY = "act_freely"
    ACT_WITH_NOTIFY = "act_with_notify"


class TaskStatus(str, Enum):
    OPEN = "open"
    IN_PROGRESS = "in_progress"
    IN_REVIEW = "in_review"
    DONE = "done"
    BLOCKED = "blocked"
    CANCELLED = "cancelled"


class TaskPriority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class CreatedBy(str, Enum):
    HUMAN = "human"
    AGENT = "agent"


class ApprovalStatus(str, Enum):
    NONE = "none"
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
