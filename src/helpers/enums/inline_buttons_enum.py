import enum


class InlineButtonsEnum(str, enum.Enum):
    BALANCE: str = "balance"
    INCOME: str = "income"
    INSERT: str = "insert"

    PREV_INCOMES: str = "prev_incomes"

    EARNINGS: str = 'earnings'
    EXPENSE: str = 'expense'
