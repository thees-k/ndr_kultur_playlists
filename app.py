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
