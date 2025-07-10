import re
from datetime import datetime, timedelta
from typing import Any, Dict
import yaml

try:
    from ruamel.yaml import YAML
except ImportError:
    import yaml as YAML

from src.models.contracts import ContractFile
from pydantic import ValidationError

# Excel date base (1900-01-01, Excel's day 1 is 1900-01-01)
EXCEL_EPOCH = datetime(1899, 12, 30)

def parse_excel_date(value: Any) -> datetime:
    """
    Parse a date from Excel numeric or string format to a datetime object.
    """
    if isinstance(value, (int, float)):
        # Excel stores days since 1899-12-30
        return EXCEL_EPOCH + timedelta(days=float(value))
    if isinstance(value, str):
        # Try common date formats
        for fmt in ("%Y-%m-%d", "%d/%m/%Y", "%m/%d/%Y"):
            try:
                return datetime.strptime(value, fmt)
            except ValueError:
                continue
        raise ValueError(f"Unrecognized date string format: {value}")
    raise TypeError(f"Cannot parse date from value: {value}")

def load_contract_yaml(path: str) -> ContractFile:
    """
    Load and validate a versioned YAML contract file using Pydantic models.
    """
    if 'ruamel' in str(type(YAML)):
        yaml = YAML(typ='safe')
        with open(path, 'r', encoding='utf-8') as f:
            data = yaml.load(f)
    else:
        import yaml
        with open(path, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
    try:
        return ContractFile.model_validate(data)
    except ValidationError as e:
        raise ValueError(f"Contract YAML validation failed: {e}")

def get_column_mapping_for_date(contract: ContractFile, date: str) -> Dict[str, str]:
    """
    Given a ContractFile and a date string (YYYY-MM-DD), return the latest column_mapping whose version <= date.
    """
    target_date = datetime.strptime(date, "%Y-%m-%d")
    candidates = [v for v in contract.versions if datetime.strptime(v.version, "%Y-%m-%d") <= target_date]
    if not candidates:
        raise ValueError(f"No contract version found for date {date}")
    # Return the mapping from the latest version
    latest = max(candidates, key=lambda v: v.version)
    return latest.column_mapping

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
            return {
                'dataset': dataset,
                'period': m.group('period'),
                'version': m.group('version'),
                'contract': rules.get('contract')
            }
    raise ValueError(f"Filename {file_name} does not match any known dataset pattern.")


def validate_headers(headers: list, contract_path: str, period: str) -> None:
    """
    Validate that all required headers (from the contract for the given period) are present in the file.
    Raises ValueError if any required header is missing.
    """
    contract = load_contract_yaml(contract_path)
    # Find the correct mapping for the period (use first day of month for period)
    mapping = get_column_mapping_for_date(contract, period + "-01")
    required_headers = set(mapping.keys())
    missing = required_headers - set(headers)
    if missing:
        raise ValueError(f"Missing required headers: {missing}") 