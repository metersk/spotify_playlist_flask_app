This Flask app makes use of the Spotify recommendations endpoint to dynamically generate a playlist based on up to 5 seed artists and or/tracks.  It will then add the playlist to your account and provide links to open in the browser or desktop app.

To run this app locally:

1. Clone repo and `cd` into it
2. Create python virtual environment and activate it
3. Install the requirements with `pip install -r requirements.txt`
4. Update the following variables in `config.py`
  - `APP_SESSION_KEY`: can be anything
  - `CLIENT_ID`: generate by registering an application [here](https://developer.spotify.com/my-applications/#!/applications)
  - `CLIENT_SECRET`: generate by registering an application [here](https://developer.spotify.com/my-applications/#!/applications)
5. Add `http://127.0.0.1:8080/callback/q` to the Redirect URIs in the Spotify console for you newly registered app
6. Run `python app.py`
7. Navigate to http://127.0.0.1:8080/
