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
- step 1 - after run commands, check the DB status
```bash
python src/ingest.py --file-path data/land/av_bait_2025-06_v-01.xlsx
python src/ingest.py --file-path data/land/welfare_patients_2025-06_v-01.xlsx
python src/ingest.py --file-path data/land/new_immigrants_2024-12_v-01.xlsx
python src/ingest.py --file-path data/land/meser_2025-06_v-01.xlsx
python src/ingest.py --file-path data/land/hazramim_2025-05_v-01.xlsx
python src/ingest.py --file-path data/land/breath_troubles_2025-06_v-01.xlsx
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
```

## YAML
```bash
pip install yamllint
yamllint your_file.yml
```

# Evaluation plans
## TODO list
- Source files to add
    - Hamal Results (from Hamal App)
    - Arnona clients
- Source files to add in far future 
    - Education platform phones data
- source files enhancement 
    - add to Welfate patients data about Telem le herum
