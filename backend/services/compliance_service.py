from datetime import datetime, time
import holidays
import pytz


IST = pytz.timezone("Asia/Kolkata")
india_holidays = holidays.India()


def is_weekend(current_date):
    # Saturday = 5, Sunday = 6
    return current_date.weekday() >= 5


def is_indian_holiday(current_date):
    return current_date in india_holidays


def is_within_business_hours(current_time):
    start = time(6, 0)   # 6 AM
    end = time(18, 0)    # 6 PM
    return start <= current_time <= end


def can_send_email_now():
    now = datetime.now(IST)
    today = now.date()
    current_time = now.time()

    if is_weekend(today):
        return False

    if is_indian_holiday(today):
        return False

    if not is_within_business_hours(current_time):
        return False

    return True