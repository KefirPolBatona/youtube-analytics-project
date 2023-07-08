import os
import isodate

from datetime import timedelta
from googleapiclient.discovery import build

api_key: str = os.getenv('YT_API_KEY')


class PlayList:
    """
    Класс для плейлиста.

    Принимает id плейлиста.

    Определяет аргументы:
        self.playlist_response - информация о плейлисте,
        self.title - название плейлиста,
        self.url - вэб-ссылка на плейлист,
        self.playlist_videos - данные по видеороликам в плейлисте,
        self.video_ids - список id всех видеороликов из плейлиста,
        self.video_response - список видеороликов из плейлиста со статистикой.
    """

    # Специальный объект для работы с API
    youtube = build('youtube', 'v3', developerKey=api_key)

    def __init__(self, playlist_id):
        """
        Экземпляр инициализируется по id плейлиста.
        """

        self.playlist_id = playlist_id
        self.playlist_response = PlayList.youtube.playlists().list(part='snippet', id=playlist_id).execute()

        self.title = self.playlist_response['items'][0]['snippet']['title']
        self.url = f'https://www.youtube.com/playlist?list={self.playlist_id}'

        self.playlist_videos = PlayList.youtube.playlistItems().list(playlistId=self.playlist_id, part='contentDetails',
                                                                     maxResults=50).execute()
        self.video_ids: list[str] = [video['contentDetails']['videoId'] for video in self.playlist_videos['items']]
        self.video_response = PlayList.youtube.videos().list(part='contentDetails,statistics',
                                                             id=','.join(self.video_ids)).execute()

    @property
    def total_duration(self):
        """
        Возвращает сумму длительности всех видеороликов из плейлиста.
        """

        playlist_timedelta = timedelta(0, 0, 0)

        for video in self.video_response['items']:
            # YouTube video duration is in ISO 8601 format
            iso_8601_duration = video['contentDetails']['duration']
            duration = isodate.parse_duration(iso_8601_duration)
            playlist_timedelta += duration
        return playlist_timedelta

    def show_best_video(self):
        """
        Возвращает ссылку на самое популярное видео из плейлиста (по количеству лайков)
        """

        video_id = ""
        video_like_count = 0

        for video in self.video_response['items']:
            if int(video["statistics"]["likeCount"]) > video_like_count:
                video_id = video["id"]
            continue
        return f"https://youtu.be/{video_id}"
