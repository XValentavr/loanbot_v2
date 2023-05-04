import enum


class CurrencyEnum(str, enum.Enum):
    DOLLAR: str = '$'
    EURO: str = '€'
    UAH: str = "₴"

    def __str__(self) -> str:
        return "%s" % self.value
