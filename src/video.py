from src.channel import Channel
import json
import os
from googleapiclient.discovery import build


class Video:
    api_key: str = os.getenv('API_KEY')
    youtube = build('youtube', 'v3', developerKey=api_key)

    def __init__(self, video_id):
        self.video_id = video_id
        self.statistic = Video.youtube.videos().list(part='snippet,statistics,contentDetails,topicDetails',
                                                     id=video_id
                                                     ).execute()
        self.name = self.statistic['items'][0]['snippet']['title']
        self.link = "https://www.youtube.com/channel/" + video_id
        self.view_count = self.statistic['items'][0]['statistics']['viewCount']
        self.view_like = self.statistic['items'][0]['statistics']['likeCount']

    def __str__(self):
        return f'{self.name}'


class PLVideo(Video):

    def __init__(self, video_id, play_id):
        super().__init__(video_id)
        self.play_id = play_id

