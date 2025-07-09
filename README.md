# ReadMe

## Flow
### Ingestion
```bash
python src/ingest.py --file-path data/land/av_bait/av_bait_2025-06_v-01.xlsx
```
## Tests
```bash
set PYTHONPATH=. && pytest tests/test_database_connection.py
set PYTHONPATH=. && pytest tests/db_connection/test_database_connection.py
```

