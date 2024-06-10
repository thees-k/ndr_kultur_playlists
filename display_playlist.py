import sqlite3
import os


def print_row(row):
    (
        id, timestamp, title, movement, composer, full_title, image_link,
        catalog_number, conductor, orchestra, solist, album, ensemble, ean, choir
    ) = row

    title = format(title)
    movement = format(movement)
    composer = format(composer)
    catalog_number = format(catalog_number)
    conductor = format(conductor)
    orchestra = format(orchestra)
    solist = format(solist)
    album = format(album)
    ensemble = format(ensemble)
    ean = format(ean)
    choir = format(choir)

    composer = "" if composer == "" else composer+ ":"
    piece_and_movement = ", ".join(format_list([title, movement]))
    performers = ", ".join(format_list([solist, choir, ensemble, orchestra, conductor]))
    performers = performers if performers == "" else "("+performers+")"
    album_info = "/".join(format_list([album, ean, catalog_number]))
    album_info = album_info if album_info == "" else "[" + album_info + "]"
    track_info = " ".join(format_list([composer, piece_and_movement, performers, album_info]))
    print(f"{timestamp}: {track_info}")


def format(str):
    if not str or str == '-':
        return ""
    return str


def format_list(list):
    result = []
    for s in list:
        if s:
            result.append(s)
    return result


def display_all_tracks(conn):
    cursor = conn.execute('SELECT * FROM Tracks ORDER BY timestamp ASC')
    results = cursor.fetchall()
    for row in results:
        print_row(row)


def main():
    # Pfad zur SQLite-Datenbank im .data-Verzeichnis
    db_path = os.path.join('.data', 'radio_playlist.db')

    # Erstelle eine Verbindung zur SQLite-Datenbank
    conn = sqlite3.connect(db_path)

    display_all_tracks(conn)

    conn.close()


if __name__ == '__main__':
    main()
