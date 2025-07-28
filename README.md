# ReadMe
This is project to integrate municipality data sources about citizens from different information systems.
## Description
### Pre-Requisites
- Admin rights on user to be able to install new applications and run CMD commands
- Ask your Sagi to add you rights in MS SQL Server

# Step by step guide
N.B. All CMD commands have to be executed from root project dir

### Project set up
#### Python Prerequisites
- install python
```
python --version                            # check is Python istalled and its version
winget install --id Python.Python.3.12      # intall LTS version of Python (if not installed)
winget upgrade --id Python.Python.3.12      # update your Python to current version (if installed)
```
- install dependencies
```bash
pip install pandas sqlalchemy pyodbc pydantic-settings pyyaml
```

### Set up the DataBase
1. Drop all tables and db and create new (WARNING! YOU WILL LOST YOUR DATA!)
```bash
python src/create_db_from_env.py
```
2. Create all tables
```bash
python src/run_ddl_scripts.py
```

### Workflow
- step 0 - backfill fake_ids if exist
```bash
python src/backfill_citizen_fid.py --filepath data/snapshots/fake_id-2025-07-27.xlsx
```
- step 1 - after run commands, check the DB status
```bash
python src/ingest.py --file-path data/land/av_bait_2025-06_v-01.xlsx
python src/ingest.py --file-path data/land/welfare_patients_2025-06_v-01.xlsx
python src/ingest.py --file-path data/land/new_immigrants_2024-12_v-01.xlsx
python src/ingest.py --file-path data/land/meser_2025-06_v-01.xlsx
python src/ingest.py --file-path data/land/hazramim_2025-05_v-01.xlsx
python src/ingest.py --file-path data/land/breath_troubles_2025-06_v-01.xlsx
python src/ingest.py --file-path data/land/hamal_2025-07_v-02.xlsx
python src/run_pipeline.py
```
- step 2 - after run commands, check the DB status
```bash
python src/ingest.py --file-path data/land/av_bait_2025-07_v-01.xlsx
python src/ingest.py --file-path data/land/welfare_patients_2025-07_v-01.xlsx
python src/run_pipeline.py
```

## How ELT process works
- ingestion (manually each file)
- run pipeline (orchestrator, db-based tasks)
    - validation (save as parquet files, physically)
    - load to stage
    - transformation (stage to core)
    - build mart layer 

## Tests
### PyTest - unit and integration tests
```bash
set PYTHONPATH=. && pytest tests/test_database_connection.py
set PYTHONPATH=. && pytest tests/db_connection/test_database_connection.py
set PYTHONPATH=. && pytest tests/file_parser_tests.py
set PYTHONPATH=. && pytest tests/test_config_env.py
```

## YAML
```bash
pip install yamllint
yamllint your_file.yml
```

# Evaluation plans
## TODO list
- Source files to add
    - Arnona clients
- Source files to add in far future 
    - Education platform phones data
- source files enhancement 
    - add to Welfate patients data about Telem le herum
        - ask Irina
        - update programm
    - add result-file with columns: `citizen_id`, `is_lonely` for klita, welfare
    to provide calls' result from all departments
- new approaches 
    - how to add information about : is called by another unit (revaha, klita)?
    - phone prioritization: duplicates, mark as not relevant
    - phone from hamal: option to add telephone in HAMAL app
    - list of addresses with prioritization (as phones)
- improve validation:
    - for BOOL columns add check for null values. null values = false value.
    - add notification about null values treated as false for user
- improve sql:
    - in `run_ddl_scripts.py` - hardcoded drop view. need to solve this
- onboarding:
    - add data lineage
    - add column meanings description
