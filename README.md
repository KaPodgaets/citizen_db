# ReadMe

## Flow
### Ingestion
```bash
python src/ingest.py --file-path data/land/av_bait_2025-07_v-01.xlsx
```
### Validation
```bash
python src/validate.py --file-id 1
```

### Run pipeline
```
python src/run_pipeline.py
```
## Tests
```bash
set PYTHONPATH=. && pytest tests/test_database_connection.py
set PYTHONPATH=. && pytest tests/db_connection/test_database_connection.py
```

## YAML
```bash
pip install yamllint
yamllint your_file.yml
```