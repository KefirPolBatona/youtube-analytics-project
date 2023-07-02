import os
import json

from googleapiclient.discovery import build

api_key: str = os.getenv('YT_API_KEY')


class Channel:
    """Класс для ютуб-канала.
    Принимает id канала.
    Определяет аргументы:
        self.channel - общая информация о канале
        self.title - название канала
        self.info - описание канала
        self.url - вэб-ссылка на канал
        self.subscribers_count - количество подписчиков
        self.video_count - количество видео
        self.views_count - общее количество просмотров всех видео.
    """

    # Специальный объект для работы с API
    youtube = build('youtube', 'v3', developerKey=api_key)

    def __init__(self, channel_id: str) -> None:
        """
        Экземпляр инициализируется по id канала. Дальше все данные будут подтягиваться по API.
        """

        self.__channel_id = channel_id

        self.channel = Channel.youtube.channels().list(id=self.__channel_id, part='snippet,statistics').execute()
        self.title = self.channel["items"][0]["snippet"]["title"]
        self.info = self.channel["items"][0]["snippet"]["description"]
        self.url = f'https://www.youtube.com/channel/{self.__channel_id}'
        self.subscribers_count = self.channel["items"][0]["statistics"]["subscriberCount"]
        self.video_count = self.channel["items"][0]["statistics"]["videoCount"]
        self.views_count = self.channel["items"][0]["statistics"]["viewCount"]

    def __str__(self):
        """
        Возвращает название канала и ссылку на него
        """
        return f"{self.title}({self.url})"

    def __add__(self, other):
        """
        Определяет сумму подписчиков двух каналов
        """
        return int(self.subscribers_count) + int(other.subscribers_count)

    def __sub__(self, other):
        """
        Определяет разность подписчиков двух каналов
        """
        return int(self.subscribers_count) - int(other.subscribers_count)

    def __gt__(self, other):
        """
        Сравнивает количество подписчиков двух каналов методом больше
        """
        return int(self.subscribers_count) > int(other.subscribers_count)

    def __ge__(self, other):
        """
        Сравнивает количество подписчиков двух каналов методом больше/равно
        """
        return int(self.subscribers_count) >= int(other.subscribers_count)

    def __lt__(self, other):
        """
        Сравнивает количество подписчиков двух каналов методом меньше
        """
        return int(self.subscribers_count) < int(other.subscribers_count)

    def __le__(self, other):
        """
        Сравнивает количество подписчиков двух каналов методом меньше/равно
        """
        return int(self.subscribers_count) <= int(other.subscribers_count)

    def __eq__(self, other):
        """
        Сравнивает количество подписчиков двух каналов методом равно
        """
        return int(self.subscribers_count) == int(other.subscribers_count)

    def print_info(self) -> None:
        """
        Выводит в консоль общую информацию о канале.
        """

        return print(self.channel)

    def to_json(self, json_name=''):
        """
        Создает файл moscowpython.json и сохраняет в нем значения атрибутов экземпляра
        """

        with open(json_name, "w", encoding="utf-8") as write_file:
            return json.dump(self.__dict__, write_file, indent=2, ensure_ascii=False)

    @classmethod
    def get_service(cls):
        """
        Возвращает объект для работы с YouTube API вне класса
        """

        youtube = build('youtube', 'v3', developerKey=api_key)
        return youtube

    @property
    def channel_id(self):
        """
        Возвращает id канала
        """
        return self.__channel_id
