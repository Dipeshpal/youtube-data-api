import json
from apiclient.discovery import build


class Youtube_API:
    def __init__(self):
        file_name = "key.json"

        with open(file_name) as file:
            data = json.load(file)

            self.key = data['key']

        self.youtube = build('youtube', 'v3', developerKey=self.key)

    def get_channel_videos(self, channel_id):
        # get Uploads playlist id
        res = self.youtube.channels().list(id=channel_id,
                                      part='contentDetails').execute()
        playlist_id = res['items'][0]['contentDetails']['relatedPlaylists']['uploads']

        videos = []
        next_page_token = None

        while 1:
            res = self.youtube.playlistItems().list(playlistId=playlist_id,
                                               part='snippet',
                                               maxResults=50,
                                               pageToken=next_page_token).execute()
            videos += res['items']
            next_page_token = res.get('nextPageToken')

            if next_page_token is None:
                break

        return videos


obj = Youtube_API()
videos = obj.get_channel_videos('UCGEoRAK92fUk2kY3kSJMR_Q')
