from datetime import timedelta

from albums.models.album import Album
from artists.models import Artist
from django.db.models import Count
from django.db.models.functions import TruncMonth
from django.utils import timezone
from rest_framework import status
from songs.models import Song
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

    def get_monthly_songs(self):
        try:
            monthly_songs = (
                Song.objects.annotate(month=TruncMonth("release_date"))
                .values("month")
                .annotate(song_count=Count("id"))
                .order_by("month")
            )

            month_names = [
                "Jan",
                "Feb",
                "Mar",
                "Apr",
                "May",
                "Jun",
                "Jul",
                "Aug",
                "Sep",
                "Oct",
                "Nov",
                "Dec",
            ]

            data = [
                {
                    "month": month_names[month["month"].month - 1],
                    "songs": month["song_count"],
                }
                for month in monthly_songs
            ]

            return success_response(
                data,
                message="Monthly songs retrieved successfully",
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            return error_response(
                error=str(e),
                message="Failed to retrieve monthly songs",
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def get_manager_monthly_songs(self, manager_id):
        try:
            managed_artists = Artist.objects.filter(manager_id=manager_id)

            monthly_songs = (
                Song.objects.filter(album__artist__in=managed_artists)
                .annotate(month=TruncMonth("release_date"))
                .values("month")
                .annotate(song_count=Count("id"))
                .order_by("month")
            )

            month_names = [
                "Jan",
                "Feb",
                "Mar",
                "Apr",
                "May",
                "Jun",
                "Jul",
                "Aug",
                "Sep",
                "Oct",
                "Nov",
                "Dec",
            ]

            data = [
                {
                    "month": month_names[month["month"].month - 1],
                    "songs": month["song_count"],
                }
                for month in monthly_songs
            ]

            return success_response(
                data,
                message="Manager's monthly songs retrieved successfully",
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            return error_response(
                error=str(e),
                message="Failed to retrieve manager's monthly songs",
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
