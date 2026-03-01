from datetime import datetime


def generate_calendar_data():
    """
    Генерирует данные календаря на текущий учебный год (как было в Flask)
    """
    current_year = datetime.now().year
    current_month = datetime.now().month

    # Определяем учебный год (с сентября по август)
    if current_month >= 9:
        academic_year_start = current_year
        academic_year_end = current_year + 1
    else:
        academic_year_start = current_year - 1
        academic_year_end = current_year

    calendar_data = {
        "session_periods": [
            f"Зимняя сессия: 25.12.{academic_year_start} - 25.01.{academic_year_end}",
            f"Летняя сессия: 25.05.{academic_year_end} - 25.06.{academic_year_end}"
        ],
        "rest_periods": [
            f"Зимние каникулы: 26.01.{academic_year_end} - 07.02.{academic_year_end}",
            f"Летние каникулы: 26.06.{academic_year_end} - 31.08.{academic_year_end}",
            f"Осенние каникулы: 01.11.{academic_year_start} - 07.11.{academic_year_start}"
        ],
        "payment_deadline": f"Крайний срок оплаты: 10 числа каждого месяца",
        "important_dates": [
            f"День знаний: 01.09.{academic_year_start}",
            f"День университета: 15.10.{academic_year_start}",
            f"Начало зимней сессии: 25.12.{academic_year_start}",
            f"Начало летнего семестра: 07.02.{academic_year_end}",
            f"Последний звонок: 25.05.{academic_year_end}"
        ]
    }
    return calendar_data