import sqlite3
import os
from datetime import datetime, timedelta
from track_formatter import format_track_info


def get_top_n_tracks(conn, start_date, n=10):
    cursor = conn.execute('''
    SELECT *, COUNT(id) as count
    FROM Tracks
    WHERE timestamp >= ?
    GROUP BY full_title, title, movement, composer, album, catalog_number, conductor, orchestra, solist, ensemble, ean, choir
    ORDER BY count DESC
    LIMIT ?
    ''', (start_date, n))
    return cursor.fetchall()


def get_top_n_composers(conn, start_date, n=10):
    cursor = conn.execute('''
    SELECT composer, COUNT(*) as count
    FROM Tracks
    WHERE composer IS NOT NULL AND timestamp >= ?
    GROUP BY composer
    ORDER BY count DESC
    LIMIT ?
    ''', (start_date, n))
    return cursor.fetchall()


def get_top_n_orchestras(conn, start_date, n=10):
    cursor = conn.execute('''
    SELECT orchestra, COUNT(*) as count
    FROM Tracks
    WHERE orchestra IS NOT NULL AND timestamp >= ?
    GROUP BY orchestra
    ORDER BY count DESC
    LIMIT ?
    ''', (start_date, n))
    return cursor.fetchall()


def get_top_n_conductors(conn, start_date, n=10):
    cursor = conn.execute('''
    SELECT conductor, COUNT(*) as count
    FROM Tracks
    WHERE conductor IS NOT NULL AND timestamp >= ?
    GROUP BY conductor
    ORDER BY count DESC
    LIMIT ?
    ''', (start_date, n))
    return cursor.fetchall()


def get_top_n_albums(conn, start_date, n=10):
    cursor = conn.execute('''
    SELECT album, COUNT(*) as count
    FROM Tracks
    WHERE album IS NOT NULL AND timestamp >= ?
    GROUP BY album
    ORDER BY count DESC
    LIMIT ?
    ''', (start_date, n))
    return cursor.fetchall()


def get_top_n_composer_piece_combinations(conn, start_date, n=10):
    cursor = conn.execute('''
    SELECT composer, title, COUNT(*) as count
    FROM Tracks
    WHERE composer IS NOT NULL AND title IS NOT NULL AND timestamp >= ?
    GROUP BY composer, title
    ORDER BY count DESC
    LIMIT ?
    ''', (start_date, n))
    return cursor.fetchall()


def get_top_n_orchestra_conductor_combinations(conn, start_date, n=10):
    cursor = conn.execute('''
    SELECT orchestra, conductor, COUNT(*) as count
    FROM Tracks
    WHERE orchestra IS NOT NULL AND conductor IS NOT NULL AND timestamp >= ?
    GROUP BY orchestra, conductor
    ORDER BY count DESC
    LIMIT ?
    ''', (start_date, n))
    return cursor.fetchall()


def get_top_n_solists(conn, start_date, n=10):
    cursor = conn.execute('''
    SELECT solist, COUNT(*) as count
    FROM Tracks
    WHERE solist IS NOT NULL AND timestamp >= ?
    GROUP BY solist
    ORDER BY count DESC
    LIMIT ?
    ''', (start_date, n))
    return cursor.fetchall()


def get_top_n_catalog_numbers(conn, start_date, n=10):
    cursor = conn.execute('''
    SELECT catalog_number, COUNT(*) as count
    FROM Tracks
    WHERE catalog_number IS NOT NULL AND timestamp >= ?
    GROUP BY catalog_number
    ORDER BY count DESC
    LIMIT ?
    ''', (start_date, n))
    return cursor.fetchall()


def get_top_n_eans(conn, start_date, n=10):
    cursor = conn.execute('''
    SELECT ean, COUNT(*) as count
    FROM Tracks
    WHERE ean IS NOT NULL AND timestamp >= ?
    GROUP BY ean
    ORDER BY count DESC
    LIMIT ?
    ''', (start_date, n))
    return cursor.fetchall()


def display_tracks_by_album(conn, album, start_date):
    cursor = conn.execute('''
    SELECT * FROM Tracks WHERE album = ? AND timestamp >= ?
    ''', (album, start_date))
    tracks = cursor.fetchall()
    displayed_tracks = set()
    for track in tracks:
        track_info = format_track_info(track)
        if track_info not in displayed_tracks:
            displayed_tracks.add(track_info)
            print(track_info)


def display_tracks_by_catalog_number(conn, catalog_number, start_date):
    cursor = conn.execute('''
    SELECT * FROM Tracks WHERE catalog_number = ? AND timestamp >= ?
    ''', (catalog_number, start_date))
    tracks = cursor.fetchall()
    displayed_tracks = set()
    for track in tracks:
        track_info = format_track_info(track)
        if track_info not in displayed_tracks:
            displayed_tracks.add(track_info)
            print(track_info)


def display_tracks_by_ean(conn, ean, start_date):
    cursor = conn.execute('''
    SELECT * FROM Tracks WHERE ean = ? AND timestamp >= ?
    ''', (ean, start_date))
    tracks = cursor.fetchall()
    displayed_tracks = set()
    for track in tracks:
        track_info = format_track_info(track)
        if track_info not in displayed_tracks:
            displayed_tracks.add(track_info)
            print(track_info)


