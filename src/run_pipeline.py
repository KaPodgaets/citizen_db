import subprocess
from sqlalchemy import create_engine, text

# Placeholder: configure your database URI
DATABASE_URI = 'postgresql://user:password@localhost:5432/citizen_db'
engine = create_engine(DATABASE_URI)

# Placeholder: meta table and file status
META_TABLE = 'meta_files'
VALIDATED_STATUS = 'validated'
PROCESSED_STATUS = 'processed'

with engine.connect() as conn:
    result = conn.execute(text(f"SELECT file_name FROM {META_TABLE} WHERE status = :status"), {'status': VALIDATED_STATUS})
    files = [row['file_name'] for row in result]

for file_name in files:
    print(f'Processing file: {file_name}')
    # Optionally pass file_name as argument to transform.py and publish.py if needed
    subprocess.run(['python', 'src/transform.py'])
    subprocess.run(['python', 'src/publish.py'])
    # Mark as processed
    with engine.begin() as conn:
        conn.execute(text(f"UPDATE {META_TABLE} SET status = :processed WHERE file_name = :file_name"), {'processed': PROCESSED_STATUS, 'file_name': file_name})

print('Pipeline run complete.')
