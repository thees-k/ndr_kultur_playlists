import argparse
import requests
from bs4 import BeautifulSoup
import sqlite3


def create_tables(conn):
    with conn:
        conn.execute('''
        CREATE TABLE IF NOT EXISTS Tracks (
            id INTEGER PRIMARY KEY,
            timestamp TEXT UNIQUE,
            title TEXT,
            movement TEXT,
            composer TEXT,
            full_title TEXT,
            image_link TEXT,
            album TEXT,
            catalog_number TEXT
        )
        ''')
        conn.execute('''
        CREATE TABLE IF NOT EXISTS Performers (
            id INTEGER PRIMARY KEY,
            track_id INTEGER,
            role TEXT,
            name TEXT,
            FOREIGN KEY(track_id) REFERENCES Tracks(id)
        )
        ''')


def insert_or_update_data(conn, track_data, performers_data):
    with conn:
        cursor = conn.execute('''
        INSERT INTO Tracks (timestamp, title, movement, composer, full_title, image_link, album, catalog_number)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(timestamp) DO UPDATE SET
            title=excluded.title,
            movement=excluded.movement,
            composer=excluded.composer,
            full_title=excluded.full_title,
            image_link=excluded.image_link,
            album=excluded.album,
            catalog_number=excluded.catalog_number
        ''', track_data)
        track_id = cursor.lastrowid if cursor.lastrowid != 0 else \
        conn.execute('SELECT id FROM Tracks WHERE timestamp = ?', (track_data[0],)).fetchone()[0]

        # Delete existing performers for this track_id
        conn.execute('DELETE FROM Performers WHERE track_id = ?', (track_id,))

        for performer in performers_data:
            conn.execute('''
            INSERT INTO Performers (track_id, role, name)
            VALUES (?, ?, ?)
            ''', (track_id, performer['role'], performer['name']))


def parse_html(content):
    soup = BeautifulSoup(content, 'lxml')
    programs = soup.find_all('li', class_='program')

    tracks = []

    for program in programs:
        time = program.find('strong', class_='time').text.strip()

        title_element = program.find('h3')
        title_text = title_element.find('span', class_='title').text.strip()

        # Trennen des Werks und der Satzbezeichnung
        musical_piece, sep, movement = title_text.partition(' - ')
        if sep == '':
            musical_piece = title_text
            movement = ''

        artist_element = title_element.find('span', class_='artist')

        if artist_element:
            artist_text = artist_element.text.strip()
            full_title = f"{title_text} - {artist_text}"
        else:
            full_title = title_text

        # Extrahiere den Bild-Link
        thumbnail_element = program.find('a', class_='zoomimage')
        image_link = thumbnail_element['href'] if thumbnail_element and 'href' in thumbnail_element.attrs else None

        details = program.find('div', class_='wrapper')
        detail_rows = details.find_all('div', class_='details_row')

        track_data = (
        time, musical_piece, movement, artist_text if artist_element else None, full_title, image_link, None, None)
        performers_data = []

        for detail in detail_rows:
            attribute = detail.find('div', class_='details_a').text.strip()
            value = detail.find('div', class_='details_b').text.strip()

            if attribute == "Album":
                track_data = track_data[:6] + (value, track_data[7])
            elif attribute.startswith("Bestellnummer") or attribute.startswith("Best.-Nr."):
                track_data = track_data[:7] + (value,)
            else:
                performers_data.append({'role': attribute, 'name': value})

        tracks.append((track_data, performers_data))

    return tracks


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
    parser = argparse.ArgumentParser(description='Parse an HTML file from a URL and extract radio program information.')
    parser.add_argument('url', help='URL of the HTML file')

    args = parser.parse_args()
    url = args.url

    # Senden einer HTTP-Anfrage an die URL
    response = requests.get(url)
    response.raise_for_status()  # Überprüfen, ob die Anfrage erfolgreich war

    html_content = response.text

    # Erstelle eine Verbindung zur SQLite-Datenbank
    conn = sqlite3.connect('radio_playlist.db')
    create_tables(conn)

    # Parse HTML und speichere die Daten in der Datenbank
    tracks = parse_html(html_content)
    for track_data, performers_data in tracks:
        insert_or_update_data(conn, track_data, performers_data)

    # Daten aus der Datenbank abrufen und auf der Konsole ausgeben
    display_data(conn)

    conn.close()


if __name__ == '__main__':
    main()
