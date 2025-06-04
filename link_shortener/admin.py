from unfold.admin import ModelAdmin
from unfold.decorators import display
from django.utils.html import format_html
from django.utils import timezone
from django.contrib import admin

from link_shortener.models import ShortURL


class ExpiredFilter(admin.SimpleListFilter):
    title = 'Expired'
    parameter_name = 'is_expired'

    def lookups(self, request, model_admin):
        return [
            ('yes', 'Expired'),
            ('no', 'Not expired'),
        ]

    def queryset(self, request, queryset):
        now = timezone.now()
        if self.value() == 'yes':
            return queryset.filter(expires_at__lt=now)
        if self.value() == 'no':
            return queryset.filter(expires_at__gte=now)
        return queryset


@admin.register(ShortURL)
class ShortURLAdmin(ModelAdmin):
    list_display = (
        'short_code', 'original_url', 'render_short_url',
        'is_active', 'render_is_expired',
        'click_count', 'created_at', 'expires_at', 'last_visited_at',
    )
    list_filter = ('is_active', ExpiredFilter)

    @display(description="Expired", boolean=True)
    def render_is_expired(self, obj):
        return obj.is_expired()

    @display(description="Short URL")
    def render_short_url(self, obj):
        return format_html(
            '<a href="/api/code/{code}" target="_blank">/api/code/{code}</a>',
            code=obj.short_code
        )
