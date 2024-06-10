import sqlite3
import os


def print_track_info(track):
    (track_id, timestamp, title, movement, composer, full_title, image_link,
     catalog_number, conductor, orchestra, solist, album, ensemble, ean, choir) = track

    title = format_field(title)
    movement = format_field(movement)
    composer = format_field(composer)
    catalog_number = format_field(catalog_number)
    conductor = format_field(conductor)
    orchestra = format_field(orchestra)
    solist = format_field(solist)
    album = format_field(album)
    ensemble = format_field(ensemble)
    ean = format_field(ean)
    choir = format_field(choir)

    composer_info = f"{composer}:" if composer else ""
    piece_and_movement = ", ".join(filter(None, [title, movement]))
    performers = ", ".join(filter(None, [solist, choir, ensemble, orchestra, conductor]))
    performers = f"({performers})" if performers else ""
    album_info = "/".join(filter(None, [album, ean, catalog_number]))
    album_info = f"[{album_info}]" if album_info else ""
    track_info = " ".join(filter(None, [composer_info, piece_and_movement, performers, album_info]))

    print(f"{timestamp}: {track_info}")


def format_field(field):
    return field if field and field != '-' else ""


def display_all_tracks(conn):
    query = 'SELECT * FROM Tracks ORDER BY timestamp ASC'
    cursor = conn.execute(query)
    tracks = cursor.fetchall()
    for track in tracks:
        print_track_info(track)


def main():
    db_path = os.path.join('.data', 'radio_playlist.db')

    with sqlite3.connect(db_path) as conn:
        display_all_tracks(conn)


if __name__ == '__main__':
    main()
