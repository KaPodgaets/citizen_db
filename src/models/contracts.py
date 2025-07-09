from pydantic import BaseModel, Field
from typing import Dict, List

class ContractVersion(BaseModel):
    version: str = Field(pattern=r'^\d{4}-\d{2}-\d{2}$')
    column_mapping: Dict[str, str]

class ContractFile(BaseModel):
    versions: List[ContractVersion] 