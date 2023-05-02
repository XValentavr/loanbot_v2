import enum

import dotenv

envs = dotenv.dotenv_values()


class Creds(str, enum.Enum):
    """
    Class to get all envs from dotenv file
    """

    LOAN_BOT_ID: str = envs.get("LOAN_BOT_ID")
    MYSQL_HOST: str = envs.get("MYSQL_HOST")

    def __str__(self) -> str:
        return "%s" % self.value
