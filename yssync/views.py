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


class CreatePlaylist:

    def __init__(self):
        self.youtube_client = self.get_youtube_client()
        self.list_name = ""
        self.all_song_info = {}
        self.uploads_list_id = {}
        self.sutoringu = 'DOG inThePWO'

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


    def get_youtube_client(self):
        os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
        api_service_name = "youtube"
        api_version = "v3"
        client_secrets_file = "client_secret.json"
        scopes = ["https://www.googleapis.com/auth/youtube.readonly"]

        """ 
        creds = None
        youtube_client = None
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                creds = pickle.load(token)
       
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
        """
        flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
                    client_secrets_file, scopes)

        creds = flow.run_local_server(
                    host='localhost',
                    port=8088,
                    authorization_prompt_message='Please visit this URL: {url}',
                    success_message='The auth flow is complete; you may close this window.',
                    open_browser=True)
        """ 
            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)
 """
        youtube_client = googleapiclient.discovery.build(
                api_service_name, api_version, credentials=creds)

        return youtube_client


def index(request):
    cp = CreatePlaylist()
    cp.get_url_list()
    return render(request, 'yssync/index.html', {'sutoringu': cp.sutoringu})
