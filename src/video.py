import os

from googleapiclient.discovery import build

api_key: str = os.getenv('YT_API_KEY')


class VideoIdNonexistent(Exception):
    """
    Класс исключения при получении несуществующего id в классе 'Video'.
    """

    def __init__(self, *args, **kwargs):
        self.message = args[0] if args else 'Несуществующий id'


class Video:
    """
    Класс для ютуб-видео.
    Принимает аргументы:
        self.id_video - id видео.
    Определяет свойства:
        self.video_response - статистика видео,
        self.title - название видео,
        self.url_video - ссылка на видео,
        self.views_video - количество просмотров,
        self.like_count - количество лайков.
    """

    # Специальный объект для работы с API
    youtube = build('youtube', 'v3', developerKey=api_key)

    def __init__(self, id_video):
        """
        Экземпляр инициализируется по id видео.
        """

        self.id_video = id_video

        try:
            self.video_response = Video.youtube.videos().list(part='snippet,statistics,contentDetails,topicDetails',
                                                              id=id_video).execute()
            self.title = self.video_response['items'][0]['snippet']['title']
            self.url_video = f'https://www.youtube.com/watch?v={self.id_video}'
            self.views_video = self.video_response['items'][0]['statistics']['viewCount']
            self.like_count = self.video_response['items'][0]['statistics']['likeCount']
        except:
            self.video_response = None
            self.title = None
            self.url_video = None
            self.views_video = None
            self.like_count = None

            print(VideoIdNonexistent().message)

    def __str__(self):
        """
        Возвращает название видео
        """
        return self.title


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
