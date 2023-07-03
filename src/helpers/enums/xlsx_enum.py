import enum


class XlsxEnum(str, enum.Enum):
    NAME: str = 'loan.xlsx'

    def __str__(self) -> str:
        return "%s" % self.value
