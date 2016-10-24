import base64
import json

import requests
import spotipy

from utils import url_encode, parse_form_data
from config import *

from flask import Flask, request, redirect, render_template, session, url_for


app = Flask(__name__)
app.secret_key = APP_SESSION_KEY
app.permanent_session_lifetime = 3600


@app.route('/')
def index():
    if not session.get('auth_header'):
        auth_url = url_encode(SPOTIFY_AUTH_URL, AUTH_QUERY_PARAMETERS)
        return redirect(auth_url)
    else:
        return redirect(url_for('home'))


@app.route('/callback/q')
def callback():
    auth_token = request.args['code']
    code_payload = {'grant_type': 'authorization_code',
                    'code': str(auth_token),
                    'redirect_uri': REDIRECT_URI
                    }
    base64encoded = base64.b64encode('{}:{}'.format(CLIENT_ID, CLIENT_SECRET))
    headers = {'Authorization': 'Basic {}'.format(base64encoded)}
    post_request = requests.post(SPOTIFY_TOKEN_URL, data=code_payload, headers=headers)

    response_data = json.loads(post_request.text)
    access_token = response_data['access_token']

    session['auth_header'] = {'Authorization': 'Bearer {}'.format(access_token)}

    return redirect(url_for('home'))


@app.route('/home')
def home():
    form_data = request.args

    if form_data:
        sp = spotipy.Spotify(auth=session['auth_header'])
        user_info = requests.get(SPOTIFY_ME_URL, headers=session['auth_header']).json()

        if form_data['artists']:
            artists = parse_form_data(form_data['artists'])
        else:
            artists = False

        if form_data['tracks']:
            tracks = parse_form_data(form_data['tracks'])
        else:
            tracks = False

        artist_ids = []
        if artists:
            for artist in artists:
                artist_search = sp.search(q='artist:' + artist, type='artist')
                if artist_search['artists']['total'] == 0:
                    artists = False
                    break
                artist_ids.append(artist_search['artists']['items'][0]['id'])

        track_ids = []
        if tracks:
            for track in tracks:
                track_search = sp.search(q='track:' + track, type='track')
                if track_search['tracks']['total'] == 0:
                    tracks = False
                    break
                track_ids.append(track_search['tracks']['items'][0]['id'])

        if artists is False and tracks is False:
            return render_template('sorry.html')

        results = sp.recommendations(seed_artists=artist_ids,
                                     seed_tracks=track_ids,
                                     limit=20,
                                     country='US')

        list_of_tracks = [track['id'] for track in results['tracks']]
        playlist = sp.user_playlist_create(user_info['id'], form_data['playlist_name'])
        playlist_id = playlist['id']

        results = sp.user_playlist_add_tracks(user_info['id'], playlist_id, list_of_tracks)

        playlist_links = {'desktop': playlist['uri'],
                          'browser': playlist['external_urls']['spotify']}

        return render_template('playlists.html',
                               desktop_link=playlist_links['desktop'],
                               browser_link=playlist_links['browser'])

    return render_template('home.html')


if __name__ == '__main__':
    app.run(debug=True, port=PORT)
