import json
import os

from googleapiclient.discovery import build


class Channel:
    """Класс для ютуб-канала"""
    api_key: str = os.getenv('API_KEY')
    youtube = build('youtube', 'v3', developerKey=api_key)

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        self.__channel_id = channel_id
        self.channel = Channel.youtube.channels().list(id=self.channel_id, part='snippet,statistics').execute()
        self.title = self.channel['items'][0]['snippet']['title']
        self.video_count = self.channel['items'][0]['statistics']['videoCount']
        self.description = self.channel['items'][0]['snippet']['description']
        self.subscriberCount = self.channel['items'][0]['statistics']['subscriberCount']
        self.viewCount = self.channel['items'][0]['statistics']['viewCount']
        self.url = "https://www.youtube.com/channel/" + channel_id

    @property
    def channel_id(self):
        return self.__channel_id

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        python = json.dumps(self.channel, indent=2, ensure_ascii=False)
        print(python)

    @classmethod
    def get_service(cls):
        """
        Класс-метод возвращающий новый экземпляр для работы с API
        """

        return cls.youtube

    def to_json(self, filename: str):
        """
        Метод класса для записи атрибутов экземпляра в файл формата json
        """

        data_get_api = {"channel_id": self.channel_id, "title": self.title,
                        "video_count": self.video_count, "description": self.description,
                        "subscriberCount": self.subscriberCount, "viewCount": self.video_count, "url": self.url}
        with open(filename, "a", encoding='UTF-8') as file:
            if os.stat(filename).st_size == 0:
                json.dump([data_get_api], file, indent=2, ensure_ascii=False)
            else:
                with open(filename) as json_file:
                    data_list = json.load(json_file)
                data_list.append(data_get_api)
                with open(filename, "w", encoding='UTF-8') as json_file:
                    json.dump(data_list, json_file, indent=2, ensure_ascii=False)
