import enum

import dotenv

envs = dotenv.dotenv_values()


class Creds(str, enum.Enum):
    """
    Class to get all envs from dotenv file
    """

    LOAN_BOT_ID: str = envs.get("LOAN_BOT_ID")
    MYSQL_HOST: str = envs.get("MYSQL_HOST")
    CURRENCY_API_ID: str = envs.get('CURRENCY_API_ID')
    CURRENCY_URL: str = envs.get('CURRENCY_URL')
    OWNER_USER_ID: str = envs.get('OWNER_USER_ID')

    def __str__(self) -> str:
        return "%s" % self.value
