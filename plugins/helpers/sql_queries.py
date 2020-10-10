class SqlQueries:

    songplay_table_insert = ("""
           (
            playid,
            start_time,
            userid,
            level,
            songid,
            artistid,
            sessionid,
            location,
            user_agent
        )
        SELECT
                md5(events.start_time) as playid,
                events.start_time, 
                events.userid, 
                events.level, 
                songs.song_id as songid, 
                songs.artist_id as artistid, 
                events.sessionid, 
                events.location, 
                events.useragent
                FROM (SELECT TIMESTAMP 'epoch' + ts/1000 * interval '1 second' AS start_time, *
            FROM staging_events
            WHERE page='NextSong') events
            LEFT JOIN staging_songs songs
            ON events.song = songs.title
                AND events.artist = songs.artist_name
                AND events.length = songs.duration
    """)

    user_table_insert = ("""
        (
            userid,
            first_name,
            last_name,
            gender,
            level
        )
        SELECT distinct userid, firstname as first_name, lastname as last_name, gender, level
        FROM staging_events
        WHERE page='NextSong'
    """)

    song_table_insert = ("""
         (
            songid,
            title,
            artistid,
            year,
            duration
        )
        SELECT distinct song_id as songid, title, artist_id as artistid, year, duration
        FROM staging_songs
    """)

    artist_table_insert = ("""
          (
            artistid,
            name,
            location,
            latitude,
            longitude    
        )
        SELECT distinct artist_id, artist_name as name, artist_location as location, artist_latitude as latitude,       artist_longitude as longitude
        FROM staging_songs
    """)

    time_table_insert = ("""
         (
            start_time,
            hour,
            day,
            week,
            month,
            year,
            weekday
        )
        SELECT start_time, extract(hour from start_time), extract(day from start_time), extract(week from start_time), 
               extract(month from start_time), extract(year from start_time), extract(dayofweek from start_time)
        FROM songplays
    """)