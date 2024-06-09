import sqlite3
import os


def display_all_tracks(conn):
    cursor = conn.execute('SELECT * FROM Tracks ORDER BY timestamp ASC')
    results = cursor.fetchall()

    for row in results:
        (
            id, timestamp, title, movement, composer, full_title, image_link,
            catalog_number, conductor, orchestra, solist, album, ensemble, ean, choir
        ) = row
        print(f"ID: {id}")
        print(f"Timestamp: {timestamp}")
        print(f"Title: {title}")
        print(f"Movement: {movement}")
        print(f"Composer: {composer}")
        print(f"Full Title: {full_title}")
        print(f"Image Link: {image_link}")
        print(f"Catalog Number: {catalog_number}")
        print(f"Conductor: {conductor}")
        print(f"Orchestra: {orchestra}")
        print(f"Solist: {solist}")
        print(f"Album: {album}")
        print(f"Ensemble: {ensemble}")
        print(f"EAN: {ean}")
        print(f"Choir: {choir}")
        print("-" * 20)


def main():
    # Pfad zur SQLite-Datenbank im .data-Verzeichnis
    db_path = os.path.join('.data', 'radio_playlist.db')

    # Erstelle eine Verbindung zur SQLite-Datenbank
    conn = sqlite3.connect(db_path)

    display_all_tracks(conn)

    conn.close()


if __name__ == '__main__':
    main()
