import pandera as pa
from pandera import Column, DataFrameSchema, Check

citizens_schema = DataFrameSchema({
    "citizen_id": Column(pa.Int, nullable=False),
    "first_name": Column(pa.String, nullable=False),
    "last_name": Column(pa.String, nullable=False),
    "birth_date": Column(pa.DateTime, nullable=True),
    "email": Column(pa.String, pa.Check.str_matches(r"^[^@\s]+@[^@\s]+\.[^@\s]+$"), nullable=True),
    "phone": Column(pa.String, nullable=True),
    "address": Column(pa.String, nullable=True),
    "created_at": Column(pa.DateTime, nullable=True),
}) 