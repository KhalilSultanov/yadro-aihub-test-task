from django.shortcuts import redirect
from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.authentication import BasicAuthentication
from rest_framework.generics import CreateAPIView, get_object_or_404, ListAPIView, UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from link_shortener.models import ShortURL
from link_shortener.serializers import ShortURLSerializer, ShortURLStatsSerializer


class ShortURLStatsView(ListAPIView):
    queryset = ShortURL.objects.order_by('-click_count')
    serializer_class = ShortURLStatsSerializer
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]
    pagination_class = None

    filter_backends = [DjangoFilterBackend]


class ShortURLCreateView(CreateAPIView):
    queryset = ShortURL.objects.all()
    serializer_class = ShortURLSerializer
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]


class ShortURLListView(ListAPIView):
    queryset = ShortURL.objects.all()
    serializer_class = ShortURLSerializer
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]

    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['is_active']


class RedirectView(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request, short_code):
        url = get_object_or_404(ShortURL, short_code=short_code)

        if not url.is_active:
            return Response({"detail": "Link is inactive."}, status=status.HTTP_403_FORBIDDEN)
        elif url.is_expired():
            return Response({"detail": "Link is expired."}, status=status.HTTP_410_GONE)

        url.click_count += 1
        url.last_visited_at = timezone.now()
        url.save(update_fields=['click_count', 'last_visited_at'])

        return redirect(url.original_url)


class ShortURLDeactivateView(UpdateAPIView):
    queryset = ShortURL.objects.all()
    lookup_field = 'short_code'
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def patch(self, request, *args, **kwargs):
        instance = self.get_object()
        if not instance.is_active:
            return Response({'detail': 'Link is already deactivated.'}, status=status.HTTP_400_BAD_REQUEST)
        instance.is_active = False
        instance.save(update_fields=['is_active'])
        return Response({'detail': 'Link successfully deactivated.'}, status=status.HTTP_200_OK)
