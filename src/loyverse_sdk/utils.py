from datetime import datetime


def standardize_datetime_str(dt: datetime) -> str:
    """Coverts datetime object to ISO 8601 format"""
    assert isinstance(dt, datetime), "dt must be a datetime object"
    return dt.isoformat(timespec="milliseconds") + "Z"
