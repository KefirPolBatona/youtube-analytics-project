import os

from googleapiclient.discovery import build

api_key: str = os.getenv('YT_API_KEY')


class Video:
    """
    Класс для ютуб-видео.
    Принимает аргументы:
        self.id_video - id видео.
    Определяет свойства:
        self.video_response - статистика видео,
        self.title_video - название видео,
        self.url_video - ссылка на видео,
        self.views_video - количество просмотров,
        self.like_video - количество лайков.
    """

    # Специальный объект для работы с API
    youtube = build('youtube', 'v3', developerKey=api_key)

    def __init__(self, id_video):
        """
        Экземпляр инициализируется по id видео.
        """
        self.id_video = id_video
        self.video_response = Video.youtube.videos().list(part='snippet,statistics,contentDetails,topicDetails',
                                                          id=id_video).execute()
        self.title_video = self.video_response['items'][0]['snippet']['title']
        self.url_video = f'https://www.youtube.com/watch?v={self.id_video}'
        self.views_video = self.video_response['items'][0]['statistics']['viewCount']
        self.like_video = self.video_response['items'][0]['statistics']['likeCount']

    def __str__(self):
        """
        Возвращает название видео
        """
        return self.title_video


class PLVideo(Video):
    """
    Класс для плей-листа.
    Принимает аргументы:
       self.id_video - id видео,
       self.id_playlist - id плей-листа.
    Наследует свойства:
       self.video_response - статистика видео,
       self.title_video - название видео,
       self.url_video - ссылка на видео,
       self.views_video - количество просмотров,
       self.like_video - количество лайков.
    """

    # Специальный объект для работы с API
    youtube = build('youtube', 'v3', developerKey=api_key)

    def __init__(self, id_video, id_playlist):
        """
        Экземпляр инициализируется по id видео и плей-листа.
        """
        super().__init__(id_video)
        self.id_playlist = id_playlist
