import sqlite3
import os

from track_formatter import format_track_info


def get_top_n_tracks(conn, n=10):
    cursor = conn.execute('''
    SELECT *, COUNT(id) as count
    FROM Tracks
    GROUP BY full_title, title, movement, composer, album, catalog_number, conductor, orchestra, solist, ensemble, ean, choir
    ORDER BY count DESC
    LIMIT ?
    ''', (n,))
    return cursor.fetchall()


def get_top_n_composers(conn, n=10):
    cursor = conn.execute('''
    SELECT composer, COUNT(*) as count
    FROM Tracks
    WHERE composer IS NOT NULL
    GROUP BY composer
    ORDER BY count DESC
    LIMIT ?
    ''', (n,))
    return cursor.fetchall()


def get_top_n_orchestras(conn, n=10):
    cursor = conn.execute('''
    SELECT orchestra, COUNT(*) as count
    FROM Tracks
    WHERE orchestra IS NOT NULL
    GROUP BY orchestra
    ORDER BY count DESC
    LIMIT ?
    ''', (n,))
    return cursor.fetchall()


def get_top_n_conductors(conn, n=10):
    cursor = conn.execute('''
    SELECT conductor, COUNT(*) as count
    FROM Tracks
    WHERE conductor IS NOT NULL
    GROUP BY conductor
    ORDER BY count DESC
    LIMIT ?
    ''', (n,))
    return cursor.fetchall()


def get_top_n_albums(conn, n=10):
    cursor = conn.execute('''
    SELECT album, COUNT(*) as count
    FROM Tracks
    WHERE album IS NOT NULL
    GROUP BY album
    ORDER BY count DESC
    LIMIT ?
    ''', (n,))
    return cursor.fetchall()


def get_top_n_composer_piece_combinations(conn, n=10):
    cursor = conn.execute('''
    SELECT composer, title, COUNT(*) as count
    FROM Tracks
    WHERE composer IS NOT NULL AND title IS NOT NULL
    GROUP BY composer, title
    ORDER BY count DESC
    LIMIT ?
    ''', (n,))
    return cursor.fetchall()


def get_top_n_orchestra_conductor_combinations(conn, n=10):
    cursor = conn.execute('''
    SELECT orchestra, conductor, COUNT(*) as count
    FROM Tracks
    WHERE orchestra IS NOT NULL AND conductor IS NOT NULL
    GROUP BY orchestra, conductor
    ORDER BY count DESC
    LIMIT ?
    ''', (n,))
    return cursor.fetchall()


def get_top_n_solists(conn, n=10):
    cursor = conn.execute('''
    SELECT solist, COUNT(*) as count
    FROM Tracks
    WHERE solist IS NOT NULL
    GROUP BY solist
    ORDER BY count DESC
    LIMIT ?
    ''', (n,))
    return cursor.fetchall()


def get_top_n_catalog_numbers(conn, n=10):
    cursor = conn.execute('''
    SELECT catalog_number, COUNT(*) as count
    FROM Tracks
    WHERE catalog_number IS NOT NULL
    GROUP BY catalog_number
    ORDER BY count DESC
    LIMIT ?
    ''', (n,))
    return cursor.fetchall()


def get_top_n_eans(conn, n=10):
    cursor = conn.execute('''
    SELECT ean, COUNT(*) as count
    FROM Tracks
    WHERE ean IS NOT NULL
    GROUP BY ean
    ORDER BY count DESC
    LIMIT ?
    ''', (n,))
    return cursor.fetchall()


def display_results(results, title):
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


def main():
    # Pfad zur SQLite-Datenbank im .data-Verzeichnis
    db_path = os.path.join('.data', 'radio_playlist.db')

    # Erstelle eine Verbindung zur SQLite-Datenbank
    conn = sqlite3.connect(db_path)

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
            results = get_top_n_tracks(conn)
            display_results(results, "Die zehn am häufigsten gespielten Titel")
        elif choice == '2':
            results = get_top_n_composers(conn)
            display_results(results, "Die zehn am häufigsten gespielten Komponisten")
        elif choice == '3':
            results = get_top_n_orchestras(conn)
            display_results(results, "Die zehn am häufigsten gespielten Orchester")
        elif choice == '4':
            results = get_top_n_conductors(conn)
            display_results(results, "Die zehn am häufigsten gespielten Dirigenten")
        elif choice == '5':
            results = get_top_n_albums(conn)
            display_results(results, "Die zehn am häufigsten gespielten Alben")
        elif choice == '6':
            results = get_top_n_composer_piece_combinations(conn)
            display_results(results, "Die zehn häufigsten Kombinationen aus Komponist und Werk")
        elif choice == '7':
            results = get_top_n_orchestra_conductor_combinations(conn)
            display_results(results, "Die zehn häufigsten Kombinationen aus Orchester und Dirigent")
        elif choice == '8':
            results = get_top_n_solists(conn)
            display_results(results, "Die zehn am häufigsten gespielten Solisten")
        elif choice == '9':
            results = get_top_n_catalog_numbers(conn)
            display_results(results, "Die zehn am häufigsten gespielten Bestellnummern")
        elif choice == '10':
            results = get_top_n_eans(conn)
            display_results(results, "Die zehn am häufigsten gespielten Alben gemäß ihrer EAN")
        elif choice == '0':
            break
        else:
            print("Ungültige Wahl. Bitte versuchen Sie es erneut.")

    conn.close()


if __name__ == '__main__':
    main()
