import os
from googleapiclient.discovery import build


class Video:
    api_key: str = os.getenv('API_KEY')
    youtube = build('youtube', 'v3', developerKey=api_key)

    def __init__(self, video_id):

        self.video_id = video_id
        self.title = None
        self.like_count = None

        try:
            self.video_id = video_id

            self.statistic = Video.youtube.videos().list(part='snippet,statistics,contentDetails,topicDetails',
                                                         id=video_id
                                                         ).execute()
            self.title = self.statistic['items'][0]['snippet']['title']
            self.link = "https://www.youtube.com/channel/" + video_id
            self.view_count = self.statistic['items'][0]['statistics']['viewCount']
            self.like_count = self.statistic['items'][0]['statistics']['likeCount']
        except Exception as ex:

            print("Пользователь передал несуществующий id видео!")

    def __str__(self):
        return f'{self.title}'


class PLVideo(Video):

    def __init__(self, video_id, play_id):
        super().__init__(video_id)
        self.play_id = play_id

