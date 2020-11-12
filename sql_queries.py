import configparser


# CONFIG
config = configparser.ConfigParser()
config.read('dwh.cfg')

# DROP TABLES

staging_events_table_drop = """ DROP TABLE IF EXISTS staging_events"""
staging_songs_table_drop =  """ DROP TABLE IF EXISTS staging_songs"""
songplay_table_drop =  """ DROP TABLE IF EXISTS song_plays"""
user_table_drop =  """ DROP TABLE IF EXISTS users"""
song_table_drop =  """ DROP TABLE IF EXISTS songs"""
artist_table_drop =  """ DROP TABLE IF EXISTS artists"""
time_table_drop = """ DROP TABLE IF EXISTS time"""

# CREATE TABLES

staging_events_table_create= ("""CREATE TABLE IF NOT EXISTS staging_events (
artist text, auth text, firstName text, gender text, ItemInSession int,
lastName text, length float8, level text, location text, method text,
page text, registration text, sessionId int, song text, status int,
ts bigint, userAgent text, userId int)
""")

staging_songs_table_create = ("""CREATE TABLE IF NOT EXISTS staging_songs (
song_id text PRIMARY KEY, artist_id text, artist_latitude float,
artist_longitude float, artist_location text, artist_name text,
duration float, num_songs int, title text, year int)
""")

songplay_table_create = (""" CREATE TABLE IF NOT EXISTS song_plays 
(songplay_id int IDENTITY(0,1) PRIMARY KEY, start_time varchar NOT NULL, user_id int NOT NULL, 
level varchar, song_id int, artist_id varchar,
session_id int, location varchar, user_agent varchar)
""")

user_table_create = (""" CREATE TABLE IF NOT EXISTS users 
(user_id int PRIMARY KEY, first_name varchar, last_name varchar,
gender varchar, level varchar)
""")

song_table_create = (""" CREATE TABLE IF NOT EXISTS songs 
(song_id varchar PRIMARY KEY, title varchar, artist_id varchar 
NOT NULL, year int, duration decimal)
""")

artist_table_create = (""" CREATE TABLE IF NOT EXISTS artists 
(artist_id varchar PRIMARY KEY, name varchar, location varchar,  
latitude decimal, longitude decimal)
""")

time_table_create = (""" CREATE TABLE IF NOT EXISTS time 
(start_time varchar PRIMARY KEY, hour varchar, day varchar, 
week varchar, month varchar, year int, weekday varchar)
""")

# STAGING TABLES

staging_events_copy = ("""COPY staging_events
                    from '{}'
                    credentials 'aws_iam_role={}'
                    region 'us-west-2'
                    COMPUPDATE OFF 
                    JSON '{}'
""").format(config.get('S3','LOG_DATA'), 
            config.get('IAM_ROLE','ARN'),
            config.get('S3','LOG_JSONPATH'))



staging_songs_copy = ("""COPY staging_songs
                    from '{}'
                    credentials 'aws_iam_role={}'
                    region 'us-west-2'
                    COMPUPDATE OFF 
                    JSON 'auto' truncatecolumns
""").format(config.get('S3','SONG_DATA'), 
            config.get('IAM_ROLE','ARN'))

# FINAL TABLES

songplay_table_insert = (""" INSERT INTO song_plays (start_time, 
user_id, level, song_id, artist_id, session_id, location, user_agent)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
""")

user_table_insert = (""" INSERT INTO users (user_id, first_name,last_name, 
gender, level) VALUES (%s, %s, %s, %s, %s) 
ON CONFLICT(user_id)
DO UPDATE SET level = excluded.level
""")

song_table_insert = (""" INSERT INTO songs (song_id, title, artist_id, year,  
duration) VALUES (%s, %s, %s, %s,%s)
ON CONFLICT(title, year, duration) DO NOTHING
""")

artist_table_insert = (""" INSERT INTO artists (artist_id, name, location, 
latitude, longitude) VALUES (%s, %s, %s, %s,%s)
ON CONFLICT(name, location, latitude, longitude) DO NOTHING
""")


time_table_insert = (""" INSERT INTO time (start_time, hour, day, week, 
month, year, weekday) VALUES (%s, %s, %s, %s, %s, %s, %s)
ON CONFLICT(start_time, hour, day, week, month, year, weekday) DO NOTHING
""")

# QUERY LISTS

create_table_queries = [staging_events_table_create, staging_songs_table_create, songplay_table_create, user_table_create, song_table_create, artist_table_create, time_table_create]
drop_table_queries = [staging_events_table_drop, staging_songs_table_drop, songplay_table_drop, user_table_drop, song_table_drop, artist_table_drop, time_table_drop]
copy_table_queries = [staging_events_copy, staging_songs_copy]
insert_table_queries = [songplay_table_insert, user_table_insert, song_table_insert, artist_table_insert, time_table_insert]
