from rest_framework import serializers
from .models import ShortURL
from django.utils import timezone


class ShortURLStatsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShortURL
        fields = ['short_code', 'original_url', 'click_count']


class ShortURLSerializer(serializers.ModelSerializer):
    full_short_url = serializers.SerializerMethodField()
    expires_at = serializers.DateTimeField(
        format="%Y-%m-%d %H:%M:%S", required=False
    )
    last_visited_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False)

    class Meta:
        model = ShortURL
        fields = [
            'original_url',
            'short_code',
            'full_short_url',
            'expires_at',
            'is_active',
            'click_count',
            'last_visited_at',
        ]
        read_only_fields = [
            'short_code',
            'full_short_url',
            'click_count',
            'last_visited_at',
        ]

    def get_full_short_url(self, obj):
        request = self.context.get('request')
        return request.build_absolute_uri(f'/api/code/{obj.short_code}')

    def create(self, validated_data):
        validated_data.setdefault(
            "expires_at", timezone.now() + timezone.timedelta(days=1)
        )
        return super().create(validated_data)
