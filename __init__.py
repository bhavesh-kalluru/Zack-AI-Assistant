from .actions import execute_action
from .memory import save_command
from .gpt_engine import get_action

def action(user_input: str) -> str:
    """
    Top-level function to:
    - Save input
    - Send to GPT
    - Execute result
    """
    save_command(user_input)
    result = get_action(user_input)
    return execute_action(result)
