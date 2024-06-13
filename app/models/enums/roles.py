from enum import Enum


class Roles(Enum):
    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"
    TOOL = "tool"
    TOOL_CALLS = "tool_calls"
    FUNCTION = "function"
