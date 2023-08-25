from datetime import datetime, timedelta


def get_datetime(delay: int) -> datetime:
    """
    :param delay: how many minutes to add to the datetime
    :return: datetime
    
    """
    return datetime.now().replace(
        microsecond=0,
        second=0
    ) + timedelta(minutes=delay)
