import pandera as pa
from pandera import Column, DataFrameSchema, Check

welfare_patients_schema = DataFrameSchema({
    "head_family_citizen_id": Column(pa.Int, nullable=False),
    "citizen_id": Column(pa.Int, nullable=False),
    "street_name": Column(pa.String, nullable=True),
    "street_code": Column(pa.Float64, nullable=True),
    "building_number": Column(pa.Float64, nullable=True),
    "apartment_number": Column(pa.Float64, nullable=True),
    "mobile_phone_number": Column(pa.String, nullable=True),
    "home_phone_number": Column(pa.String, nullable=True),
})