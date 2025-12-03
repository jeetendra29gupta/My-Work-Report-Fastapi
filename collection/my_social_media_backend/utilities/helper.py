from datetime import timezone, datetime


def get_utc_now():
    return datetime.now(timezone.utc)
