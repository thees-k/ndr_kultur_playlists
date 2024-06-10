import sqlite3
import os
from track_formatter import format_track_info


def display_all_tracks(conn):
    query = 'SELECT * FROM Tracks ORDER BY timestamp ASC'
    cursor = conn.execute(query)
    tracks = cursor.fetchall()
    for track in tracks:
        timestamp = track[1]
        print(f"{timestamp} {format_track_info(track)}")


def main():
    db_path = os.path.join('.data', 'radio_playlist.db')

    with sqlite3.connect(db_path) as conn:
        display_all_tracks(conn)


if __name__ == '__main__':
    main()
