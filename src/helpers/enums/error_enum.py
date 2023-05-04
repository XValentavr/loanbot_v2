import enum


class ErrorEnum(str, enum.Enum):
    CURRENCY_NOT_FOUND: str = "Валюта не найдена, попробуйте ещё раз"
