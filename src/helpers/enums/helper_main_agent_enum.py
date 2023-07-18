import enum


class HelperMainAgentEnum(str, enum.Enum):
    MAIN_ADMIN_USERNAME: list = ["Valentavr", "demkov"]
    MORE_HISTORY: str = 'MORE'
    LIMIT: int = 10
    MAIN_AGENT_HISTORY: str = 'AGENT_HISTORY'
    MAIN_AGENT_WITHDRAW: str = 'AGENT_WITHDRAW'

    MORE_BALANCE: str = 'MORE BALANCE'
