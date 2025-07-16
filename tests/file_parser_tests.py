from src.utils.source_file_validator import parse_and_validate_filename


def test_file_name_parser_result(file_path='av_bait_2025-06_v-01.xlsx'):
    file_meta = parse_and_validate_filename(file_name=file_path)
    print(f"""
        dataset_name: {file_meta["dataset"]},
        period: {file_meta["period"]},
        version: {file_meta["version"]},
          """)
    assert file_meta["dataset"] == 'av_bait'
    assert file_meta["period"] == '2025-06'
    assert file_meta["version"] == 1