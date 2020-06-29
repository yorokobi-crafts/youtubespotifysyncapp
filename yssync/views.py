import sys
from django.http import HttpResponse
from django.shortcuts import render
import json
import requests
import youtube_dl
from django.views.decorators.csrf import ensure_csrf_cookie
from oauth2client import client
import httplib2
from apiclient import discovery


# Let's create a new class to manage the playlists we are going to synchronize
class CreatePlaylist:

    # Declarations
    def __init__(self):
        self.youtube_client = {}
        self.username = ""
        self.userpicture = ""
        self.menu = []
        self.spotify_token = {}
        self.playlist_lister = {}
        self.list_item_count = ""
        self.session = {}

    # To get the user information, we ask for the credentials we stored previously in a cookie, passed as the creds
    # variable We get the Youtube Client using the get_youtube_client function along with the creds We ask for a list
    # with the information of our Youtube Client's channel. Then, we retrieve the user's name and the user's profile
    # picture.
    def get_user_info(self, creds):
        self.youtube_client = self.get_youtube_client(creds)
        request = self.youtube_client.channels().list(
            mine="True",
            part="id,snippet,contentDetails"
        )

        response = request.execute()

        for item in response["items"]:
            self.username = item["snippet"]["title"]
            self.userpicture = item["snippet"]["thumbnails"]["high"]["url"]

    # We set the api service name as Youtube, and its version as v3
    # The credentials can be authorized using the authorize function and the httplib2 library
    # It's time to build the Youtube client using our previously configured parameters.
    # Lastly, the Youtube client is returned ready to be used.
    def get_youtube_client(self, creds):
        api_service_name = "youtube"
        api_version = "v3"

        http_auth = creds.authorize(httplib2.Http())
        youtube_client = discovery.build(api_service_name, api_version, http=http_auth)
        return youtube_client

    # This function lets us acces the information of the playlists owned by the Youtube client. We make a request asking
    # for a list of playlists owned by the Youtube client. The snippet part contains the information of the playlists,
    # and the contentDetails parts gives us the number videos in the playlist. After executing the request, we set the
    # total number of playlists found in the list_item_count variable Finally, it's time for looping through the
    # response, looking for the id, the title, the thumbnail url and the videos within the playlist.
    def get_youtube_lists(self):
        request = self.youtube_client.playlists().list(
            mine=True,
            part="snippet,contentDetails",
            maxResults="50"
        )

        response = request.execute()

        self.list_item_count = response["pageInfo"]["totalResults"]

        for item in response["items"]:
            self.menu.append([item["id"], item["snippet"]["title"], item["snippet"]["thumbnails"]["medium"]["url"],
                              item["contentDetails"]["itemCount"]])

    # Let's set a default query that we can use to search of a song. We can use the song_name and the artist
    # variables to get the correct song. After the query is set, let's make a request with the proper header stated
    # by Spotify. Go to Spotify docs for more information-> https://developer.spotify.com/console/get-search-item/
    # Turn the response into JSON data, and set the songs variable with the tracks information. Choose the first
    # retrieved song's element, wich is the uri information, and try to set it into the uri variable. If this is
    # successful, return the value. If not, set it with an error message that we will use later to recognize that the
    # song information is not available ( Usually for copyright or regional issues).
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
            uri = "error"

        return uri

    # This function is used to generate the process of creating a playlist, add the songs to the playlist and lastly
    # complete the synchronization process. We need the Youtube playlist's name, its url and the array of items we
    # want to avoid during the synchronization process. We ask if the user already has a Spotify playlist with the
    # same name of the playlist we are trying to sync. If the user does have the playlist, store the Spotify
    # playlist's id in the playlist_id variable. If the playlist exists, we ask for the songs within the playlist,
    # and store them in the user_uri_list We will use the user_uri_list to avoid synchronizing already duplicated
    # songs. get_songs_per page will start the process of syncing using the playlist id, the user's songs already in
    # the playlist, the playlist name and the songs we won't sync. If the user doesn't have a Spotify playlist with
    # the same name of the playlist to sync, we create a new Spotify playlist with the name of the Youtube playlist
    # to sync wiht the create_spotify_playlist function. After that, proceed to start the syncing process without an
    # user_uri_list since the Spotify playlist doesn't exists.
    def add_songs_to_spotify(self, playlist_name, playlist_url, ignored_array):
        playlist_id = self.playlist_exists(playlist_name)

        if playlist_id:
            user_uri_list = self.feed_user_uri_list(playlist_id)
            self.get_songs_per_page(playlist_id, playlist_url, user_uri_list, playlist_name, ignored_array)
        else:
            playlist_id = self.create_spotify_playlist(playlist_name)
            self.get_songs_per_page(playlist_id, playlist_url, None, playlist_name, ignored_array)

    # It is necessary to know the user's Spotify id to get the user's playlists' information. A request asking for the
    # user's information must be set with the correct format specified by Spotify. Go to Spotify docs for more
    # information-> https://developer.spotify.com/console/get-current-user/ Turn the response of the request into JSON
    # data and then ask for the id value. Return the the user's id as the myid variable.
    def my_id(self):
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

    # We can know if the user already has a Spotify playlist with the same name of the playlist we are trying to
    # sync. We need to pass the playlist_name in order to do that. Get the user id with the my_id function and set it
    # in the myid variable. A request asking for the user's playlists must be set with the correct format specified
    # by Spotify.  Go to Spotify docs for more information->
    # https://developer.spotify.com/console/get-playlists/?user_id=wizzler Turn the response of the request into JSON
    # data. Loop through the response looking for every item and compare each Spotify playlist's name with the name
    # of the playlist to sync. Return the id of the duplicated playlist if exists.
    def playlist_exists(self, playlist_name):

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
            if playlist_name == item["name"]:
                return item["id"]

    # This might be the most complex part of the program. The function get_songs_per_page gets all the tracks from a
    # Youtube playlist and sends them to a Spotify playlist. The function asks for a playlist id to work on,
    # a Youtube playlist where it will obtain the songs from, a list of the user's songs already in the spotify
    # playlist (if exists) The name of the playlist and an array with the songs we want to avoid during the syncing
    # process. playlist_lister is a dictionary that contains all the Youtube playlists we are going to sync We want
    # to show the user the result of the syincing process, so we set 'no-changes-applied' as the default option This
    # is because this status will be overwritten if a change is applied. We check if the user uri list is empty (This
    # will be the case if the Spotify playlist is not duplicated) If there is not user uri list we set the value
    # empty and change the playlist status to "no-songs-found". This means that the playlist is new, so there must be
    # changes (songs added). "no-songs-found" will only change if actual songs were found afterwards. We set the
    # return_token as NULL in order to break the syncing loop if there is just one page in the Youtube playlist.
    # Create a song_info dictionary to store the information o all the found songs. Start an infinite loop Verify is
    # return_token is NULL. This will happen always the first time the loop starts. If the return_token is NULL,
    # create a request asking for a list with the user's playlists. Retrieve the snipped part and 50 items. (The
    # limit) If the return_token is not NULL it means the playlist has a previous or next page. Be sure to create a
    # request with the pageToken parameter in order to get the previous or the next page. Get the response of the
    # request and try to set the nextPageToken value to the return_token variable. If the youtube playlist doesn't
    # have a previous or next page thiw will fail and you must set the return_token to NULL again. Loop through the
    # response and set the video_title, youtube_url and youtube_id with the correct values. Verify if the current
    # video is not a video you must ignore. If not, try to extract the song information within the Youtube video and
    # set the song_name and artist variables with the correct values. If you success, compare the video with the
    # user's videos in Spotify. (If it's not a playlist already in Spotify, user_uri_list will be None and the
    # comparison will always return False, don't worry) Create a new key in the song_info dictionary for the current
    # video and set the video information. Verify if the song_info dictionary has actual songs that we can send to
    # Spotify or if it is empty. This will return a new list with only syncrhonizable songs. If the song_info
    # dictionary is not empty, set the playlist status to 'completed' since we have actual songs to sync. Use the
    # send_uris_to_spotify function to sent the non_empty_playlist to the correct Spotify playlist specified in the
    # playlist_id variable. Be sure to clear the song_info dictionary in order to send only the correct songs of each
    # Youtube playlist page. break the wile loop if the return_token is NULL, since this means there's no more pages
    # to loop through.
    def get_songs_per_page(self, playlist_id, list_url, user_uri_list, playlist_name, ignored_array):

        self.playlist_lister[playlist_name] = "no-changes-applied"

        if user_uri_list is None:
            user_uri_list = []
            self.playlist_lister[playlist_name] = "no-songs-found"

        return_token = 'NULL'
        song_info = {}
        while True:

            if return_token == 'NULL':
                request = self.youtube_client.playlistItems().list(
                    playlistId=list_url,
                    part="snippet",
                    maxResults=50
                )
            else:
                request = self.youtube_client.playlistItems().list(
                    playlistId=list_url,
                    part="snippet",
                    pageToken=return_token,
                    maxResults=50
                )

            response = request.execute()
            try:
                return_token = response["nextPageToken"]
            except:
                return_token = 'NULL'

            for item in response["items"]:
                video_title = item["snippet"]["title"]
                youtube_url = "https://www.youtube.com/watch?v={}".format(item["snippet"]["resourceId"]["videoId"])
                youtube_id = item["snippet"]["resourceId"]["videoId"]

                if youtube_id not in ignored_array:
                    try:
                        video = youtube_dl.YoutubeDL().extract_info(youtube_url, download=False)
                        song_name = video['track']
                        artist = video['artist']
                        if song_name is not None and artist is not None:
                            compare_uri = self.get_spotify_uri(song_name, artist)
                            if compare_uri not in user_uri_list:
                                song_info[video_title] = {
                                    "youtube_url": youtube_url,
                                    "song_name": song_name,
                                    "artist": artist,
                                    "spotify_uri": compare_uri
                                }
                    except Exception:
                        sys.exc_clear()

            not_empty_playlist = self.check_if_empty_uris(song_info)

            if not_empty_playlist:
                self.playlist_lister[playlist_name] = "completed"
                self.send_uris_to_spotify(not_empty_playlist, playlist_id)

            song_info.clear()

            if return_token == 'NULL':
                break

    # The feed_user_uri_list will ask for the user's videos in a determined playlist specified by the playlist_id
    # variable. We can only ask for 50 songs at the time, so we set that as the limit amount in the query and we loop
    # through the whole playlist using a while loop and the next data. Let's create the user_uri_list, where we are
    # going to store the user's uris. Create a while loop, and after the query is set, let's make a request with the
    # proper header specified by Spotify. Go to Spotify docs for more information->
    # https://developer.spotify.com/console/get-playlist-tracks/ Turn the response of the request into JSON data and
    # iterate it. Append each track uri to the user_uri_list array. Set the response's next value to the next
    # variable. It if fails, break the while loop. This means there are no more items to retrieve.
    def feed_user_uri_list(self, playlist_id):
        next = "https://api.spotify.com/v1/playlists/{}/tracks?fields=items(track(name%2C%20uri))%2C%20next&limit=50&offset=0".format(
            playlist_id)
        user_uri_list = []

        while True:
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
                user_uri_list.append(item["track"]["uri"])

            next = response_json["next"]

            if not next:
                break

        return user_uri_list

    # The check_if_empty_uris function will verify if the songs can be sent to Spotify. We achieve this by verifying
    # that the song has not 'error' set as the spotify_uri value. If it is not the case, append the uri to the new
    # uri list. If there are actually uris in the new uri array, return the content of the array. If the uris array
    # is empty just return False.
    def check_if_empty_uris(self, song_info):

        uris = []
        for song, info in song_info.items():
            if info['spotify_uri'] != "error":
                uris.append(info['spotify_uri'])

        if uris:
            return uris
        else:
            return False

    # This is the final process of each Youtube playlist. The send_uris_to_spotify function uses a uris array to send
    # and a playlist_id to specify the playlist the songs in the uris array will be sent to. Set the request_data
    # variable with the uris as JSON data. A request to send the tracks to the Spotify playlist must be set with the
    # correct format specified by Spotify. Go to Spotify docs for more information->
    # https://developer.spotify.com/console/post-playlist-tracks/ Turn the response of the request into JSON data and
    # its content.
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

    # The create_spotify_playlist will allow us to create a new Spotify playlist if the user has not a playlist with
    # the same name of the playlist to sync already. Use the my_id function and set the user's id in the myid
    # variable. Define the body of the request and include the name of the new Spotify playlist. A request to create
    # a new Spotify playlist must be set with the correct format specified by Spotify. Go to Spotify docs for more
    # information-> https://developer.spotify.com/console/post-playlists/ Turn the response of the request into JSON
    # data and its content.
    def create_spotify_playlist(self, playlist_name):
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

    # The get_url_info will obtain the information of a determined Youtube playlist. Create a request that asks for
    # the snippet and the contentDetails of a playlist specified by the url_info. Iterate over each item in the
    # response looking for the playlist's id, title thumbnail url, and the number of videos within it. Return the
    # content of the url_info_dict if there is information, and return Flase if the process failed.
    def get_url_info(self, url_info):
        url_info_dict = {}

        request = self.youtube_client.playlists().list(
            id=url_info,
            part="snippet,contentDetails"
        )
        response = request.execute()

        for item in response["items"]:
            url_info_dict = {'id': item["id"], 'title': item["snippet"]["title"],
                             'thumbnail': item["snippet"]["thumbnails"]["medium"]["url"],
                             'counter': item["contentDetails"]["itemCount"]}
        if url_info_dict:
            return url_info_dict
        else:
            return False

    # The get_url_videos function will retrieve the videos of a determined playlist specified by a playlist id. It
    # also recieves a specific page valgue if provided by the user. If the user did not provided a Youtube playlist
    # specific page (next page or previous page) set the goto_page value to NULL Proceed to create a request asking
    # for a list with the videos of the provided Youtube playlist. If the user actually selected a specific page to
    # go, use that value as the pageToken in the request. Try to read the prevPageToken and the nextPageToken,
    # and if exists set it to the prev_page and next_page variables. Create a video_collection array, then iterate
    # over the items in the response of the request and get its video id, title and thumbnail url. Create a context
    # dictionary and include the previously retrieved information. Turn the context array into JSON data, and return
    # its content.
    def get_url_videos(self, playlist_id, goto_page):

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
            videos_collection.append([item["snippet"]["resourceId"]["videoId"], item["snippet"]["title"],
                                      item["snippet"]["thumbnails"]["medium"]["url"]])

        context = {
            'videos': videos_collection,
            'prev_page': prev_page,
            'next_page': next_page,
        }

        data = json.dumps(context, indent=4, sort_keys=True, default=str)
        return data


