import os
import tempfile
import yaml
import pytest
from src.utils import source_file_validator

# Sample datasets_config.yml content
DATASETS_CONFIG = {
    'citizens': {
        'filename_regex': r'^citizens_(?P<period>\\d{4}-\\d{2})_v(?P<version>\\d+)\\.csv$',
        'contract': 'citizens_contract.yml'
    }
}

# Sample contract YAML content
CONTRACT_YAML = {
    '2024-01': {
        'mapping': {
            'id': 'citizen_id',
            'name': 'full_name',
            'dob': 'date_of_birth'
        }
    }
}

def write_yaml(tmp_path, data, filename):
    path = tmp_path / filename
    with open(path, 'w', encoding='utf-8') as f:
        yaml.safe_dump(data, f)
    return str(path)

def test_parse_and_validate_filename(tmp_path):
    config_path = write_yaml(tmp_path, DATASETS_CONFIG, 'datasets_config.yml')
    # Valid filename
    result = source_file_validator.parse_and_validate_filename('citizens_2024-01_v1.csv', config_path)
    assert result['dataset'] == 'citizens'
    assert result['period'] == '2024-01'
    assert result['version'] == '1'
    assert result['contract'] == 'citizens_contract.yml'
    # Invalid filename
    with pytest.raises(ValueError):
        source_file_validator.parse_and_validate_filename('invalidfile.csv', config_path)

def test_validate_headers(tmp_path, monkeypatch):
    # Write contract YAML
    contract_path = write_yaml(tmp_path, CONTRACT_YAML, 'citizens_contract.yml')
    # Patch parse_contract and get_closest_mapping_before to use our YAML
    def fake_parse_contract(path):
        with open(path, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
        class ContractVersion:
            def __init__(self, mapping):
                self.mapping = mapping
        class ContractFile:
            pass
        cf = ContractFile()
        cf.versions = [ContractVersion(data['2024-01']['mapping'])]
        return cf
    def fake_get_closest_mapping_before(contract_file, period):
        # Always return the only mapping
        return type('FakeMapping', (), {'mapping': CONTRACT_YAML['2024-01']['mapping']})()
    monkeypatch.setattr(source_file_validator, 'parse_contract', fake_parse_contract)
    monkeypatch.setattr(source_file_validator, 'get_closest_mapping_before', fake_get_closest_mapping_before)
    # Valid headers
    headers = ['id', 'name', 'dob']
    source_file_validator.validate_headers(headers, contract_path, '2024-01')
    # Missing header
    with pytest.raises(ValueError) as excinfo:
        source_file_validator.validate_headers(['id', 'name'], contract_path, '2024-01')
    assert 'Missing required headers' in str(excinfo.value) 