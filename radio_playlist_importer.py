import requests
from bs4 import BeautifulSoup
import sqlite3
import os
from datetime import datetime, timedelta


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
            catalog_number TEXT,
            orchestra TEXT,
            conductor TEXT,
            solist TEXT,
            choir TEXT
        )
        ''')


def insert_or_update_data(conn, track_data):
    with conn:
        conn.execute('''
        INSERT INTO Tracks (timestamp, title, movement, composer, full_title, image_link, album, catalog_number, orchestra, conductor, solist, choir)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(timestamp) DO UPDATE SET
            title=excluded.title,
            movement=excluded.movement,
            composer=excluded.composer,
            full_title=excluded.full_title,
            image_link=excluded.image_link,
            album=excluded.album,
            catalog_number=excluded.catalog_number,
            orchestra=excluded.orchestra,
            conductor=excluded.conductor,
            solist=excluded.solist,
            choir=excluded.choir
        ''', track_data)


def parse_html(content, date_str):
    soup = BeautifulSoup(content, 'lxml')
    programs = soup.find_all('li', class_='program')

    tracks = []

    for program in programs:
        time = program.find('strong', class_='time').text.strip()
        full_time = f"{date_str} {time}"

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

        track_data = {
            'timestamp': full_time,
            'title': musical_piece,
            'movement': movement,
            'composer': artist_text if artist_element else None,
            'full_title': full_title,
            'image_link': image_link,
            'album': None,
            'catalog_number': None,
            'orchestra': None,
            'conductor': None,
            'solist': None,
            'choir': None
        }

        for detail in detail_rows:
            attribute = detail.find('div', class_='details_a').text.strip()
            value = detail.find('div', class_='details_b').text.strip()

            if attribute == "Album":
                track_data['album'] = value
            elif attribute.startswith("Bestellnummer") or attribute.startswith("Best.-Nr."):
                track_data['catalog_number'] = value
            elif attribute in ["Orchester", "Ensemble"]:
                track_data['orchestra'] = value
            elif attribute == "Dirigent":
                track_data['conductor'] = value
            elif attribute == "Solist":
                track_data['solist'] = value
            elif attribute == "Chor":
                track_data['choir'] = value

        tracks.append(track_data)

    return tracks


def fetch_and_parse(url, date_str):
    response = requests.get(url)
    response.raise_for_status()  # Überprüfen, ob die Anfrage erfolgreich war
    return parse_html(response.text, date_str)


def main():
    base_url = 'https://www.ndr.de/kultur/programm/titelliste1212.html'
    end_date = datetime.now()
    start_date = end_date - timedelta(days=60)

    # Sicherstellen, dass das .data-Verzeichnis existiert
    os.makedirs('.data', exist_ok=True)
    db_path = os.path.join('.data', 'radio_playlist.db')

    # Erstelle eine Verbindung zur SQLite-Datenbank
    conn = sqlite3.connect(db_path)
    create_tables(conn)

    # Iteriere über die letzten 60 Tage, jede Stunde
    current_date = start_date
    while current_date <= end_date:
        for hour in range(6, 24):  # Stunden von 6 bis 23 Uhr importieren
            date_str = current_date.strftime('%Y-%m-%d')
            url = f'{base_url}?date={date_str}&hour={hour}'
            print(f'Fetching: {url}')  # Fortschritt ausgeben
            tracks = fetch_and_parse(url, date_str)
            for track_data in tracks:
                insert_or_update_data(conn, (
                    track_data['timestamp'],
                    track_data['title'],
                    track_data['movement'],
                    track_data['composer'],
                    track_data['full_title'],
                    track_data['image_link'],
                    track_data['album'],
                    track_data['catalog_number'],
                    track_data['orchestra'],
                    track_data['conductor'],
                    track_data['solist'],
                    track_data['choir']
                ))
        current_date += timedelta(days=1)

    conn.close()


if __name__ == '__main__':
    main()
