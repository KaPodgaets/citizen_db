from datetime import datetime, timedelta
from typing import Any

# Excel date base (1900-01-01, Excel's day 1 is 1900-01-01)
EXCEL_EPOCH = datetime(1899, 12, 30)

def parse_excel_date(value: Any) -> datetime:
    """
    Parse a date from Excel numeric or string format to a datetime object.
    """
    if isinstance(value, (int, float)):
        # Excel stores days since 1899-12-30
        return EXCEL_EPOCH + timedelta(days=float(value))
    if isinstance(value, str):
        # Try common date formats
        for fmt in ("%Y-%m-%d", "%d/%m/%Y", "%m/%d/%Y"):
            try:
                return datetime.strptime(value, fmt)
            except ValueError:
                continue
        raise ValueError(f"Unrecognized date string format: {value}")
    raise TypeError(f"Cannot parse date from value: {value}")