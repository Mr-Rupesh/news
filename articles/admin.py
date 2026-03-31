from django.contrib import admin
from .models import Article, Comment


class CommentInline(admin.TabularInline):
    model = Comment
    extra = 0


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    inlines = [CommentInline]
    list_display = ["title", "source_name", "published_at"]
    list_filter = ["source_name", "published_at"]
    search_fields = ["title", "body"]
    date_hierarchy = "published_at"


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ["article", "author", "comment"]
    list_filter = ["article"]
    search_fields = ["comment"]