# Ensure the sending of the csrf cookie in order to be able to communicate this the application later The index
# function is the principal function in this program First of all, try to get the sessionCookie. This stores the
# information of the user's session. If you successfully retrieve the sessionCookie, this means the user has already
# logged in, so you can the user enter to the core application. Otherwise, you must send the user to the landing page
# in order to let the user log in. If there's already a session stored in the cookies, create a new object of the
# class CreatePlaylist. This will manage the entire playlists. Get the user information using the stored credentials.
# This will retrieve the user's Youtube client. Start the get_youtube_lists function. This will run the entire
# syncing process. Then you can send the needed information to the final user in the application.
@ensure_csrf_cookie
def index(request):
    creds = request.session.get('sessionCookie', None)
    if creds:
        cp = CreatePlaylist()
        cp.get_user_info(creds)
        cp.get_youtube_lists()
        return render(request, 'yssync/index2.html',
                      {'username': cp.username, 'userpicture': cp.userpicture, 'listitem': cp.menu,
                       'itemCount': cp.list_item_count})
    else:
        return render(request, 'yssync/login.html')


# The callback function is used as the redirect URL for the Spotify login process.
def callback(request):
    return render(request, 'yssync/spotifyLoginFinish.html', {})


# The retrieve_playlist_url function retrieves the information of a specified Youtube playlist. First, try to obtain
# the sessionCookie. The create an object of the class CreatePlaylist. Get the user's information using the stored
# credentials and the get_user_info function. Get the provided Youtube playlist URL stored in the 'playListURL' data
# in the post request, and set it in the url_info_full variable. Remove the main part of the url and keep the
# playlist id in the url_info variable. Use the get_url_info function with the url_info variable to get the
# information of the playlist and set that information in the playlist_info_dict. If it is successful,
# turn the playlist_info_dict into JSON data and store it in the response_json variable. Otherwise set the
# response_json variable to NULL. Lastly, return the resulting information in response_json.
def retrieve_playlist_url(request):
    creds = request.session.get('sessionCookie', None)
    cp = CreatePlaylist()
    cp.get_user_info(creds)
    url_info_full = request.POST['playListURL']
    url_info = url_info_full.lstrip('https://www.youtube.com/playlist?list=')
    playlist_info_dict = cp.get_url_info(url_info)
    if playlist_info_dict:
        response_json = json.dumps(playlist_info_dict)
    else:
        response_json = "NULL"
    return HttpResponse(response_json)


