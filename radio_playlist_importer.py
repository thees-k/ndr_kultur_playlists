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
            catalog_number TEXT,
            conductor TEXT,
            orchestra TEXT,
            solist TEXT,
            album TEXT,
            ensemble TEXT,
            ean TEXT,
            choir TEXT
        )
        ''')


def insert_or_update_data(conn, track_data):
    with conn:
        conn.execute('''
        INSERT INTO Tracks (timestamp, title, movement, composer, full_title, image_link, catalog_number, conductor, orchestra, solist, album, ensemble, ean, choir)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(timestamp) DO UPDATE SET
            title=excluded.title,
            movement=excluded.movement,
            composer=excluded.composer,
            full_title=excluded.full_title,
            image_link=excluded.image_link,            
            catalog_number=excluded.catalog_number,
            conductor=excluded.conductor,
            orchestra=excluded.orchestra,            
            solist=excluded.solist,
            album=excluded.album,
            ensemble=excluded.ensemble,
            ean=excluded.ean,
            choir=excluded.choir
        ''', track_data)


def parse_html(content, date_str, detail_counts):
    tracks = []

    soup = BeautifulSoup(content, 'lxml')
    programs = soup.find_all('li', class_='program')

    for program in programs:
        time = program.find('strong', class_='time').text.strip()
        full_time = f"{date_str} {time}"
        print(f"Datum und Uhrzeit: {full_time}")

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

        print(f"Voller Titel: {full_title}")
        print(f"Komponist/Künstler: {artist_text}")
        print(f"Werk: {musical_piece}")
        print(f"Satzbezeichnung: {movement}")

        # Extrahiere den Bild-Link
        thumbnail_element = program.find('a', class_='zoomimage')
        image_link = 'https://www.ndr.de' + thumbnail_element['href'] if thumbnail_element and 'href' in thumbnail_element.attrs else None
        print(f"Image: {image_link}")

        track_data = {
            'timestamp': full_time,
            'title': musical_piece,
            'movement': movement,
            'composer': artist_text if artist_element else None,
            'full_title': full_title,
            'image_link': image_link,
            'catalog_number': None,
            'conductor': None,
            'orchestra': None,
            'solist': None,
            'album': None,
            'ensemble': None,
            'ean': None,
            'choir': None
        }

        details = program.find('div', class_='wrapper')
        detail_rows = details.find_all('div', class_='details_row')

        for detail in detail_rows:
            attribute = detail.find('div', class_='details_a').text.strip()

            attribute = replace_attribute_if_necessary(attribute)

            unique_values = fetch_unique_values(detail)
            if unique_values:
                value = '; '.join(unique_values)
            else:
                value = detail.find('div', class_='details_b').text.strip()

            print(f"{attribute}: {value}")

            if attribute in detail_counts:
                detail_counts[attribute] += 1
            else:
                detail_counts[attribute] = 1

            if attribute.startswith("Bestellnummer") or attribute.startswith("Best.-Nr."):
                track_data['catalog_number'] = value
            elif attribute == "Dirigent":
                track_data['conductor'] = value
            elif attribute == "Orchester":
                track_data['orchestra'] = value
            elif attribute == "Solist":
                track_data['solist'] = value
            elif attribute == "Album":
                track_data['album'] = value
            elif attribute == "Ensemble":
                track_data['ensemble'] = value
            elif attribute == "EAN":
                track_data['ean'] = value
            elif attribute == "Chor":
                track_data['choir'] = value

        tracks.append(track_data)
        print()

    return tracks


def replace_attribute_if_necessary(attribute):
    if attribute == "Solisten":
        attribute = "Solist"
    if attribute == "Ensembles":
        attribute = "Ensemble"
    if attribute == "Dirigenten":
        attribute = "Dirigent"
    if attribute == "Chöre":
        attribute = "Chor"
    return attribute


def fetch_unique_values(detail):
    unique_values = []
    seen_values = set()
    for value in detail.find('div', class_='details_b').find_all('span'):
        value_text = value.text.strip()
        if value_text not in seen_values:
            unique_values.append(value_text)
            seen_values.add(value_text)
    return unique_values


def fetch_and_parse(url, date_str, detail_counts):
    response = requests.get(url)
    response.raise_for_status()  # Überprüfen, ob die Anfrage erfolgreich war
    return parse_html(response.text, date_str, detail_counts)


def main():
    detail_counts = {}

    base_url = 'https://www.ndr.de/kultur/programm/titelliste1212.html'
    end_date = datetime.now()
    start_date = end_date - timedelta(days=6)

    # Sicherstellen, dass das data-Verzeichnis existiert
    os.makedirs('data', exist_ok=True)
    db_path = os.path.join('data', 'radio_playlist.db')

    # Erstelle eine Verbindung zur SQLite-Datenbank
    conn = sqlite3.connect(db_path)
    create_tables(conn)

    # Iteriere über die letzten 60 Tage, jede Stunde
    current_date = start_date
    while current_date <= end_date:
        for hour in range(6, 24):  # Stunden von 6 bis 23 Uhr importieren
            date_str = current_date.strftime('%Y-%m-%d')
            url = f'{base_url}?date={date_str}&hour={hour}'
            # print(f'Fetching: {url}')  # Fortschritt ausgeben
            tracks = fetch_and_parse(url, date_str, detail_counts)
            for track_data in tracks:
                insert_or_update_data(conn, (
                    track_data['timestamp'],
                    track_data['title'],
                    track_data['movement'],
                    track_data['composer'],
                    track_data['full_title'],
                    track_data['image_link'],
                    track_data['catalog_number'],
                    track_data['conductor'],
                    track_data['orchestra'],
                    track_data['solist'],
                    track_data['album'],
                    track_data['ensemble'],
                    track_data['ean'],
                    track_data['choir']
                ))

        current_date += timedelta(days=1)
    conn.close()

    print()
    print("Detail-Häufigkeiten:")
    sorted_detail_counts = sorted(detail_counts.items(), key=lambda item: item[1], reverse=True)
    for word, count in sorted_detail_counts:
        print(f'{word}: {count}')



if __name__ == '__main__':
    main()
