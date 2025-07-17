from src.utils.config import Settings

def test_env_files_parsing():
    settings = Settings()
    assert settings.database == 'citizen_db_project_test'