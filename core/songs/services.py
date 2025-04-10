import uuid

from albums.models.album import Album
from albums.selectors import check_album
from django.db import DatabaseError, connection
from django.utils import timezone
from rest_framework import status

from core.utils.response import error_response, success_response
from songs.models import Song
from songs.selectors import (
    fetch_album_songs,
    fetch_song,
    fetch_songs,
)
from songs.serializers import SongOutputSerializer, SongSerializer
from songs.validators import validate_release


class SongService:
    def get_songs(self, request):
        try:
            songs_dicts = fetch_songs()
            serializer = SongOutputSerializer(songs_dicts, many=True)
            songs = serializer.data

        except Exception as e:
            return error_response(
                error=str(e),
                message="Failed to fetch songs",
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        return success_response(
            data=songs,
            message="Songs retrieved successfully",
            status=status.HTTP_200_OK,
            request=request,
        )

    def get_song(self, id):
        try:
            song_dict = fetch_song(id=id)
            serializer = SongSerializer(song_dict)
            song = serializer.data

        except Exception as e:
            return error_response(
                error=str(e),
                message="Failed to fetch song",
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        return success_response(
            data=song,
            message="Song retrieved successfully",
            status=status.HTTP_200_OK,
        )

    def get_album_songs(self, album_id, request):
        try:
            songs_dicts = fetch_album_songs(album_id=album_id)
            serializer = SongSerializer(songs_dicts, many=True)
            songs = serializer.data

        except Exception as e:
            return error_response(
                error=str(e),
                message="Failed to fetch album's songs",
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        return success_response(
            data=songs,
            message="Songs retrieved successfully",
            status=status.HTTP_200_OK,
            request=request,
        )

    def get_artist_songs(self, artist_id, request):
        try:
            filtered_songs = Song.objects.prefetch_related("album__artist").filter(
                album__artist__id=artist_id
            )
            serializer = SongOutputSerializer(filtered_songs, many=True)
            songs = serializer.data

        except Exception as e:
            return error_response(
                error=str(e),
                message="Failed to fetch song",
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        return success_response(
            data=songs,
            message="Song retrieved successfully",
            status=status.HTTP_200_OK,
            request=request,
        )

    def create(self, payload):
        try:
            with connection.cursor() as c:
                id = uuid.uuid4()
                title = payload.get("title")
                album_id = payload.get("album_id")
                release_date = payload.get("release_date")
                genre = payload.get("genre")
                created_at = timezone.now()
                updated_at = timezone.now()

                check_album(id=album_id)
                validate_release(album_id, release_date)

                c.execute(
                    """INSERT INTO songs_song (id, title, album_id, release_date, genre, created_at, updated_at) values
                    (%s, %s, %s, %s, %s, %s, %s) RETURNING *;
                """,
                    [
                        id,
                        title,
                        album_id,
                        release_date,
                        genre,
                        created_at,
                        updated_at,
                    ],
                )

                result = c.fetchone()
                columns = [col[0] for col in c.description]

                song_dicts = dict(zip(columns, result))

                # Django model expects 'album'
                if "album_id" in song_dicts:
                    song_dicts["album"] = song_dicts.pop("album_id")

                serializer = SongSerializer(song_dicts)
                song = serializer.data

                album = Album.objects.get(id=album_id)
                song_count = Song.objects.filter(album=album.id).count()

                if song_count == 1 or song_count == 0:
                    album.album_type = "single"
                    album.total_tracks = song_count

                elif song_count > 1 and song_count < 5:
                    album.album_type = "ep"
                    album.total_tracks = song_count

                elif song_count > 4:
                    album.album_type = "album"
                    album.total_tracks = song_count

                album.save()

                return success_response(
                    data=song,
                    message="Song created successfully",
                    status=status.HTTP_201_CREATED,
                )

        except Exception as e:
            return error_response(
                error=str(e),
                message="Failed to fetch song",
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def update(self, payload, id):
        try:
            with connection.cursor() as c:
                song_dicts = fetch_song(id=id)
                if "album_id" in song_dicts:
                    song_dicts["album"] = song_dicts.pop("album_id")

                serializer = SongSerializer(song_dicts)
                old_song = serializer.data

                id = old_song.get("id")
                title = payload.get("title", old_song.get("title"))
                album_id = payload.get("album_id", old_song.get("album_id"))
                release_date = payload.get("release_date", old_song.get("release_date"))
                genre = payload.get("genre", old_song.get("genre"))
                created_at = old_song.get("created_at")
                updated_at = timezone.now()

                check_album(id=album_id)

                c.execute(
                    """UPDATE songs_song SET title=%s, album_id=%s, release_date=%s, genre=%s,created_at=%s, updated_at=%s
                    WHERE id=%s RETURNING *;
                """,
                    [
                        title,
                        album_id,
                        release_date,
                        genre,
                        created_at,
                        updated_at,
                        id,
                    ],
                )

                result = c.fetchone()
                columns = [col[0] for col in c.description]

                song_dicts = dict(zip(columns, result))

                if "album_id" in song_dicts:
                    song_dicts["album"] = song_dicts.pop("album_id")

                serializer = SongSerializer(song_dicts)
                song = serializer.data

                return success_response(
                    data=song,
                    message="Song updated successfully",
                    status=status.HTTP_200_OK,
                )

        except Exception as e:
            return error_response(
                error=str(e),
                message="Failed to update song",
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def delete(self, id):
        try:
            song = Song.objects.get(id=id)
            album = Album.objects.get(id=song.album.id)

            with connection.cursor() as c:
                c.execute(
                    "DELETE FROM songs_song WHERE id=%s RETURNING TRUE;",
                    [id],
                )
                result = c.fetchone()

                if not result:
                    return error_response(
                        error="Invalid song ID",
                        message="Album does not exist",
                        status=status.HTTP_404_NOT_FOUND,
                    )
            song_count = Song.objects.filter(album=album.id).count()

            if song_count == 1 or song_count == 0:
                album.album_type = "single"
                album.total_tracks = song_count

            elif song_count > 1 and song_count < 5:
                album.album_type = "ep"
                album.total_tracks = song_count

            elif song_count > 4:
                album.album_type = "album"
                album.total_tracks = song_count

            album.save()

            return success_response(
                message="Song deleted successfully",
                status=status.HTTP_204_NO_CONTENT,
            )

        except DatabaseError as e:
            return error_response(
                error=str(e),
                message="Database error",
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def get_manager_songs(self, manager_id, request):
        try:
            filtered_songs = Song.objects.prefetch_related("album__artist").filter(
                album__artist__manager_id=manager_id
            )

            songs = SongOutputSerializer(filtered_songs, many=True).data

            return success_response(
                data=songs,
                message="Songs retrieved successfully",
                status=status.HTTP_200_OK,
                request=request,
            )

        except Exception as e:
            return error_response(
                error=str(e),
                message="Failed to fetch songs",
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                request=request,
            )