def display_results(conn, results, title, option, start_date):
    print(f'\n{title}\n' + '-' * len(title))
    for i, result in enumerate(results, 1):
        if len(result) == 16:  # Normale Track-Daten
            (track_id, timestamp, title, movement, composer, full_title, image_link,
             catalog_number, conductor, orchestra, solist, album, ensemble, ean, choir, count) = result
            track = (track_id, timestamp, title, movement, composer, full_title, image_link, catalog_number, conductor, orchestra, solist, album, ensemble, ean, choir)
            print(f"{format_track_info(track)} - {count} Mal gespielt")
        elif len(result) == 3:  # Kombinationen
            entity1, entity2, count = result
            print(f"{i}. {entity1} & {entity2} - {count} Mal gespielt")
        elif len(result) == 2:  # Einzelne Einheiten (z.B. Komponisten, Orchester)
            name, count = result
            print(f"{i}. {name} - {count} Mal gespielt")

        # Zusätzliche Anzeige der zugehörigen Tracks für Option 5, 9 und 10
        if option == 5 and len(result) == 2:
            album = result[0]
            display_tracks_by_album(conn, album, start_date)
        elif option == 9 and len(result) == 2:
            catalog_number = result[0]
            display_tracks_by_catalog_number(conn, catalog_number, start_date)
        elif option == 10 and len(result) == 2:
            ean = result[0]
            display_tracks_by_ean(conn, ean, start_date)


def get_earliest_date(conn):
    cursor = conn.execute('''
    SELECT MIN(timestamp) FROM Tracks
    ''')
    earliest_date = cursor.fetchone()[0]
    return earliest_date


def main():
    db_path = os.path.join('.data', 'radio_playlist.db')

    with sqlite3.connect(db_path) as conn:
        earliest_date_str = get_earliest_date(conn)
        if earliest_date_str:
            earliest_date = datetime.strptime(earliest_date_str, '%Y-%m-%d %H:%M')
            max_weeks = (datetime.now() - earliest_date).days // 7
            print(f"Die gespeicherten Daten reichen bis zu {max_weeks} Wochen zurück.")
        else:
            print("Keine Daten in der Datenbank gefunden.")
            return

        weeks = int(input(f"Wieviele Wochen zurück sollen die Titellisten analysiert werden? (Max: {max_weeks}): "))
        if weeks > max_weeks:
            weeks = max_weeks

        start_date = datetime.now() - timedelta(weeks=weeks)
        start_date_str = start_date.strftime('%Y-%m-%d %H:%M')

        while True:
            print("\nWählen Sie eine Option:")
            print("1. Die zehn am häufigsten gespielten Titel sehen")
            print("2. Die zehn am häufigsten gespielten Komponisten sehen")
            print("3. Die zehn am häufigsten gespielten Orchester sehen")
            print("4. Die zehn am häufigsten gespielten Dirigenten sehen")
            print("5. Die zehn am häufigsten gespielten Alben sehen")
            print("6. Die zehn häufigsten Kombinationen aus Komponist und Werk sehen")
            print("7. Die zehn häufigsten Kombinationen aus Orchester und Dirigent sehen")
            print("8. Die zehn am häufigsten gespielten Solisten sehen")
            print("9. Die zehn am häufigsten gespielten Bestellnummern sehen")
            print("10. Die zehn am häufigsten gespielten Alben gemäß ihrer EAN")
            print("0. Beenden")

            choice = input("Ihre Wahl: ")

            if choice == '1':
                results = get_top_n_tracks(conn, start_date_str)
                display_results(conn, results, "Die zehn am häufigsten gespielten Titel", 1, start_date_str)
            elif choice == '2':
                results = get_top_n_composers(conn, start_date_str)
                display_results(conn, results, "Die zehn am häufigsten gespielten Komponisten", 2, start_date_str)
            elif choice == '3':
                results = get_top_n_orchestras(conn, start_date_str)
                display_results(conn, results, "Die zehn am häufigsten gespielten Orchester", 3, start_date_str)
            elif choice == '4':
                results = get_top_n_conductors(conn, start_date_str)
                display_results(conn, results, "Die zehn am häufigsten gespielten Dirigenten", 4, start_date_str)
            elif choice == '5':
                results = get_top_n_albums(conn, start_date_str)
                display_results(conn, results, "Die zehn am häufigsten gespielten Alben", 5, start_date_str)
            elif choice == '6':
                results = get_top_n_composer_piece_combinations(conn, start_date_str)
                display_results(conn, results, "Die zehn häufigsten Kombinationen aus Komponist und Werk", 6, start_date_str)
            elif choice == '7':
                results = get_top_n_orchestra_conductor_combinations(conn, start_date_str)
                display_results(conn, results, "Die zehn häufigsten Kombinationen aus Orchester und Dirigent", 7, start_date_str)
            elif choice == '8':
                results = get_top_n_solists(conn, start_date_str)
                display_results(conn, results, "Die zehn am häufigsten gespielten Solisten", 8, start_date_str)
            elif choice == '9':
                results = get_top_n_catalog_numbers(conn, start_date_str)
                display_results(conn, results, "Die zehn am häufigsten gespielten Bestellnummern", 9, start_date_str)
            elif choice == '10':
                results = get_top_n_eans(conn, start_date_str)
                display_results(conn, results, "Die zehn am häufigsten gespielten Alben gemäß ihrer EAN", 10, start_date_str)
            elif choice == '0':
                break
            else:
                print("Ungültige Wahl. Bitte versuchen Sie es erneut.")


if __name__ == '__main__':
    main()
