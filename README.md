# ReadMe

## Flow
- ingestion (manually each file)
- run pipeline (orchestrator, db-based tasks)
    - validation (save as parquet files, physically)
    - load to stage
    - transformation (stage to core)
    - build mart layer 

## Tests
### Workflow tests
- step 0 - backfill fake_ids if exist
```bash
python src/backfill_citizen_fid.py --filepath data/snapshots/fake_id-2025-06-15.xlsx
```
- step 1 - after run commands, check the DB status
```bash
python src/ingest.py --file-path data/land/av_bait_2025-06_v-01.xlsx
python src/ingest.py --file-path data/land/welfare_patients_2025-06_v-01.xlsx
python src/ingest.py --file-path data/land/new_immigrants_2024-12_v-01.xlsx
python src/ingest.py --file-path data/land/meser_2025-06_v-01.xlsx
python src/ingest.py --file-path data/land/hazramim_2025-05_v-01.xlsx
python src/ingest.py --file-path data/land/breath_troubles_2025-06_v-01.xlsx
python src/ingest.py --file-path data/land/hamal_2025-07_v-01.xlsx
python src/run_pipeline.py
```
-step 2 - after run commands, check the DB status
```bash
python src/ingest.py --file-path data/land/av_bait_2025-07_v-01.xlsx
python src/ingest.py --file-path data/land/welfare_patients_2025-07_v-01.xlsx
python src/run_pipeline.py
```

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
- new approaches 
    - how to add information about : is called by another unit (revaha, klita)?
    - phone prioritization: duplicates, mark as not relevant
    - phone from hamal: option to add telephone in HAMAL app
    - list of addresses with prioritization (as phones)
     
