from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.utils import swagger_auto_schema
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.generics import RetrieveAPIView, ListAPIView
from rest_framework.permissions import AllowAny

from apps.content.models import News, Article, Banner, KnowledgeBase
from apps.content.serializer import GetNewsSerializer, PostNewsSerializer, GetArticleSerializer, PostArticleSerializer, \
    RetrieveNewsSerializer, GetBannerSerializer, PostBannerSerializer, RetrieveBannerSerializer, \
    BannerMainPageSerializer, NewsMainPageSerializer, GetKnowledgeBaseSerializer, PostKnowledgeBaseSerializer, \
    KnowledgeBaseNewsSerializer, KnowledgeBaseMainPageSerializer
from config.utils.pagination import APIPagination
from config.utils.permissions import LandingPage
from config.views import ModelViewSetPack


class NewsModelViewSet(ModelViewSetPack):
    queryset = News.objects.all()
    serializer_class = GetNewsSerializer
    post_serializer_class = PostNewsSerializer
    permission_classes = (LandingPage,)

    @swagger_auto_schema(request_body=PostNewsSerializer)
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(request_body=PostNewsSerializer)
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)


class NewsRetrieveAPIView(RetrieveAPIView):
    queryset = News.objects.all()
    serializer_class = RetrieveNewsSerializer


class NewsLandingListAPIView(ListAPIView):
    queryset = News.objects.filter(is_draft=False).order_by('-id')[:3]
    serializer_class = NewsMainPageSerializer
    permission_classes = [AllowAny, ]


class NewsPageListAPIView(ListAPIView):
    queryset = News.objects.filter(is_draft=False).order_by('-id')
    serializer_class = NewsMainPageSerializer
    permission_classes = [AllowAny, ]
    pagination_class = APIPagination
    filter_backends = [DjangoFilterBackend, OrderingFilter, ]
    ordering_fields = ['created_at', ]
    # search_fields = ['title_uz', 'title_ru', 'title_en',
    #                  'description_uz', 'description_ru', 'description_en',
    #                  'content_uz', 'content_ru', 'content_en', ]


class NewsLandingRetrieveAPIView(RetrieveAPIView):
    queryset = News.objects.filter(is_draft=False)
    serializer_class = GetNewsSerializer
    permission_classes = [AllowAny, ]


class KnowledgeBaseModelViewSet(ModelViewSetPack):
    queryset = KnowledgeBase.objects.all()
    serializer_class = GetKnowledgeBaseSerializer
    post_serializer_class = PostKnowledgeBaseSerializer
    permission_classes = (LandingPage,)

    @swagger_auto_schema(request_body=PostKnowledgeBaseSerializer)
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(request_body=PostKnowledgeBaseSerializer)
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)


class KnowledgeBaseRetrieveAPIView(RetrieveAPIView):
    queryset = KnowledgeBase.objects.all()
    serializer_class = KnowledgeBaseNewsSerializer


class KnowledgeBasePageListAPIView(ListAPIView):
    queryset = KnowledgeBase.objects.filter(is_draft=False).order_by('-id')
    serializer_class = KnowledgeBaseMainPageSerializer
    permission_classes = [AllowAny, ]
    pagination_class = APIPagination
    filter_backends = [DjangoFilterBackend, OrderingFilter, ]
    ordering_fields = ['created_at', ]
    # search_fields = ['title_uz', 'title_ru', 'title_en',
    #                  'description_uz', 'description_ru', 'description_en',
    #                  'content_uz', 'content_ru', 'content_en', ]


class ArticleModelViewSet(ModelViewSetPack):
    queryset = Article.objects.all()
    serializer_class = GetArticleSerializer
    post_serializer_class = PostArticleSerializer
    permission_classes = (LandingPage,)
    filter_backends = [DjangoFilterBackend, SearchFilter, ]
    search_fields = ['name_uz', 'name_ru', 'name_en', ]

    @swagger_auto_schema(request_body=PostArticleSerializer)
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(request_body=PostArticleSerializer)
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)


class ArticleRetrieveAPIView(RetrieveAPIView):
    queryset = Article.objects.all()
    serializer_class = PostArticleSerializer


class BannerModelViewSet(ModelViewSetPack):
    queryset = Banner.objects.all()
    serializer_class = GetBannerSerializer
    post_serializer_class = PostBannerSerializer
    permission_classes = (LandingPage,)

    @swagger_auto_schema(request_body=PostBannerSerializer)
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(request_body=PostBannerSerializer)
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)


class BannerRetrieveAPIView(RetrieveAPIView):
    queryset = Banner.objects.all()
    serializer_class = RetrieveBannerSerializer


class BannerMainPageAPIView(ListAPIView):
    queryset = Banner.objects.all()
    serializer_class = BannerMainPageSerializer
    permission_classes = [AllowAny, ]
