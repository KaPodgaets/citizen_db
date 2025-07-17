import pandera.pandas as pa
from pandera import Column, DataFrameSchema

new_immigrants_schema = DataFrameSchema({
    "citizen_id": Column(pa.Int, nullable=False),
    "citizen_phone_number_1": Column(pa.String, nullable=True),
    "citizen_phone_number_2": Column(pa.String, nullable=True),
    "is_left_the_city": Column(pa.String, nullable=True),
})