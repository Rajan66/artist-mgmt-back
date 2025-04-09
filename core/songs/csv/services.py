import csv
from io import TextIOWrapper

from albums.models.album import Album
from artists.models import Artist
from django.http import HttpResponse, JsonResponse
from rest_framework import status
from songs.models import Song
from songs.validators import validate_release

from core.utils.response import error_response, success_response


class CSVService:
    def admin_export(self, request):
        songs = (
            Song.objects.select_related("album")
            .select_related("album__artist")
            .select_related("album__artist__user")
        )

        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = 'attachment; filename="all_songs.csv"'
        writer = csv.writer(response)

        writer.writerow(
            [
                "Song Title",
                "Genre",
                "Song Release Date",
                "Album Title",
                "Album Type",
                "Artist Name",
                "Artist Email",
            ]
        )

        for song in songs:
            writer.writerow(
                [
                    song.title,
                    song.genre,
                    song.release_date,
                    song.album.title,
                    song.album.album_type,
                    song.album.artist.name,
                    song.album.artist.user.email,
                ]
            )

        return response

    def manager_export(self, request, manager_id):
        songs = (
            Song.objects.select_related("album")
            .select_related("album__artist")
            .select_related("album__artist__user")
            .filter(album__artist__manager__id=manager_id)
        )

        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = 'attachment; filename="manager_songs.csv"'
        writer = csv.writer(response)

        writer.writerow(
            [
                "Song Title",
                "Genre",
                "Song Release Date",
                "Album Title",
                "Album Type",
                "Artist Name",
                "Artist Email",
            ]
        )

        for song in songs:
            writer.writerow(
                [
                    song.title,
                    song.genre,
                    song.release_date,
                    song.album.title,
                    song.album.album_type,
                    song.album.artist.name,
                    song.album.artist.user.email,
                ]
            )

        return response

    def artist_export(self, request, user_id):
        songs = (
            Song.objects.select_related("album")
            .select_related("album__artist")
            .select_related("album__artist__user")
            .filter(album__artist__user__id=user_id)
        )

        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = 'attachment; filename="artist_songs.csv"'
        writer = csv.writer(response)

        writer.writerow(
            [
                "Song Title",
                "Genre",
                "Song Release Date",
                "Album Title",
                "Album Type",
                "Artist Name",
                "Artist Email",
            ]
        )

        for song in songs:
            writer.writerow(
                [
                    song.title,
                    song.genre,
                    song.release_date,
                    song.album.title,
                    song.album.album_type,
                    song.album.artist.name,
                    song.album.artist.user.email,
                ]
            )

        return response

    def admin_import(self, request):
        file = request.FILES.get("file")
        if not file:
            return JsonResponse({"error": "No file provided"}, status=400)

        file = TextIOWrapper(file.file, encoding="utf-8")
        csv_reader = csv.DictReader(file)

        error_messages = []
        for row in csv_reader:
            try:
                song_title = row.get("Song Title")
                genre = row.get("Genre")
                song_release_date = row.get("Song Release Date")
                album_title = row.get("Album Title")
                artist_email = row.get("Artist Email")

                try:
                    artist = Artist.objects.get(user__email=artist_email)
                except Artist.DoesNotExist:
                    error_messages.append(
                        f"Artist with email {artist_email} not found."
                    )
                    continue

                try:
                    album = Album.objects.get(title=album_title, artist=artist)
                except Album.DoesNotExist:
                    error_messages.append(
                        f"Album '{album_title}' by artist '{artist.name}' not found."
                    )
                    continue

                validate_release(id=album.id, release_date=song_release_date)
                Song.objects.create(
                    title=song_title,
                    genre=genre,
                    release_date=song_release_date,
                    album=album,
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

            except Exception as e:
                error_messages.append(f"Error processing row: {row}. Error: {str(e)}")

        if error_messages:
            return error_response(
                error=error_messages,
                message="CSV Import Error",
                status=status.HTTP_400_BAD_REQUEST,
            )

        return success_response(
            message="CSV import successful", status=status.HTTP_200_OK
        )

    def manager_import(self, request, manager_id):
        file = request.FILES.get("file")
        if not file:
            return JsonResponse({"error": "No file provided"}, status=400)

        file = TextIOWrapper(file.file, encoding="utf-8")
        csv_reader = csv.DictReader(file)

        error_messages = []
        for row in csv_reader:
            try:
                song_title = row.get("Song Title")
                genre = row.get("Genre")
                song_release_date = row.get("Song Release Date")
                album_title = row.get("Album Title")
                artist_email = row.get("Artist Email")

                try:
                    artist = Artist.objects.get(user__email=artist_email)
                except Artist.DoesNotExist:
                    error_messages.append(
                        f"Artist with email {artist_email} not found."
                    )
                    continue

                if str(artist.manager.id) != manager_id:
                    error_messages.append(
                        f"Artist '{artist.name}' is not managed by the manager."
                    )
                    continue

                try:
                    album = Album.objects.get(title=album_title, artist=artist)
                except Album.DoesNotExist:
                    error_messages.append(
                        f"Album '{album_title}' by artist '{artist.name}' not found."
                    )
                    continue

                validate_release(id=album.id, release_date=song_release_date)
                Song.objects.create(
                    title=song_title,
                    genre=genre,
                    release_date=song_release_date,
                    album=album,
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

            except Exception as e:
                error_messages.append(f"Error processing row: {row}. Error: {str(e)}")

        if error_messages:
            return error_response(
                error=error_messages,
                message="CSV Import Error",
                status=status.HTTP_400_BAD_REQUEST,
            )

        return success_response(
            message="CSV import successful", status=status.HTTP_200_OK
        )

    def artist_import(self, request, user_id):
        file = request.FILES.get("file")
        if not file:
            return JsonResponse({"error": "No file provided"}, status=400)

        file = TextIOWrapper(file.file, encoding="utf-8")
        csv_reader = csv.DictReader(file)

        error_messages = []
        for row in csv_reader:
            try:
                song_title = row.get("Song Title")
                genre = row.get("Genre")
                song_release_date = row.get("Song Release Date")
                album_title = row.get("Album Title")

                try:
                    artist = Artist.objects.get(user__id=user_id)
                except Artist.DoesNotExist:
                    error_messages.append(f"Artist with user ID {user_id} not found.")
                    continue

                try:
                    album = Album.objects.get(title=album_title, artist=artist)
                except Album.DoesNotExist:
                    error_messages.append(
                        f"Album '{album_title}' by artist '{artist.name}' not found."
                    )
                    continue

                validate_release(id=album.id, release_date=song_release_date)
                Song.objects.create(
                    title=song_title,
                    genre=genre,
                    release_date=song_release_date,
                    album=album,
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

            except Exception as e:
                error_messages.append(f"Error processing row: {row}. Error: {str(e)}")

        if error_messages:
            return error_response(
                error=error_messages,
                message="CSV Import Error",
                status=status.HTTP_400_BAD_REQUEST,
            )

        return success_response(
            message="CSV import successful", status=status.HTTP_200_OK
        )
