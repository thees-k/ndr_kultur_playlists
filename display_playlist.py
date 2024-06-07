import sqlite3
import os


def display_data(conn):
    cursor = conn.execute('''
    SELECT t.timestamp, t.title, t.movement, t.composer, t.full_title, t.image_link, t.album, t.catalog_number,
           p.role, p.name
    FROM Tracks t
    LEFT JOIN Performers p ON t.id = p.track_id
    ORDER BY t.timestamp
    ''')

    current_timestamp = None
    for row in cursor.fetchall():
        timestamp, title, movement, composer, full_title, image_link, album, catalog_number, role, name = row
        if timestamp != current_timestamp:
            if current_timestamp is not None:
                print()  # Leerzeile zwischen verschiedenen Tracks
            print(f"Uhrzeit: {timestamp}")
            print(f"Werk: {title}")
            print(f"Satzbezeichnung: {movement}")
            print(f"Komponist: {composer}")
            print(f"Voller Titel: {full_title}")
            print(f"Bild-Link: {image_link}")
            print(f"Album: {album}")
            print(f"Bestellnummer: {catalog_number}")
            current_timestamp = timestamp
        if role and name:
            print(f"{role}: {name}")


def main():
    # Pfad zur SQLite-Datenbank im .data-Verzeichnis
    db_path = os.path.join('.data', 'radio_playlist.db')

    # Erstelle eine Verbindung zur SQLite-Datenbank
    conn = sqlite3.connect(db_path)

    # Daten aus der Datenbank abrufen und auf der Konsole ausgeben
    display_data(conn)

    conn.close()


if __name__ == '__main__':
    main()
