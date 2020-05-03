import sys
import spotipy
import spotipy.util as util

scope = 'user-library-read'

if len(sys.argv) > 1:
    username = sys.argv[1]
else:
    print("Usage: %s username" % (sys.argv[0],))
    sys.exit()

token = util.prompt_for_user_token(username, scope)

if token:
    sp = spotipy.Spotify(auth=token)
    results = sp.album_tracks('spotify:album:3lGUiDSMpXjccoYh2B6i71')
    album_name = sp.album('spotify:album:3lGUiDSMpXjccoYh2B6i71')
    print(album_name['images'][0]['url'])
    print(album_name['artists'][0]['name'])
    print(album_name['name'])
    print("***")
    songs = results['items']
    for song_name in songs:
        print(song_name['name'])
else:
    print("Can't get token for", username)
