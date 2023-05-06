from functools import wraps

from create_engine import session
from cruds.agent_cruds import agent_cruds


def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):

        session.commit()

        agent = agent_cruds.get_by_username(username=args[0].from_user.username)
        if agent.is_login:
            return func(*args, **kwargs)

    return wrapper
