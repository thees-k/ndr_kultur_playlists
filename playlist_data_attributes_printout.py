import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta



def parse_html(content, date_str, detail_counts):
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
        image_link = thumbnail_element['href'] if thumbnail_element and 'href' in thumbnail_element.attrs else None

        details = program.find('div', class_='wrapper')
        detail_rows = details.find_all('div', class_='details_row')

        for detail in detail_rows:
            attribute = detail.find('div', class_='details_a').text.strip()

            values = [value.text.strip() for value in detail.find('div', class_='details_b').find_all('span')]
            if values:
                value = '; '.join(values)
            else:
                value = detail.find('div', class_='details_b').text.strip()

            print(f"{attribute}: {value}")

            if attribute in detail_counts:
                detail_counts[attribute] += 1
            else:
                detail_counts[attribute] = 1

        print()



def fetch_and_parse(url, date_str, detail_counts):
    response = requests.get(url)
    response.raise_for_status()  # Überprüfen, ob die Anfrage erfolgreich war
    parse_html(response.text, date_str, detail_counts)


def main():
    detail_counts = {}

    base_url = 'https://www.ndr.de/kultur/programm/titelliste1212.html'
    end_date = datetime.now()
    start_date = end_date - timedelta(days=60)

    # Iteriere über die letzten 60 Tage, jede Stunde
    current_date = start_date
    while current_date <= end_date:
        for hour in range(6, 24):  # Stunden von 6 bis 23 Uhr importieren
            date_str = current_date.strftime('%Y-%m-%d')
            url = f'{base_url}?date={date_str}&hour={hour}'
            # print(f'Fetching: {url}')  # Fortschritt ausgeben
            fetch_and_parse(url, date_str, detail_counts)
        current_date += timedelta(days=1)

    print()
    print("DETAIL-HÄUFIGKEITEN:")
    sorted_detail_counts = sorted(detail_counts.items(), key=lambda item: item[1], reverse=True)
    # Ergebnis anzeigen
    for word, count in sorted_detail_counts:
        print(f'{word}: {count}')


if __name__ == '__main__':
    main()
