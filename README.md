# NDR Kultur Playlist Analyzer

## Overview

This project allows for the analysis of the tracks played by the radio station NDR Kultur. The application collects playlists from the last two months, stores them in a SQLite database, and provides a web interface to browse and analyze the stored data.

## Features

- **Playlist Collection**: Automatically collect and store playlists from the NDR Kultur radio station for the past two months.
- **Database**: Store the collected data in a SQLite database.
- **Web Interface**: Searchable table of stored tracks.
- **Analysis Functions**: Display the top ten most frequently played tracks, composers, orchestras, conductors, albums, soloists, catalog numbers, and combinations.

## Installation

### Requirements

- Python 3.x
- Flask
- Flask-SQLAlchemy
- SQLite

### Steps

1. **Clone the Repository**

   ```bash
   git clone https://github.com/yourusername/ndr_kultur_playlist_analyzer.git
   cd ndr_kultur_playlist_analyzer
   ```

2. **Create and Activate Virtual Environment**

   ```bash
   python -m venv venv
   source venv/bin/activate   # For Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Initialize Database**

   ```bash
   python radio_playlist_importer.py
   ```

   This will collect playlists from the last two months from NDR Kultur and store them in the SQLite database.

5. **Start the Web Application**

   ```bash
   python app.py
   ```

6. **Open the Website**

   Open a web browser and go to `http://127.0.0.1:5000` to use the web interface.

## Files and Directories

- `app.py`: Flask application that provides the web interface.
- `radio_playlist_importer.py`: Script for collecting and storing playlists in the SQLite database.
- `track_formatter.py`: Contains the method for formatting track information.
- `analyze_playlist.py`: Script for analyzing the stored playlists.
- `data/`: Directory containing the SQLite database.
- `templates/index.html`: HTML template for the web interface.
- `requirements.txt`: List of required Python packages.

## Usage

### Web Interface

The web interface allows browsing and analyzing the stored playlists. The table shows the stored tracks and allows filtering the results by various columns.

![Screenshot](/assets/images/screenshot.jpg)


### Analysis Script

The script `analyze_playlist.py` can also be run directly from the command line to analyze the stored playlists. It will first ask how many weeks back the playlists should be analyzed and then perform the desired analysis.

- The ten most frequently played tracks
- The ten most frequently played composers
- The ten most frequently played orchestras
- The ten most frequently played conductors
- The ten most frequently played albums
- The ten most frequently played soloists
- The ten most frequently played catalog numbers
- The ten most frequent combinations of composer and piece
- The ten most frequent combinations of orchestra and conductor


```bash
python analyze_playlist.py
```

## Contributions

Contributions to this project are welcome. Please open an issue to report bugs or suggest new features. Pull requests are also welcome.

## License

This project is licensed under the MIT License – see the [LICENSE](LICENSE) file for details.

### Third-Party Licenses

This project includes third-party libraries that are distributed under their own licenses:

- [Bootstrap](https://getbootstrap.com/) is licensed under the MIT License.
- [jQuery](https://jquery.com/) is licensed under the MIT License.
- [DataTables](https://datatables.net/) is licensed under the MIT License.
```

