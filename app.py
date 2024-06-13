from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

# Konfiguration der SQLite-Datenbank
db_path = os.path.join(os.path.dirname(__file__), '.data', 'radio_playlist.db')
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Tracks(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.String)
    title = db.Column(db.String)
    movement = db.Column(db.String)
    composer = db.Column(db.String)
    full_title = db.Column(db.String)
    image_link = db.Column(db.String)
    catalog_number = db.Column(db.String)
    conductor = db.Column(db.String)
    orchestra = db.Column(db.String)
    solist = db.Column(db.String)
    album = db.Column(db.String)
    ensemble = db.Column(db.String)
    ean = db.Column(db.String)
    choir = db.Column(db.String)


@app.route('/')
def index():
    tracks = Tracks.query.all()
    return render_template('index.html', tracks=tracks)


@app.route('/top_tracks')
def top_tracks():
    tracks = Tracks.query.all()
    sorted_tracks = sorted(tracks, key=lambda x: (x.timestamp, x.title))
    return render_template('analysis.html', title="Top 10 Tracks", tracks=sorted_tracks[:10])


@app.route('/top_composers')
def top_composers():
    composers = db.session.query(Tracks.composer, db.func.count(Tracks.id)).group_by(Tracks.composer).order_by(
        db.func.count(Tracks.id).desc()).limit(10).all()
    return render_template('analysis.html', title="Top 10 Composers", items=composers)


@app.route('/top_orchestras')
def top_orchestras():
    orchestras = db.session.query(Tracks.orchestra, db.func.count(Tracks.id)).group_by(Tracks.orchestra).order_by(
        db.func.count(Tracks.id).desc()).limit(10).all()
    return render_template('analysis.html', title="Top 10 Orchestras", items=orchestras)


@app.route('/top_conductors')
def top_conductors():
    conductors = db.session.query(Tracks.conductor, db.func.count(Tracks.id)).group_by(Tracks.conductor).order_by(
        db.func.count(Tracks.id).desc()).limit(10).all()
    return render_template('analysis.html', title="Top 10 Conductors", items=conductors)


@app.route('/top_albums')
def top_albums():
    albums = db.session.query(Tracks.album, db.func.count(Tracks.id)).group_by(Tracks.album).order_by(
        db.func.count(Tracks.id).desc()).limit(10).all()
    return render_template('analysis.html', title="Top 10 Albums", items=albums)


@app.route('/top_solists')
def top_solists():
    solists = db.session.query(Tracks.solist, db.func.count(Tracks.id)).group_by(Tracks.solist).order_by(
        db.func.count(Tracks.id).desc()).limit(10).all()
    return render_template('analysis.html', title="Top 10 Solists", items=solists)


@app.route('/top_catalog_numbers')
def top_catalog_numbers():
    catalog_numbers = db.session.query(Tracks.catalog_number, db.func.count(Tracks.id)).group_by(
        Tracks.catalog_number).order_by(db.func.count(Tracks.id).desc()).limit(10).all()
    return render_template('analysis.html', title="Top 10 Catalog Numbers", items=catalog_numbers)


@app.route('/top_eans')
def top_eans():
    eans = db.session.query(Tracks.ean, db.func.count(Tracks.id)).group_by(Tracks.ean).order_by(
        db.func.count(Tracks.id).desc()).limit(10).all()
    return render_template('analysis.html', title="Top 10 EANs", items=eans)


if __name__ == '__main__':
    # Sicherstellen, dass das .data-Verzeichnis existiert
    os.makedirs(os.path.join(os.path.dirname(__file__), '.data'), exist_ok=True)

    # Initialisieren der Datenbank
    with app.app_context():
        db.create_all()

        # Testdaten hinzufügen, wenn die Tabelle leer ist
        if Tracks.query.count() == 0:
            test_track = Tracks(
                timestamp='2024-06-13 12:00',
                title='Test Title',
                movement='Test Movement',
                composer='Test Composer',
                full_title='Test Full Title',
                image_link='http://example.com/image.jpg',
                catalog_number='12345',
                conductor='Test Conductor',
                orchestra='Test Orchestra',
                solist='Test Solist',
                album='Test Album',
                ensemble='Test Ensemble',
                ean='67890',
                choir='Test Choir'
            )
            db.session.add(test_track)
            db.session.commit()

    app.run(debug=True)
