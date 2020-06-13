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
        self.playlist_lister = {}
        self.playlist_collection = []
        self.user_uri_list = []

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
                    success_message='<script>' +

                                    'function closeWin() {' +
                                    'myWindow.close();   // Closes the new window' +
                                    '} ' +

                                    'document.addEventListener("DOMContentLoaded", closeWin);' +

                                    '</script>',
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

                try:
                    video = youtube_dl.YoutubeDL().extract_info(youtube_url, download=False)

                    song_name = video['track']
                    artist = video['artist']
                    if song_name is not None and artist is not None:
                        print(video_title)
                        self.all_song_info[video_title] = {
                            "youtube_url": youtube_url,
                            "song_name": song_name,
                            "artist": artist,
                            "spotify_uri": self.get_spotify_uri(song_name, artist)
                        }
                except:
                    print("Video not available")

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

        if not uris:
            self.playlist_lister[playlist_name] = "no-songs-found"
            print("it is null")
            response_json = "it is null"
            return response_json

        else:
            self.playlist_lister[playlist_name] = "completed"
            print("it is not null")

            query = "https://api.spotify.com/v1/me"
            response = requests.get(
                query,
                headers={
                    "Content-Type": "application/json",
                    "Authorization": "Bearer {}".format(self.spotify_token)
                }
            )
            response_json = response.json()
            myid = response_json["id"]

            query = "https://api.spotify.com/v1/users/{}/playlists?limit=50".format(myid)
            response = requests.get(
                query,
                headers={
                    "Content-Type": "application/json",
                    "Authorization": "Bearer {}".format(self.spotify_token)
                }
            )
            response_json = response.json()

            for item in response_json["items"]:
                self.playlist_collection.append([item["name"], item["id"]])

            for item in self.playlist_collection:
                if playlist_name == item[0]:
                    playlist_id = item[1]
                    break
                else:
                    playlist_id = self.create_spotify_playlist(playlist_name)
                    break

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
            return response_json

    def add_songs_to_spotify(self, playlist_name, playlist_url):
        print("add_songs_to_spotify")
        playlist_id = self.playlist_exists(playlist_name)

        if playlist_id:
            print("Playlist exists")
            user_uri_list = self.feed_user_uri_list(playlist_id)
            self.get_songs_per_page(playlist_id, playlist_url, user_uri_list, playlist_name)
            print(self.playlist_lister)
        else:
            print("Playlist doesn't exists")
            playlist_id = self.create_spotify_playlist(playlist_name)
            self.get_songs_per_page(playlist_id, playlist_url, None, playlist_name)

    def my_id(self):
        print("getting my_id")
        query = "https://api.spotify.com/v1/me"
        response = requests.get(
            query,
            headers={
                "Content-Type": "application/json",
                "Authorization": "Bearer {}".format(self.spotify_token)
            }
        )
        response_json = response.json()

        myid = response_json["id"]
        return myid

    def playlist_exists(self, playlist_name):
        print("playlist_exists")
        playlist_collection = []

        myid = self.my_id()

        query = "https://api.spotify.com/v1/users/{}/playlists?limit=50".format(myid)
        response = requests.get(
            query,
            headers={
                "Content-Type": "application/json",
                "Authorization": "Bearer {}".format(self.spotify_token)
            }
        )
        response_json = response.json()

        for item in response_json["items"]:
            playlist_collection.append([item["name"], item["id"]])

        for item in playlist_collection:
            if playlist_name == item[0]:
                print("playlist matches")
                return item[1]

    def get_songs_per_page(self, playlist_id, list_url, user_uri_list, playlist_name):

        self.playlist_lister[playlist_name] = "no-changes-applied"

        if user_uri_list is None:
            user_uri_list = []
            self.playlist_lister[playlist_name] = "no-songs-found"

        ReturnToken = 'NULL'
        song_info = {}
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
                ReturnToken = 'NULL'

            for item in response["items"]:
                video_title = item["snippet"]["title"]
                youtube_url = "https://www.youtube.com/watch?v={}".format(item["snippet"]["resourceId"]["videoId"])
                try:
                    video = youtube_dl.YoutubeDL().extract_info(youtube_url, download=False)
                    song_name = video['track']
                    artist = video['artist']
                    if song_name is not None and artist is not None:
                        compare_uri = self.get_spotify_uri(song_name, artist)
                        if compare_uri not in user_uri_list:
                            print("new song added")
                            song_info[video_title] = {
                                "youtube_url": youtube_url,
                                "song_name": song_name,
                                "artist": artist,
                                "spotify_uri": compare_uri
                            }
                except:
                    print("Video not available")

            not_empty_playlist = self.check_if_empy_uris(song_info)

            if not_empty_playlist:
                self.playlist_lister[playlist_name] = "completed"
                self.send_uris_to_spotify(not_empty_playlist, playlist_id)
            else:
                print("empty list")

            song_info.clear()

            if ReturnToken == 'NULL':
                break

    def feed_user_uri_list(self, playlist_id):

        next = "https://api.spotify.com/v1/playlists/{}/tracks?fields=items(track(name%2C%20uri))%2C%20next&limit=50&offset=0".format(
            playlist_id)
        user_uri_list = []

        while True:
            print("feed_user_uri_list")
            query = next
            response = requests.get(
                query,
                headers={
                    "Content-Type": "application/json",
                    "Authorization": "Bearer {}".format(self.spotify_token)
                }
            )
            response_json = response.json()

            for item in response_json["items"]:
                full_uri = item["track"]["uri"]
                user_uri_list.append(full_uri)

            next = response_json["next"]

            if not next:
                break

        return user_uri_list

    def check_if_empy_uris(self, song_info):
        print("append_songs_to_playlist")

        uris = []
        for song, info in song_info.items():
            if info['spotify_uri'] != "lmao":
                print("song append to uris")
                uris.append(info['spotify_uri'])

        if uris:
            return uris
        else:
            return False

    def send_uris_to_spotify(self, uris, playlist_id):
        print("send_uris_to_spotify")
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
        return response_json

    def create_spotify_playlist(self, playlist_name):
        print("create_spotify_playlist")
        myid = self.my_id()
        request_body = json.dumps({
            "name": playlist_name,
            "description": "Playlist made with YoutubeSpotifySync app",
            "public": "true"
        })

        query = "https://api.spotify.com/v1/users/{}/playlists".format(myid)

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

    def get_url_info(self, url_info):

        urlInfoDict = {}

        request = self.youtube_client.playlists().list(
            id=url_info,
            part="snippet,contentDetails"
        )
        response = request.execute()
        print(response)

        for item in response["items"]:
            urlInfoDict = {'id': item["id"], 'title': item["snippet"]["title"],
                           'thumbnail': item["snippet"]["thumbnails"]["medium"]["url"],
                           'counter': item["contentDetails"]["itemCount"]}
        if urlInfoDict:
            return urlInfoDict
        else:
            return False

    def get_url_videos(self, playlist_id, goto_page):
        print("get_url_videos")


        if goto_page == "NULL":
            request = self.youtube_client.playlistItems().list(
                playlistId=playlist_id,
                part="snippet",
                maxResults=50
            )
        else:
            request = self.youtube_client.playlistItems().list(
                playlistId=playlist_id,
                part="snippet",
                pageToken=goto_page,
                maxResults=50
            )

        response = request.execute()

        try:
            prev_page = response["prevPageToken"]
        except:
            prev_page = "NULL"

        try:
            next_page = response["nextPageToken"]
        except:
            next_page = "NULL"

        videos_collection = []
        for item in response["items"]:
            videos_collection.append([item["snippet"]["resourceId"]["videoId"], item["snippet"]["title"], item["snippet"]["thumbnails"]["medium"]["url"]])

        context = {
            'videos': videos_collection,
            'prev_page': prev_page,
            'next_page': next_page,
        }

        data = json.dumps(context, indent=4, sort_keys=True, default=str)
        return data


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
    return render(request, 'yssync/index2.html',
                  {'username': cp.username, 'userpicture': cp.userpicture, 'listitem': cp.menu})


