import pandera.pandas as pa
from pandera import Column, DataFrameSchema

meser_schema = DataFrameSchema({
    "citizen_id": Column(pa.Int, nullable=False),
    "street_name": Column(pa.String, nullable=True),
    "building_number": Column(pa.String, nullable=True),
    "apartment_number": Column(pa.String, nullable=True),
    "phone_number_1": Column(pa.String, nullable=True),
    "phone_number_2": Column(pa.String, nullable=True),
})