# The retrieve_video_list function retrieves the videos within a specified Youtube playlist. First, try to obtain the
# sessionCookie. The create an object of the class CreatePlaylist. Get the user's information using the stored
# credentials and the get_user_info function. Get the provided Youtube playlist URL stored in the 'playListURL' data
# in the post request, and set it in the url_info_full variable. Also get the 'goto_page' data in the post request
# and store it in the goto_page variable. This is the page we are going to read. Get the videos of the playlist by
# using the get_url_videos function and store the resulting information in the videos_collection variable Turn the
# videos_collection variable intro JSON data and send it to the final user in the application.
def retrieve_video_list(request):
    creds = request.session.get('sessionCookie', None)
    cp = CreatePlaylist()
    cp.get_user_info(creds)
    url_info_full = request.POST['playListId']
    goto_page = request.POST['goto_page']
    videos_collection = cp.get_url_videos(url_info_full, goto_page)
    response_json = json.dumps(videos_collection)
    return HttpResponse(response_json, content_type='application/json')


# The delete_cookie function is used to 'log out' the user. Since once the user has not session data stored in
# cookies, the apaplication leads the user to the landing page instead of the core application. Try to delete the
# stored sessionCookie. Set the status variable as 200 is successful, otherwise set it to 500.
def delete_cookie(request):
    try:
        del request.session['sessionCookie']
        status = "200"
    except:
        status = "500"
    return HttpResponse(status)


# The login function let's the user login if there's not session data stored in cookies. It prevents the user to go
# to the core application without loggin in previously. It is also used in the core applications for swapping the
# current user. Once the authentication proccess is done in the frontend, the resulting authentication code is sent
# to this application by a post request. Get that authentication code and store it in the auth_code variable. Specify
# the path were yout secret is stored in the client_secrets_file variable. Set the desired scope in the scopes
# variable. Use the client library's get credentials from client secrets and code and use yout client secrets,
# your scope and yout authentication code. Store the resulting session in the credentials variable. Set a
# 'sessionCookie' cookie that will contain the resulting credentials. These credentials will be used by the user
# whether until the session expires or the user logs out and the cookie is destroyed.
def login(request):
    auth_code = request.POST['auth_code']

    client_secrets_file = "client_secret.json"
    scopes = ["https://www.googleapis.com/auth/youtube.readonly"]

    credentials = client.credentials_from_clientsecrets_and_code(
        client_secrets_file,
        scopes,
        auth_code)

    request.session['sessionCookie'] = credentials
    return HttpResponse('200')
