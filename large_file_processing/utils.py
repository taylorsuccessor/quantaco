from datetime import datetime
from decimal import Decimal


def parse_datetime_from_custom_format(date_str):
    try:
        return datetime.strptime(date_str, "%d/%m/%Y %I:%M:%S %p")
    except Exception:
        return None


def convert_decimal_to_float(obj):
    if isinstance(obj, list):
        return [convert_decimal_to_float(item) for item in obj]
    elif isinstance(obj, dict):
        return {k: convert_decimal_to_float(v) for k, v in obj.items()}
    elif isinstance(obj, Decimal):
        return str(obj)
    else:
        return obj
