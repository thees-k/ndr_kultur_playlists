import sqlite3
import os


def get_top_n_tracks(conn, n=10):
    cursor = conn.execute('''
    SELECT t.full_title, t.title, t.movement, t.composer, t.album, t.catalog_number, 
           GROUP_CONCAT(p.role || ': ' || p.name, ', ') as performers, COUNT(*) as count
    FROM Tracks t
    LEFT JOIN Performers p ON t.id = p.track_id
    GROUP BY t.full_title, t.title, t.movement, t.composer, t.album, t.catalog_number, performers
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
    SELECT p.name, COUNT(*) as count
    FROM Performers p
    JOIN Tracks t ON p.track_id = t.id
    WHERE p.role = 'Orchester'
    GROUP BY p.name
    ORDER BY count DESC
    LIMIT ?
    ''', (n,))
    return cursor.fetchall()


def get_top_n_conductors(conn, n=10):
    cursor = conn.execute('''
    SELECT p.name, COUNT(*) as count
    FROM Performers p
    JOIN Tracks t ON p.track_id = t.id
    WHERE p.role = 'Dirigent'
    GROUP BY p.name
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


def display_results(results, title):
    print(f'\n{title}\n' + '-' * len(title))
    for i, result in enumerate(results, 1):
        if isinstance(result, tuple) and len(result) > 2:
            full_title, title, movement, composer, album, catalog_number, performers, count = result
            print(f"{i}. {full_title} - {count} Mal gespielt")
            print(f"   Werk: {title}")
            print(f"   Satzbezeichnung: {movement}")
            print(f"   Komponist: {composer}")
            print(f"   Album: {album}")
            print(f"   Bestellnummer: {catalog_number}")
            print(f"   Interpreten: {performers}")
        else:
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
        print("6. Beenden")

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
            break
        else:
            print("Ungültige Wahl. Bitte versuchen Sie es erneut.")

    conn.close()


if __name__ == '__main__':
    main()
