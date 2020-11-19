import datetime as dt
from datetime import datetime


def time_interval(start_interval, end_interval):
    """Функция для создания списка дат из выбранного интервала"""
    start_date = datetime.strptime(start_interval, "%Y-%m-%d").date()
    end_date = datetime.strptime(end_interval, "%Y-%m-%d").date()
    list_interval = [start_date + dt.timedelta(days=x) for x in range((end_date-start_date).days + 1)]
    return list_interval