def callback(request):
    return render(request, 'yssync/spotifyLoginFinish.html', {})


def create_playlist_spotify(request):
    cp = CreatePlaylist()
    cp.get_user_info()
    if request.method == 'POST':
        cp.spotify_token = request.POST['accessToken']
    for playlist_name, url in request.POST.items():
        if playlist_name != 'accessToken':
            cp.add_songs_to_spotify(playlist_name, url)
    json_response = json.dumps(cp.playlist_lister)
    print(json_response)
    return HttpResponse(json_response)


def retrieve_playlist_url(request):
    cp = CreatePlaylist()
    cp.get_user_info()
    urlInfoFull = request.POST['playListURL']
    urlInfo = urlInfoFull.lstrip('https://www.youtube.com/playlist?list=')
    playlist_info_dict = cp.get_url_info(urlInfo)
    if playlist_info_dict:
        response_json = json.dumps(playlist_info_dict)
    else:
        response_json = "NULL"
    return HttpResponse(response_json)

def retrieve_video_list(request):
    cp = CreatePlaylist()
    cp.get_user_info()
    urlInfoFull = request.POST['playListId']
    goto_page = request.POST['goto_page']
    videos_collection = cp.get_url_videos(urlInfoFull, goto_page)
    response_json = json.dumps(videos_collection)
    return HttpResponse(response_json, content_type='application/json')
    #return HttpResponse(response_json)


























