from flask import Flask, render_template, jsonify, abort, send_file
import requests
import os
import json
from dotenv import load_dotenv
from mcstats import *

load_dotenv()

app = Flask(__name__)
STATS_DIR = os.getenv('MINECRAFT_WORLD_PATH') + "/stats"

# Global cache for players and their stats
PLAYERS_CACHE = {}
STATS_CACHE = {}

# Constantes pour les images
HEADS_DIR = os.path.join('static', 'heads')
HEADS_URL = "https://mc-heads.net/head/{}/left"

def download_player_head(username):
    """Télécharge et sauvegarde la tête du joueur"""
    head_path = os.path.join(HEADS_DIR, f"{username}.png")
    if not os.path.exists(head_path):
        try:
            response = requests.get(HEADS_URL.format(username))
            if response.status_code == 200:
                os.makedirs(HEADS_DIR, exist_ok=True)
                with open(head_path, 'wb') as f:
                    f.write(response.content)
                app.logger.info(f"Downloaded head for {username}")
                return True
        except Exception as e:
            app.logger.error(f"Error downloading head for {username}: {str(e)}")
    return os.path.exists(head_path)

def initialize_cache():
    """Load all player stats once at startup"""
    os.makedirs(HEADS_DIR, exist_ok=True)
    
    for file in os.listdir(STATS_DIR):
        if file.endswith('.json'):
            with open(os.path.join(STATS_DIR, file), 'r') as f:
                uuid = file.split('.')[0]
                try:
                    username = uuid_pseudo(uuid)
                    if username is not None:  # Only add non-None usernames
                        player_data = json.load(f)
                        PLAYERS_CACHE[username] = player_data
                        STATS_CACHE[username] = getstats(player_data)
                        # Précharger la tête du joueur
                        download_player_head(username)
                except Exception as e:
                    app.logger.error(f"Error loading stats for {uuid}: {str(e)}")
                    continue
    app.logger.info(f"Loaded stats for {len(PLAYERS_CACHE)} players")

@app.route('/')
def index():
    return render_template('index.html', players=list(PLAYERS_CACHE.keys()))

@app.route('/stats/<string:player>')
def get_stats(player):
    if player in STATS_CACHE:
        return render_template('stats.html', player=player, stats=STATS_CACHE[player])
    abort(404)

@app.route('/player-head/<username>')
def player_head(username):  # Changed function name to match URL format
    """Serve player head from local cache"""
    head_path = os.path.join(HEADS_DIR, f"{username}.png")
    if os.path.exists(head_path):
        return send_file(head_path, mimetype='image/png')
    abort(404)

# Initialize cache when the application starts
initialize_cache()

if __name__ == '__main__':
    app.run(debug=True)
