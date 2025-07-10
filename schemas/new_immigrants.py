import pandera as pa
from pandera import Column, DataFrameSchema, Check

new_immigrants_schema = DataFrameSchema({
    "citizen_id": Column(pa.Int, nullable=False),
    "street_name": Column(pa.String, nullable=True),
    "street_code": Column(pa.String, nullable=True),
    "building_number": Column(pa.String, nullable=True),
    "apartment_number": Column(pa.String, nullable=True),
}) 