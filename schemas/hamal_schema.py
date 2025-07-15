import pandera.pandas as pa
from pandera import Column, DataFrameSchema

hamal_schema = DataFrameSchema({
    "citizen_fid": Column(pa.Int, nullable=False),
    "file_name": Column(pa.String, nullable=False),
    "is_answered_the_call": Column(pa.Bool, nullable=False),
    "is_lonely": Column(pa.Bool, nullable=False),
    "is_address_wrong": Column(pa.Bool, nullable=False),
    "new_street_name": Column(pa.String, nullable=True),
    "new_building_number": Column(pa.String, nullable=True),
    "new_appartment_number": Column(pa.String, nullable=True),
    "has_mamad": Column(pa.Bool, nullable=False),
    "has_miklat_prati": Column(pa.Bool, nullable=False),
    "has_miklat_ziburi": Column(pa.Bool, nullable=False),
    "has_mobility_restriction": Column(pa.Bool, nullable=False),
    "is_dead": Column(pa.Bool, nullable=False),
    "is_left_the_ctiry_permanent": Column(pa.Bool, nullable=False),
    "has_temporary_address": Column(pa.Bool, nullable=False),
    "is_temporary_abroad": Column(pa.Bool, nullable=False),
    "temporary_street_name": Column(pa.String, nullable=True),
    "temporary_building_number": Column(pa.String, nullable=True),
    "temporary_appartment": Column(pa.String, nullable=True),
    "appearance_count": Column(pa.Int, nullable=True),
    "calcenter_case_number": Column(pa.String, nullable=True)
})