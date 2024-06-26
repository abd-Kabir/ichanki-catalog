from django.urls import path
from rest_framework.routers import DefaultRouter

from apps.content.views import NewsModelViewSet, ArticleModelViewSet, ArticleRetrieveAPIView, NewsRetrieveAPIView, \
    BannerModelViewSet, BannerRetrieveAPIView, BannerMainPageAPIView, NewsLandingListAPIView, \
    NewsLandingRetrieveAPIView, NewsPageListAPIView, KnowledgeBaseModelViewSet, KnowledgeBaseRetrieveAPIView, \
    KnowledgeBasePageListAPIView

router = DefaultRouter()
router.register(r'news', NewsModelViewSet, basename='news')
router.register(r'knowledge-base', KnowledgeBaseModelViewSet, basename='knowledge_base')
router.register(r'article', ArticleModelViewSet, basename='article')
router.register(r'banner', BannerModelViewSet, basename='banner')

app_name = 'content'
urlpatterns = [
    path('article/<int:pk>/all/', ArticleRetrieveAPIView.as_view(), name='article_retrieve_all'),
    path('news/<int:pk>/all/', NewsRetrieveAPIView.as_view(), name='news_retrieve_all'),
    path('news/landing-page/', NewsLandingListAPIView.as_view(), name='news_landing_page'),
    path('news/landing-page/<int:pk>/', NewsLandingRetrieveAPIView.as_view(), name='news_landing_page_retrieve'),
    path('news/page/', NewsPageListAPIView.as_view(), name='news_page'),
    path('banner/<int:pk>/all/', BannerRetrieveAPIView.as_view(), name='banner_retrieve_all'),
    path('banner/main-page/', BannerMainPageAPIView.as_view(), name='banner_main_page'),
    path('knowledge-base/page/', KnowledgeBasePageListAPIView.as_view(), name='knowledge_base_page'),
    path('knowledge-base/<int:pk>/all/', KnowledgeBaseRetrieveAPIView.as_view(), name='knowledge_base_retrieve_all'),
]
urlpatterns += router.urls
