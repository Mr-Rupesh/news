from django.urls import path
from .views import (
    ArticleListView,
    ArticleDetailView,
    FetchNewsView,
)

urlpatterns = [
    path("<int:pk>/", ArticleDetailView.as_view(), name="article_detail"),
    path("fetch-news/", FetchNewsView.as_view(), name="fetch_news"),
    path("", ArticleListView.as_view(), name="article_list"),
]
