import spotipy
import spotipy.util as util

scope = 'user-top-read'
username = 'juan'
token = util.prompt_for_user_token(username, scope)
urn = 'spotify:artist:57YJQe0ayvIaRZJ3PW5nFP'
sp = spotipy.Spotify()

if token:
    sp = spotipy.Spotify(auth=token)
    album = sp.albums(['spotify:album:7acEciVtnuTzmwKptkjth5'])
    print(album['albums'][0]['images'])
    results = sp.artist(urn)
    print(results ['name'])

    user = sp.user('12151651273')
    print(user['display_name'])
else:
    print("Can't get token for", username)
