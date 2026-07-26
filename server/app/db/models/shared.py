from enum import Enum as EnumBase


class AgentPermissionLevel(str, EnumBase):
    PROPOSE_ONLY = "propose_only"
    ACT_FREELY = "act_freely"
    ACT_WITH_NOTIFY = "act_with_notify"
