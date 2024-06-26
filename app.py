from flask import Flask, render_template, jsonify
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

# Konfiguration der SQLite-Datenbank
db_path = os.path.join(os.path.dirname(__file__), 'data', 'radio_playlist.db')
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Tracks(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.String, unique=True)
    title = db.Column(db.String, nullable=True)
    movement = db.Column(db.String, nullable=True)
    composer = db.Column(db.String, nullable=True)
    full_title = db.Column(db.String, nullable=True)
    image_link = db.Column(db.String, nullable=True)
    catalog_number = db.Column(db.String, nullable=True)
    conductor = db.Column(db.String, nullable=True)
    orchestra = db.Column(db.String, nullable=True)
    solist = db.Column(db.String, nullable=True)
    album = db.Column(db.String, nullable=True)
    ensemble = db.Column(db.String, nullable=True)
    ean = db.Column(db.String, nullable=True)
    choir = db.Column(db.String, nullable=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/data')
def data():
    tracks = Tracks.query.all()
    track_list = [{
        'timestamp': track.timestamp,
        'title': track.title,
        'movement': track.movement,
        'composer': track.composer,
        'full_title': track.full_title,
        'image_link': track.image_link,
        'catalog_number': track.catalog_number,
        'conductor': track.conductor,
        'orchestra': track.orchestra,
        'solist': track.solist,
        'album': track.album,
        'ensemble': track.ensemble,
        'ean': track.ean,
        'choir': track.choir
    } for track in tracks]
    return jsonify({"data": track_list})

if __name__ == '__main__':
    # Sicherstellen, dass das data-Verzeichnis existiert
    os.makedirs(os.path.join(os.path.dirname(__file__), 'data'), exist_ok=True)

    # Initialisieren der Datenbank
    with app.app_context():
        db.create_all()

    app.run(debug=True)
