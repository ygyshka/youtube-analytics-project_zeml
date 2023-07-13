import datetime
#from datetime import datetime
from src.video import Video
import time
import json
import isodate
import os
from googleapiclient.discovery import build


class MixConnect:
    """
    Класс-миксин, для получения коннекта с API YouTube
    """
    def open_conn(self):
        api_key: str = os.getenv('API_KEY')
        youtube = build('youtube', 'v3', developerKey=api_key)
        return youtube


class PlayList(MixConnect):

    def __init__(self, play_id):
        self.play_id = play_id
        self.response = self.get_data()
        self.play_info = self.get_info()
        self.title = self.play_info['items'][0]['snippet']['title']
        self.url = "https://www.youtube.com/playlist?list=" + play_id

        video_ids = [video['contentDetails']['videoId'] for video in self.response['items']]
        self.time_videos = self.open_conn().videos().list(part='contentDetails,statistics',
                                                          id=','.join(video_ids)
                                                          ).execute()

        self.__total_duration = datetime.timedelta(seconds=0)
        for vid in self.time_videos['items']:

            iso_8601_duration = vid['contentDetails']['duration']
            duration = isodate.parse_duration(iso_8601_duration)
            self.__total_duration += duration

    @property
    def total_duration(self):
        return self.__total_duration

    def show_best_video(self):
        """
        Метод для поиска ссылки на популярное видео
        """

        best_video = 'https://youtu.be/'
        id_best_video = ''
        check_like = 0
        for vid in self.time_videos['items']:
            if check_like > int(vid['statistics']['likeCount']):
                id_best_video = vid['id']
                return f'{best_video + id_best_video}'
                # return best_video + vid['id']
            else:
                check_like = int(vid['statistics']['likeCount'])
                id_best_video = vid['id']

        return best_video + id_best_video

    def total_seconds(self):
        """
        Возвращает общее количество времени всех видео в плайлисте в секундах
        """

        total_s = 0
        for vid in self.time_videos['items']:
            iso_8601_duration = vid['contentDetails']['duration']
            duration = isodate.parse_duration(iso_8601_duration)
            total_s += duration.total_seconds()

        return total_s

    def get_data(self):
        """
        Возвращает общую информацию наполнения плайлиста по ID
        """

        response = self.open_conn().playlistItems().list(playlistId=self.play_id,
                                                         part='contentDetails,snippet',
                                                         maxResults=50,
                                                         ).execute()
        return response

    def get_info(self):
        """
        Возвращает общую информацию плайлиста по ID
        """

        play_list_info = self.open_conn().playlists().list(id=self.play_id,
                                                           part='snippet'
                                                           ).execute()

        return play_list_info
