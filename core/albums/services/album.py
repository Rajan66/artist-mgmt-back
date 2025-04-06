import uuid

from albums.models.album import Album
from albums.selectors import fetch_album, fetch_albums
from albums.serializers.album import (
    AlbumFetchSerializer,
    AlbumOutputSerializer,
)
from artists.selectors import fetch_artist
from artists.serializers import AlbumArtistSerializer
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.db import DatabaseError, connection, transaction
from django.utils import timezone
from rest_framework import status
from songs.models import Song

from core.utils.exceptions import CustomAPIException
from core.utils.response import error_response, success_response


class AlbumService:
    def get_albums(self):
        try:
            albums_dicts = fetch_albums()
            if albums_dicts == []:
                return success_response(
                    message="Albums retrieved successfully",
                    status=status.HTTP_200_OK,
                )

            for album in albums_dicts:
                artist_id = album.get("artist_id")
                artist_dict = fetch_artist(id=artist_id)

                # user_dict = fetch_user(artist_dict)
                # serializer = UserOutputSerializer(user_dict)
                # artist_dict["user"] = serializer.data

                serializer = AlbumArtistSerializer(artist_dict)
                album["artist"] = serializer.data

            serializer = AlbumOutputSerializer(albums_dicts, many=True)
            albums = serializer.data

        except Exception as e:
            return error_response(
                error=str(e),
                message="Failed to fetch albums",
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        return success_response(
            data=albums,
            message="Albums retrieved successfully",
            status=status.HTTP_200_OK,
        )

    def get_album(self, album_id):
        try:
            album_dict = fetch_album(id=album_id)

            artist_id = album_dict.get("artist_id")
            artist_dict = fetch_artist(id=artist_id)

            # user_dict = fetch_user(artist_dict)
            # serializer = UserOutputSerializer(user_dict)
            # artist_dict["user"] = serializer.data

            serializer = AlbumArtistSerializer(artist_dict)
            album_dict["artist"] = serializer.data

            serializer = AlbumOutputSerializer(album_dict)
            albums = serializer.data

        except Exception as e:
            return error_response(
                error=str(e),
                message="Failed to fetch albums",
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        return success_response(
            data=albums,
            message="Albums retrieved successfully",
            status=status.HTTP_200_OK,
        )

    def get_artist_albums(self, id):
        try:
            filtered_albums = Album.objects.filter(artist=id)

            serializer = AlbumOutputSerializer(filtered_albums, many=True)
            albums = serializer.data

        except Exception as e:
            return error_response(
                error=str(e),
                message="Failed to fetch albums",
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        return success_response(
            data=albums,
            message="Albums retrieved successfully",
            status=status.HTTP_200_OK,
        )

    def create(self, payload):
        try:
            with connection.cursor() as c:
                id = uuid.uuid4()
                title = payload.get("title")
                artist_id = payload.get("artist")
                cover_image_file = payload.get("cover_image")
                total_tracks = payload.get("total_tracks", 0)
                release_date = payload.get("release_date")
                album_type = payload.get("album_type", "single")
                created_at = timezone.now()
                updated_at = timezone.now()

                try:
                    uuid.UUID(artist_id, version=4)
                except ValueError:
                    raise CustomAPIException(
                        detail="The provided artist ID is not a valid UUID v4",
                        code=status.HTTP_400_BAD_REQUEST,
                    )

                c.execute("SELECT name FROM artists_artist WHERE id=%s", [artist_id])
                result = c.fetchone()
                if not result:
                    raise ValueError("Invalid artist ID")

                cover_image_path = None
                if (
                    cover_image_file
                    and cover_image_file != {}
                    and cover_image_file != ""
                ):
                    filename = f"albums/{str(id).split('-')[0]}_{cover_image_file.name}"
                    cover_image_path = default_storage.save(
                        filename, ContentFile(cover_image_file.read())
                    )

                c.execute(
                    """INSERT INTO albums_album (id, title, artist_id, cover_image, total_tracks, release_date, album_type, created_at, updated_at) values
                    (%s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING *;""",
                    [
                        id,
                        title,
                        artist_id,
                        cover_image_path,
                        total_tracks,
                        release_date,
                        album_type,
                        created_at,
                        updated_at,
                    ],
                )

                result = c.fetchone()
                columns = [col[0] for col in c.description]

            album_dict = dict(zip(columns, result))

            artist_dict = fetch_artist(id=artist_id)
            artist_serializer = AlbumArtistSerializer(artist_dict)
            album_dict["artist"] = artist_serializer.data

            album_serializer = AlbumFetchSerializer(album_dict)
            album = album_serializer.data

        except ValueError as e:
            raise CustomAPIException(
                error=str(e),
                detail="Invalid ID",
                code=status.HTTP_400_BAD_REQUEST,
            )

        except Exception as e:
            raise CustomAPIException(
                error=str(e),
                detail="Something went wrong while creating an album",
                code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        return success_response(
            data=album,
            message="Album created successfully",
            status=status.HTTP_200_OK,
        )

    def update(self, payload, album_id):
        song_count = Song.objects.filter(album=album_id).count()
        try:
            with connection.cursor() as c:
                old_dict = fetch_album(id=album_id)
                serializer = AlbumFetchSerializer(old_dict)
                old_album = serializer.data

                id = old_album.get("id")
                title = payload.get("title", old_album.get("title"))
                artist_id = payload.get("artist", old_album.get("artist_id"))
                cover_image_file = payload.get("cover_image")
                cover_image_path = old_album.get("cover_image")
                total_tracks = payload.get(
                    "total_tracks", old_album.get("total_tracks")
                )
                release_date = payload.get(
                    "release_date", old_album.get("release_date")
                )
                album_type = payload.get("album_type", old_album.get("album_type"))
                created_at = old_album.get("created_at")
                updated_at = timezone.now()
                print(cover_image_file)
                print(cover_image_path)
                try:
                    uuid.UUID(artist_id, version=4)
                except ValueError:
                    raise CustomAPIException(
                        detail="The provided artist ID is not a valid UUID v4",
                        code=status.HTTP_400_BAD_REQUEST,
                    )

                c.execute(
                    "SELECT name FROM artists_artist WHERE id=%s",
                    [artist_id],
                )
                result = c.fetchone()
                if not result:
                    raise ValueError("Invalid artist ID")

                if (
                    cover_image_file
                    and cover_image_file != {}
                    and cover_image_file != ""
                    and cover_image_file != "undefined"
                ):
                    cover_image_path = None
                    filename = f"albums/{str(id).split('-')[0]}_{cover_image_file.name}"
                    cover_image_path = default_storage.save(
                        filename, ContentFile(cover_image_file.read())
                    )

                if song_count == 1 or song_count == 0:
                    album_type = "single"
                    total_tracks = song_count
                elif song_count > 1 and song_count < 5:
                    album_type = "ep"
                    total_tracks = song_count

                elif song_count > 4:
                    album_type = "album"
                    total_tracks = song_count

                c.execute(
                    """UPDATE albums_album SET title=%s, artist_id=%s, cover_image=%s, total_tracks=%s, release_date=%s, album_type=%s, created_at=%s, updated_at=%s
                         WHERE id=%s RETURNING *;
                    """,
                    [
                        title,
                        artist_id,
                        cover_image_path,
                        total_tracks,
                        release_date,
                        album_type,
                        created_at,
                        updated_at,
                        id,
                    ],
                )

                result = c.fetchone()
                columns = []
                for col in c.description:
                    columns.append(col[0])

            album_dict = dict(zip(columns, result))

            # artist_dict = fetch_artist(id=artist_id)
            # serializer = AlbumArtistSerializer(artist_dict)
            album_dict["artist"] = album_dict.get("artist_id")
            print(album_dict)

            serializer = AlbumFetchSerializer(album_dict)
            album = serializer.data

        except ValueError as e:
            raise CustomAPIException(
                error=str(e),
                detail="Invalid ID",
                code=status.HTTP_400_BAD_REQUEST,
            )

        except Exception as e:
            raise CustomAPIException(
                error=str(e),
                detail="Something went wrong while creating an album",
                code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
        return success_response(
            data=album,
            message="Album created successfully",
            status=status.HTTP_200_OK,
        )

    def delete(self, id):
        try:
            with transaction.atomic():
                with connection.cursor() as c:
                    c.execute(
                        "DELETE FROM songs_song WHERE album_id=%s RETURNING TRUE",
                        [id],
                    )
                    c.execute(
                        "DELETE FROM albums_album WHERE id=%s RETURNING TRUE;",
                        [id],
                    )
                    result = c.fetchone()

                    if not result:
                        return error_response(
                            error="Invalid album ID",
                            message="Album does not exist",
                            status=status.HTTP_404_NOT_FOUND,
                        )

            return success_response(
                message="Album deleted successfully",
                status=status.HTTP_204_NO_CONTENT,
            )

        except DatabaseError as e:
            return error_response(
                error=str(e),
                message="Database error",
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def get_manager_albums(self, manager_id):
        try:
            filtered_albums = Album.objects.filter(
                artist__manager=manager_id
            ).prefetch_related("artist")

            albums = AlbumOutputSerializer(filtered_albums, many=True).data

            return success_response(
                data=albums,
                message="Albums retrieved successfully",
                status=status.HTTP_200_OK,
            )

        except Exception as e:
            return error_response(
                error=str(e),
                message="Failed to fetch albums",
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
