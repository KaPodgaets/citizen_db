import yaml

from pydantic import BaseModel
from datetime import datetime, date
from dataclasses import dataclass

from src.models.contracts import ColumnMapping, ContractFile, ContractVersion

def parse_contract(raw: dict) -> ContractFile:
    result = {}
    for date_str, mapping_dict in raw.items():
        # Convert string key to datetime.date
        contract_date = datetime.strptime(date_str, "%Y-%m-%d").date()
        
        # Extract and wrap column_mapping
        mapping = ColumnMapping(mapping=mapping_dict)

        result[contract_date] = mapping

    return ContractFile(versions=result)

def get_closest_mapping_before(contract: ContractFile, incoming_period: date) -> ContractVersion:
    # Filter keys that are before the incoming period
    previous_dates = [x for x in contract.versions if x < incoming_period]
    
    if not previous_dates:
        raise ValueError(f"No contract versions exist before {incoming_period}")

    # Get the latest date before incoming_period
    closest_date = max(previous_dates)
    mapping = contract.versions[closest_date].mapping

    return ContractVersion(version_date=closest_date, mapping=mapping)