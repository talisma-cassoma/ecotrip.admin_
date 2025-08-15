from django.contrib import admin
from django.db.models import Count, Sum
from django.utils import timezone
from .models import (
    User, UserRefreshToken, Driver, Trip, TripCancellation,
    Place, Coord, Point, Role, DriverStatus, TripStatus
)

# ==== CONFIGURAÇÃO DE USER ====
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "role", "telephone", "created_at")
    list_filter = ("role", "created_at")
    search_fields = ("name", "email")

    # Permite o controle de edição/exclusão por grupo
    def has_add_permission(self, request):
        return request.user.is_superuser or request.user.has_perm("app.add_user")
    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser or request.user.has_perm("app.change_user")
    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser or request.user.has_perm("app.delete_user")


# ==== DRIVER ====
@admin.register(Driver)
class DriverAdmin(admin.ModelAdmin):
    list_display = ("user", "car_model", "car_plate", "status", "rating", "completed_rides", "created_at")
    list_filter = ("status", "created_at", "rating")
    search_fields = ("user__name", "car_plate")

    def has_add_permission(self, request):
        return request.user.is_superuser or request.user.has_perm("app.add_driver")
    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser or request.user.has_perm("app.change_driver")
    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser or request.user.has_perm("app.delete_driver")


# ==== TRIP ====
@admin.register(Trip)
class TripAdmin(admin.ModelAdmin):
    list_display = ("token", "status", "passenger", "driver", "freight", "created_at")
    list_filter = ("status", "created_at")
    search_fields = ("token", "passenger__name", "driver__user__name")

    def changelist_view(self, request, extra_context=None):
        """
        Adiciona métricas ao contexto da lista de viagens
        """
        extra_context = extra_context or {}
        today = timezone.now().date()

        extra_context["total_deliveries"] = Trip.objects.filter(status=TripStatus.COMPLETED).count()
        extra_context["total_income"] = Trip.objects.filter(status=TripStatus.COMPLETED).aggregate(Sum("freight"))["freight__sum"] or 0
        extra_context["total_request_accepted"] = Trip.objects.filter(status=TripStatus.ACCEPTED).count()
        extra_context["total_vehicles_active"] = Driver.objects.filter(status=DriverStatus.AVAILABLE).count()
        extra_context["total_canceled_deliveries"] = Trip.objects.filter(status=TripStatus.CANCELLED).count()
        extra_context["canceled_by_drivers"] = TripCancellation.objects.filter(cancelled_by=Role.DRIVER).count()
        extra_context["canceled_by_passengers"] = TripCancellation.objects.filter(cancelled_by=Role.PASSENGER).count()
        extra_context["new_drivers_today"] = Driver.objects.filter(created_at__date=today).count()
        extra_context["new_passengers_today"] = User.objects.filter(role=Role.PASSENGER, created_at__date=today).count()
        extra_context["top_rated_drivers"] = Driver.objects.order_by("-rating")[:5]

        return super().changelist_view(request, extra_context=extra_context)

    def has_add_permission(self, request):
        return request.user.is_superuser or request.user.has_perm("app.add_trip")
    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser or request.user.has_perm("app.change_trip")
    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser or request.user.has_perm("app.delete_trip")


# ==== TRIP CANCELLATION ====
@admin.register(TripCancellation)
class TripCancellationAdmin(admin.ModelAdmin):
    list_display = ("trip", "cancelled_by", "user", "created_at")
    list_filter = ("cancelled_by", "created_at")
    search_fields = ("trip__token", "user__name")

    def has_add_permission(self, request):
        return request.user.is_superuser or request.user.has_perm("app.add_tripcancellation")
    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser or request.user.has_perm("app.change_tripcancellation")
    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser or request.user.has_perm("app.delete_tripcancellation")


# ==== OUTROS MODELS ====
@admin.register(UserRefreshToken)
class UserRefreshTokenAdmin(admin.ModelAdmin):
    list_display = ("user", "token", "is_revoked", "created_at", "expires_at")
    list_filter = ("is_revoked",)

@admin.register(Place)
class PlaceAdmin(admin.ModelAdmin):
    list_display = ("name", "location")

@admin.register(Coord)
class CoordAdmin(admin.ModelAdmin):
    list_display = ("lat", "lng")

@admin.register(Point)
class PointAdmin(admin.ModelAdmin):
    list_display = ("driver", "location", "created_at")
