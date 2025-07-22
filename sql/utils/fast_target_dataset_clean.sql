delete from stage.hamal
delete from core.hamal

delete
  FROM [citizen_db_project_test].[meta].[dataset_version]
  where dataset = 'hamal'

  delete
  FROM [citizen_db_project_test].[meta].[transform_log]
where dataset = 'hamal'

delete
FROM [citizen_db_project_test].[meta].[ingestion_log]
where dataset = 'hamal'