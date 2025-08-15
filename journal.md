### 8/13/2025
Created this VM.  Started the data migration by zstd compressing the CSV files on local machine and scp-ing them over.  
Created stg schema in psql - CREATE SCHEMA IF NOT EXISTS stg;

Used following commands to stage the CSVs, format A = NCAA Trackman data, B = MLB_All_Time, C = Statcast
python3 make_stage_sql.py ~/uploads/Full_College_TM_2023.csv pitches_fmt_a | psql -U micro -d baseball -h localhost
python3 make_stage_sql.py ~/uploads/MLB_ALL_TIME.csv pitches_fmt_b | psql -U micro -d baseball -h localhost
python3 make_stage_sql.py ~/uploads/Statcast_2024.csv pitches_fmt_c | psql -U micro -d baseball -h localhost

This actually copied the data from CSV to staging:
\timing
SET synchronous_commit = off;
SET maintenance_work_mem = '256MB';

-- Format A (the two matching files)
\copy stg.pitches_fmt_a FROM '/home/mikerabayda/uploads/Full_College_TM_2023.csv' CSV HEADER
\copy stg.pitches_fmt_a FROM '/home/mikerabayda/uploads/Full_College_TM_2024.csv' CSV HEADER

-- Format B
\copy stg.pitches_fmt_b FROM '/home/mikerabayda/uploads/MLB_ALL_TIME.csv' CSV HEADER

-- Format C
\copy stg.pitches_fmt_c FROM '/home/mikerabayda/uploads/Statcast_2024.csv' CSV HEADER

-- Quick sanity
SELECT 'A' src, COUNT(*) FROM stg.pitches_fmt_a
UNION ALL SELECT 'B', COUNT(*) FROM stg.pitches_fmt_b
UNION ALL SELECT 'C', COUNT(*) FROM stg.pitches_fmt_c;
\timing
SET synchronous_commit = off;
SET maintenance_work_mem = '256MB';

-- Format A (the two matching files)
\copy stg.pitches_fmt_a FROM '/home/mikerabayda/uploads/Full_College_TM_2023.csv' CSV HEADER
\copy stg.pitches_fmt_a FROM '/home/mikerabayda/uploads/Full_College_TM_2024.csv' CSV HEADER

-- Format B
\copy stg.pitches_fmt_b FROM '/home/mikerabayda/uploads/MLB_ALL_TIME.csv' CSV HEADER

-- Format C
\copy stg.pitches_fmt_c FROM '/home/mikerabayda/uploads/Statcast_2024.csv' CSV HEADER

Then I created a create table file for format A to start with since I know the Trackman data typing the best. Then I created a load from staging to table for format A that creates a view of the data from staging, and then selects everything from that view to then insert into the final table that will be queried from.  My next step will be making similar tables for formats B and C, which are very similar but differ for a couple of variables, some are present, however some appear not to be present in both which is why I separated MLB_ALL_TIME and Statcast_2024. After that is finished, I should be all set to start with the classification of pitches, which will be a cool project to start with, as I'll do both MLB and College and compare the 2, especially on differences like curveball/slider/sweeper. 

### 8/14/2025 
Note from Johnny that Statcast only started reporting bat_speed and swing-length in 2024.

Made 2 .sql files, one to create the Statcast table (~/repos/BaseballAnalysisSite/create_table_Statcast.sql) and the other to load both of the ready staging tables into the table that was created in the first file(~/repos/BaseballAnalysisSite/load_pitches_from_staging_statcast.sql).  Ran both, so now all of the data can be found in psql and is queryable.

I'm considering creating the website just so I can get something put up, but I think I might just start with the classification and go from there.  Not sure how to do git projects that contain git projects so I'll need to learn how that works in practice.
