import pandera.pandas as pa
from pandera import Column, DataFrameSchema

breath_troubles_schema = DataFrameSchema({
    "citizen_id": Column(pa.Int, nullable=False),
    "phone_number": Column(pa.String, nullable=True),
    "phone_number_contact_person": Column(pa.String, nullable=True),
})