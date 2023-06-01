import calendar
import datetime


def get_current_month():
    current_date = datetime.date.today()
    previous_month = current_date.replace(day=1) - datetime.timedelta(days=1)
    previous_month_name = previous_month.strftime("%B")
    previous_month_year = previous_month.year
    return previous_month_name, previous_month_year


def get_prev_month(current_month):
    month_index = list(calendar.month_name).index(current_month.capitalize())
    return (month_index - 1) % 12
