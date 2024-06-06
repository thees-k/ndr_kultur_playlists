import argparse
import requests
from bs4 import BeautifulSoup


def parse_html(content):
    soup = BeautifulSoup(content, 'lxml')
    programs = soup.find_all('li', class_='program')

    for program in programs:
        time = program.find('strong', class_='time').text.strip()
        print(f"Uhrzeit: {time}")

        title_element = program.find('h3')
        title_text = title_element.find('span', class_='title').text.strip()

        # Trennen des Werks und der Satzbezeichnung
        musical_piece, sep, movement = title_text.partition(' - ')
        if sep == '':
            musical_piece = title_text
            movement = ''

        print(f"Werk: {musical_piece}")
        print(f"Satzbezeichnung: {movement}")

        artist_element = title_element.find('span', class_='artist')

        if artist_element:
            artist_text = artist_element.text.strip()
            full_title = f"{title_text} - {artist_text}"
            print(f"Komponist: {artist_text}")
        else:
            full_title = title_text

        print(f"Titel: {title_text}")
        print(f"Voller Titel: {full_title}")

        # Extrahiere den Bild-Link
        thumbnail_element = program.find('a', class_='zoomimage')
        if thumbnail_element and 'href' in thumbnail_element.attrs:
            image_link = thumbnail_element['href']
            print(f"Bild-Link: {image_link}")

        details = program.find('div', class_='wrapper')
        detail_rows = details.find_all('div', class_='details_row')

        for detail in detail_rows:
            attribute = detail.find('div', class_='details_a').text.strip()
            value = detail.find('div', class_='details_b').text.strip()
            print(f"{attribute}: {value}")

        print()  # Leerzeile zur Trennung der Einträge


def main():
    parser = argparse.ArgumentParser(description='Parse an HTML file from a URL and extract radio program information.')
    parser.add_argument('url', help='URL of the HTML file')

    args = parser.parse_args()
    url = args.url

    # Senden einer HTTP-Anfrage an die URL
    response = requests.get(url)
    response.raise_for_status()  # Überprüfen, ob die Anfrage erfolgreich war

    html_content = response.text

    # Führe die Funktion mit dem Inhalt der heruntergeladenen HTML-Datei aus
    parse_html(html_content)


if __name__ == '__main__':
    main()
