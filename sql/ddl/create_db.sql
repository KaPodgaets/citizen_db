use master;

if not exists (select * from sys.databases where name = 'citizen_db_project_test')
begin
    create database citizen_db_project_test;
end
