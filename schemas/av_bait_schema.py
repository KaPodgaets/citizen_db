import pandera.pandas as pa
from pandera.pandas import Column, DataFrameSchema

av_bait_schema = DataFrameSchema({
    "citizen_id": Column(pa.Int, nullable=False),
    "first_name": Column(pa.String, nullable=True),
    "last_name": Column(pa.String, nullable=False),
    "age": Column(pa.Int, nullable=False),
    # "birth_date": Column(pa.DateTime, nullable=True),
    "street_name": Column(pa.String, nullable=True),
    "street_code": Column(pa.Int, nullable=False),
    "building_number": Column(pa.Int, nullable=False),
    "apartment_number": Column(pa.Int, nullable=False),
    "family_index_number": Column(pa.Int, nullable=False),
}) 