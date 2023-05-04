from functools import wraps

from cruds.agent_cruds import agent_cruds


def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        agent = agent_cruds.get_by_username(username=args[0].from_user.username)
        if agent.is_login:
            return func(*args, **kwargs)

    return wrapper
