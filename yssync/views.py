from django.http import HttpResponse
from django.shortcuts import render
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import os
import pickle
import json
import requests
import os.path
import youtube_dl


class CreatePlaylist:

    def __init__(self):
        self.youtube_client = {}
        self.list_name = ""
        self.username = ""
        self.userpicture = ""
        self.all_song_info = {}
        self.uploads_list_id = {}
        self.sutoringu = 'DOG inThePWO'
        self.list_menu = {}
        self.menu = []
        self.urlInfoDict = {}
        self.spotify_token = {}
        self.youtube_ulr = ""

    def get_user_info(self):
        self.youtube_client = self.get_youtube_client()
        request = self.youtube_client.channels().list(
            mine="True",
            part="id,snippet,contentDetails"
        )

        """self.sutoringu = request.execute()"""

        response = request.execute()

        for item in response["items"]:
            self.username = item["snippet"]["title"]
            self.userpicture = item["snippet"]["thumbnails"]["high"]["url"]

    def get_url_list(self):

        opt2 = 'https://www.youtube.com/playlist?list=PLi3XTR26mSxVqLKXtkZqBcujFylqK7n7n'
        opt2 = opt2.strip('https://www.youtube.com/playlist?list=')

        request = self.youtube_client.playlists().list(
            id=opt2,
            part="snippet,contentDetails"
        )

        response = request.execute()
        for item in response["items"]:
            self.list_name = item["snippet"]["title"]

        request = self.youtube_client.playlistItems().list(
            playlistId=opt2,
            part="snippet",
            maxResults=50
        )

        self.sutoringu = request.execute()

    def get_url_info(self, url_info):
        request = self.youtube_client.playlists().list(
            id=url_info,
            part="snippet,contentDetails"
        )
        response = request.execute()

        for item in response["items"]:
            self.urlInfoDict = {'id': item["id"], 'title': item["snippet"]["title"],'thumbnail': item["snippet"]["thumbnails"]["high"]["url"],'counter': item["contentDetails"]["itemCount"]}

        print(self.urlInfoDict)

        return response

    def get_youtube_lists(self):
        request = self.youtube_client.playlists().list(
            mine=True,
            part="snippet,contentDetails",
            maxResults="50"
        )

        response = request.execute()

        print(response)

        for item in response["items"]:
            self.menu.append([item["id"], item["snippet"]["title"], item["snippet"]["thumbnails"]["medium"]["url"],
                              item["contentDetails"]["itemCount"]])

        self.sutoringu = response

    def create_spotify_playlist(self, playlist_name):
        request_body = json.dumps({
            "name": playlist_name,
            "description": "All liked YouTube Videos",
            "public": "true"
        })

        query = "https://api.spotify.com/v1/users/{}/playlists".format("y7tgnyerhxbjzontdni3f69fw")

        response = requests.post(
            query,
            data=request_body,
            headers={
                "Content-Type": "application/json",
                "Authorization": "Bearer {}".format(self.spotify_token)
            }
        )

        response_json = response.json()
        return response_json["id"]

    def get_youtube_client(self):
        os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
        api_service_name = "youtube"
        api_version = "v3"
        client_secrets_file = "client_secret.json"
        scopes = ["https://www.googleapis.com/auth/youtube.readonly"]
        creds = None

        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                creds = pickle.load(token)

        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
                    client_secrets_file, scopes)

                creds = flow.run_local_server(
                    host='localhost',
                    port=8088,
                    authorization_prompt_message='Please visit this URL: {url}',
                    success_message='The auth flow is complete; you may close this window.',
                    open_browser=True)

            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)

        youtube_client = googleapiclient.discovery.build(api_service_name, api_version, credentials=creds)
        return youtube_client

    def get_songs_list(self, list_url):
        ReturnToken = 'NULL'
        while True:

            if ReturnToken == 'NULL':
                request = self.youtube_client.playlistItems().list(
                    playlistId=list_url,
                    part="snippet",
                    maxResults=50
                )
            else:
                request = self.youtube_client.playlistItems().list(
                    playlistId=list_url,
                    part="snippet",
                    pageToken=ReturnToken,
                    maxResults=50
                )

            response = request.execute()
            try:
                ReturnToken = response["nextPageToken"]
            except:
                print('Last page')
                ReturnToken = 'NULL'

            for item in response["items"]:
                video_title = item["snippet"]["title"]
                youtube_url = "https://www.youtube.com/watch?v={}".format(item["snippet"]["resourceId"]["videoId"])
                video = youtube_dl.YoutubeDL().extract_info(youtube_url, download=False)
                song_name = video['track']
                artist = video['artist']
                if song_name is not None and artist is not None:
                    self.all_song_info[video_title] = {
                        "youtube_url": youtube_url,
                        "song_name": song_name,
                        "artist": artist,
                        "spotify_uri": self.get_spotify_uri(song_name, artist)
                    }
            if ReturnToken == 'NULL':
                break

    def get_spotify_uri(self, song_name, artist):

        query = "https://api.spotify.com/v1/search?query=track%3A{}+artist%3A{}&type=track&offset=0&limit=20".format(
            song_name,
            artist
        )

        response = requests.get(
            query,
            headers={
                "Content-Type": "application/json",
                "Authorization": "Bearer {}".format(self.spotify_token)
            }
        )

        response_json = response.json()
        songs = response_json['tracks']['items']

        try:
            uri = songs[0]['uri']
        except:
            uri = "lmao"
            print("An exception occurred")

        return uri

    def add_songs_to_playlist_url(self, playlist_name):
        uris = []
        for song, info in self.all_song_info.items():
            if info['spotify_uri'] != "lmao":
                uris.append(info['spotify_uri'])
        print(uris)
        playlist_id = self.create_spotify_playlist(playlist_name)
        request_data = json.dumps(uris)
        query = "https://api.spotify.com/v1/playlists/{}/tracks?position=0".format(playlist_id)
        response = requests.post(
            query,
            data=request_data,
            headers={
                "Content-Type": "application/json",
                "Authorization": "Bearer {}".format(self.spotify_token)
            }
        )
        response_json = response.json()
        print(response_json)
        return response_json


def index2(request):
    cp = CreatePlaylist()
    cp.get_user_info()
    cp.get_youtube_lists()

    # return render(request, 'yssync/index2.html', {'sutoringu': cp.menu})
    return render(request, 'yssync/index.html',
                  {'username': cp.username, 'userpicture': cp.userpicture, 'listitem': cp.menu})

def index(request):
    cp = CreatePlaylist()
    cp.get_user_info()
    cp.get_youtube_lists()
    return render(request, 'yssync/index2.html', {'username': cp.username, 'userpicture': cp.userpicture, 'listitem': cp.menu})

def callback(request):
    return render(request, 'yssync/spotifyLoginFinish.html', {})


def create_playlist_spotify(request):
    cp = CreatePlaylist()
    cp.get_user_info()
    if request.method == 'POST':
        cp.spotify_token = request.POST['accessToken']
    for playlist_name, url in request.POST.items():
        if playlist_name != 'accessToken':
            cp.get_songs_list(url)
            cp.add_songs_to_playlist_url(playlist_name)
            cp.all_song_info.clear()
    return HttpResponse('Ready')


def retrieve_playlist_url(request):
    cp = CreatePlaylist()
    cp.get_user_info()
    urlInfoFull = request.POST['playListURL']
    urlInfo = urlInfoFull.strip('https://www.youtube.com/playlist?list=')
    cp.get_url_info(urlInfo)
    response_json = json.dumps(cp.urlInfoDict)
    print(response_json)
    return HttpResponse(response_json)
