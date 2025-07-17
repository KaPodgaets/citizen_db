import re
import yaml
from datetime import datetime

from src.utils.yaml_parser import parse_contract, get_closest_mapping_before\


def parse_and_validate_filename(file_name: str, dataset_config_path: str = "datasets_config.yml") -> dict:
    """
    Parse and validate the filename using the regex from datasets_config.yml.
    Returns a dict with dataset, period, version if valid, else raises ValueError.
    """
    with open(dataset_config_path, 'r', encoding='utf-8') as f:
        config = yaml.safe_load(f)
    for dataset, rules in config.items():
        pattern = rules.get('filename_regex')
        if not pattern:
            continue
        m = re.match(pattern, file_name)
        if m:
            version_str = m.group('version')
            try:
                version = int(version_str)
            except (TypeError, ValueError):
                version = version_str  # fallback to original if conversion fails
            return {
                'dataset': dataset,
                'period': m.group('period'),
                'version': version,
                'contract': rules.get('contract')
            }
    raise ValueError(f"Filename {file_name} does not match any known dataset pattern.")


def validate_headers(headers: list, contract_path: str, period: str) -> None:
    """
    Validate that all required headers (from the contract for the given period) are present in the file.
    Raises ValueError if any required header is missing.
    """
    # read yaml file to get contracts as raw string
    with open(contract_path, encoding="utf-8") as f:
        raw_contract = yaml.safe_load(f)

    dataset_contract_file = parse_contract(raw_contract)

    period_as_date = datetime.strptime(period + "-01", "%Y-%m-%d").date()

    # Find the correct mapping for the period (use first day of month for period)
    contract_version = get_closest_mapping_before(dataset_contract_file, period_as_date)
    required_headers = set(contract_version.mapping.keys())
    missing = required_headers - set(headers)
    if missing:
        raise ValueError(f"Missing required headers: {missing}") 