from pydantic import BaseModel, Field
from typing import Dict, List
from pydantic import BaseModel
from datetime import datetime, date

class ColumnMapping(BaseModel):
    mapping: Dict[str, str]

class ContractFile(BaseModel):
    versions: Dict[date, ColumnMapping]

class ContractVersion(BaseModel):
    version_date: date
    mapping: Dict[str, str]