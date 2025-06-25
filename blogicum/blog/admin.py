from django.contrib import admin

from .models import Location, Category, Post

admin.site.empty_value_display = "Не задано"


def get_all_fields(model):
    """Вернуть список всех полей модели."""
    return model._meta.get_fields()


class BlogAdmin(admin.ModelAdmin):
    """Общий интерфейс админ-панели блог."""

    list_editable = ("is_published",)


@admin.register(Post)
class PostAdmin(BlogAdmin):
    """Интерфейс для постов."""

    list_display = [
        field.name
        for field in get_all_fields(Post)
        if field.name not in ("id", "text")
    ]
    list_display_links = ("title",)
    search_fields = (
        "title",
        "text",
    )
    list_filter = (
        "is_published",
        "category",
        "location",
        "author",
    )


@admin.register(Category)
class CategoryAdmin(BlogAdmin):
    """Интерфейс для категорий."""

    list_display = (
        "title",
        "is_published",
        "created_at",
        "slug",
    )


@admin.register(Location)
class LocationAdmin(BlogAdmin):
    """Интерфейс для местоположения."""

    list_display = (
        "name",
        "is_published",
        "created_at",
    )
