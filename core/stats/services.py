from datetime import timedelta

from albums.models.album import Album
from artists.models import Artist
from django.db.models import Count, F
from django.utils import timezone
from rest_framework import status
from songs.models import Song
from songs.serializers import SongOutputSerializer
from users.models.user import CustomUser as User

from core.utils.response import error_response, success_response


class StatService:
    def get_manager_stats(self, id):
        try:
            now = timezone.now()
            one_week_ago = now - timedelta(days=7)
            two_weeks_ago = now - timedelta(days=14)

            artists = Artist.objects.filter(manager=id)
            albums = Album.objects.filter(artist__in=artists)
            songs = Song.objects.filter(album__in=albums)

            artists_last_week = artists.filter(created_at__gte=one_week_ago).count()
            artists_prev_week = artists.filter(
                created_at__gte=two_weeks_ago, created_at__lt=one_week_ago
            ).count()

            albums_last_week = albums.filter(created_at__gte=one_week_ago).count()
            albums_prev_week = albums.filter(
                created_at__gte=two_weeks_ago, created_at__lt=one_week_ago
            ).count()

            songs_last_week = songs.filter(created_at__gte=one_week_ago).count()
            songs_prev_week = songs.filter(
                created_at__gte=two_weeks_ago, created_at__lt=one_week_ago
            ).count()

            stats = {
                "total_artists": artists.count(),
                "artist_diff": artists_last_week - artists_prev_week,
                "total_albums": albums.count(),
                "album_diff": albums_last_week - albums_prev_week,
                "total_songs": songs.count(),
                "song_diff": songs_last_week - songs_prev_week,
                "total_genres": songs.values("genre").distinct().count(),
            }

            return success_response(
                stats,
                message="Stats retrieved successfully",
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            return error_response(
                error=str(e),
                message="Failed to retrieve manager stats",
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def get_all_stats(self):
        try:
            now = timezone.now()
            one_week_ago = now - timedelta(days=7)
            two_weeks_ago = now - timedelta(days=14)

            # Totals
            artists = Artist.objects.all()
            albums = Album.objects.all()
            songs = Song.objects.all()
            managers = User.objects.filter(role="artist_manager")

            # Weekly additions
            artists_last_week = artists.filter(created_at__gte=one_week_ago).count()
            artists_prev_week = artists.filter(
                created_at__gte=two_weeks_ago, created_at__lt=one_week_ago
            ).count()

            albums_last_week = albums.filter(created_at__gte=one_week_ago).count()
            albums_prev_week = albums.filter(
                created_at__gte=two_weeks_ago, created_at__lt=one_week_ago
            ).count()

            songs_last_week = songs.filter(created_at__gte=one_week_ago).count()
            songs_prev_week = songs.filter(
                created_at__gte=two_weeks_ago, created_at__lt=one_week_ago
            ).count()

            managers_last_week = managers.filter(date_joined__gte=one_week_ago).count()
            managers_prev_week = managers.filter(
                date_joined__gte=two_weeks_ago, date_joined__lt=one_week_ago
            ).count()

            stats = {
                "total_artists": artists.count(),
                "artist_diff": artists_last_week - artists_prev_week,
                "total_albums": albums.count(),
                "album_diff": albums_last_week - albums_prev_week,
                "total_songs": songs.count(),
                "song_diff": songs_last_week - songs_prev_week,
                "total_managers": managers.count(),
                "manager_diff": managers_last_week - managers_prev_week,
            }

            return success_response(
                stats,
                message="All stats retrieved successfully",
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            return error_response(
                error=str(e),
                message="Failed to retrieve all stats",
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def get_manager_genre(self, manager_id):
        artists = Artist.objects.filter(manager=manager_id).values_list("id", flat=True)

        stats = (
            Song.objects.filter(album__artist__in=artists)
            .values("genre")
            .annotate(values=Count("genre"))
        )

        return success_response(
            stats,
            message="Manager genre stats retrieved successfully",
            status=status.HTTP_200_OK,
        )

    def get_all_genre(self):
        stats = Song.objects.all().values("genre").annotate(values=Count("genre"))

        return success_response(
            stats,
            message="All genre stats retrieved successfully",
            status=status.HTTP_200_OK,
        )

    def get_manager_artist_songs(self, manager_id):
        stats = (
            Song.objects.filter(album__artist__manager=manager_id)
            .values(artist=F("album__artist__name"))
            .annotate(songs=Count("id"))
        )
        return success_response(
            stats,
            message="All genre stats retrieved successfully",
            status=status.HTTP_200_OK,
        )

    def get_all_artist_songs(self):
        stats = Song.objects.values(artist=F("album__artist__name")).annotate(
            songs=Count("id")
        )

        return success_response(
            stats,
            message="All genre stats retrieved successfully",
            status=status.HTTP_200_OK,
        )

    def get_manager_artist_albums(self, manager_id):
        stats = (
            Album.objects.filter(artist__manager=manager_id)
            .values(artist_name=F("artist__name"))
            .annotate(albums=Count("id"))
        )

        return success_response(
            stats,
            message="All genre stats retrieved successfully",
            status=status.HTTP_200_OK,
        )

    def get_all_artist_albums(self):
        stats = Album.objects.values(artist_name=F("artist__name")).annotate(
            albums=Count("id")
        )

        return success_response(
            stats,
            message="Albums per artist retrieved successfully",
            status=status.HTTP_200_OK,
        )

    def get_manager_recent_songs(self, manager_id):
        one_week = timezone.now() - timedelta(days=7)
        songs = (
            Song.objects.filter(created_at__gte=one_week)
            .select_related("album")
            .filter(album__artist__manager=manager_id)
            .prefetch_related("album__artist")
            .order_by("-created_at")[:5]
        )
        serializer = SongOutputSerializer(songs, many=True)
        stats = serializer.data

        return success_response(
            stats,
            message="Manager recent songs retrieved successfully",
            status=status.HTTP_200_OK,
        )

    def get_all_recent_songs(self):
        one_week = timezone.now() - timedelta(days=7)
        songs = (
            Song.objects.filter(created_at__gte=one_week)
            .select_related("album")
            .prefetch_related("album__artist")
            .order_by("-created_at")[:5]
        )
        serializer = SongOutputSerializer(songs, many=True)
        stats = serializer.data
        return success_response(
            stats,
            message="Recent songs retrieved successfully",
            status=status.HTTP_200_OK,
        )
