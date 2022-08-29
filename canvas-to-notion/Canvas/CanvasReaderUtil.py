from datetime import datetime, timezone

def utc_to_datetime(dtstr: str) -> datetime:
    """
    Args:
        dtstr (str): Expects '%Y-%m-%dT%H:%M:%SZ' format 
    """

    if dtstr is None:
        raise TypeError("dtstr is None! ")

    return datetime.strptime(dtstr, '%Y-%m-%dT%H:%M:%SZ').replace(tzinfo=timezone.utc).astimezone(tz=None)