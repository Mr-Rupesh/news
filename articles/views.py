import datetime

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.utils import timezone
from django.views import View
from django.views.generic import ListView, DetailView, FormView
from django.views.generic.detail import SingleObjectMixin
from django.urls import reverse

from .forms import CommentForm
from .models import Article
from .services.news_api import fetch_top_headlines, save_articles


class ArticleListView(LoginRequiredMixin, ListView):
    model = Article
    template_name = "article_list.html"

    def get_queryset(self):
        queryset = super().get_queryset()
        # If "all=1" is in query params, show all news
        if self.request.GET.get("all") == "1":
            return queryset
        # Otherwise, filter to last 1 hour
        one_hour_ago = timezone.now() - datetime.timedelta(hours=1)
        return queryset.filter(published_at__gte=one_hour_ago)


class CommentGet(DetailView):
    model = Article
    template_name = "article_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = CommentForm()
        return context


class CommentPost(SingleObjectMixin, FormView):
    model = Article
    form_class = CommentForm
    template_name = "article_detail.html"

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        comment = form.save(commit=False)
        comment.article = self.object
        comment.author = self.request.user
        comment.save()
        return super().form_valid(form)

    def get_success_url(self):
        article = self.object
        return reverse("article_detail", kwargs={"pk": article.pk})


class ArticleDetailView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        view = CommentGet.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        view = CommentPost.as_view()
        return view(request, *args, **kwargs)


class FetchNewsView(View):
    """Trigger news fetch via HTTP GET (for Render free tier without shell)."""

    def get(self, request):
        try:
            data = fetch_top_headlines(count=20)
            saved = save_articles(data)
            return JsonResponse({
                "status": "success",
                "saved": saved,
                "message": f"Fetched and saved {saved} new articles"
            })
        except Exception as e:
            return JsonResponse({
                "status": "error",
                "message": str(e)
            }, status=500)
