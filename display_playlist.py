import sqlite3
import os


def display_all_tracks(conn):
    cursor = conn.execute('''
    SELECT timestamp, title, movement, composer, full_title, image_link, album, catalog_number, orchestra, conductor, solist, choir
    FROM Tracks
    ORDER BY timestamp ASC
    ''')

    tracks = cursor.fetchall()

    print("\nAlle gespeicherten Tracks\n" + "-" * 25)
    for track in tracks:
        timestamp, title, movement, composer, full_title, image_link, album, catalog_number, orchestra, conductor, solist, choir = track
        print(f"Zeit: {timestamp}")
        print(f"Titel: {title}")
        print(f"Satzbezeichnung: {movement}")
        print(f"Komponist: {composer}")
        print(f"Voller Titel: {full_title}")
        print(f"Bildlink: {image_link}")
        print(f"Album: {album}")
        print(f"Bestellnummer: {catalog_number}")
        print(f"Orchester/Ensemble: {orchestra}")
        print(f"Dirigent: {conductor}")
        print(f"Solist: {solist}")
        print(f"Chor: {choir}")
        print("\n" + "-" * 25)


def main():
    # Pfad zur SQLite-Datenbank im .data-Verzeichnis
    db_path = os.path.join('.data', 'radio_playlist.db')

    # Erstelle eine Verbindung zur SQLite-Datenbank
    conn = sqlite3.connect(db_path)

    display_all_tracks(conn)

    conn.close()


if __name__ == '__main__':
    main()
