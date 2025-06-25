from django.shortcuts import render, get_object_or_404
from django.utils import timezone

from blog.models import Post, Category

from blog.constants import NUMOFRECPUB, NUMOFRECCAT


def post_query():
    """Запрос к таблице blog_post."""
    date_now = timezone.now()
    query_set = (
        Post.objects.select_related(
            "category",
            "location",
            "author",
        )
        .filter(
            pub_date__lte=date_now,
            is_published=True,
            category__is_published=True,
        )
    )
    return query_set


def category_query():
    """Запрос к таблице blog_category."""
    query_set = Category.objects.filter(
        is_published=True
    )
    return query_set


def index(request):
    """не более 5 записей на главную."""
    post_list = post_query().order_by("-pub_date")[:NUMOFRECPUB]
    context = {"post_list": post_list}
    return render(request, "blog/index.html", context)


def post_detail(request, id):
    """Отдельно страница поста."""
    post = get_object_or_404(
        post_query(),
        pk=id,
    )
    context = {"post": post}
    return render(request, "blog/detail.html", context)


def category_posts(request, category_slug):
    """Страница категории."""
    category = get_object_or_404(
        category_query(),
        slug=category_slug,
    )
    post_list = (
        post_query()
        .filter(category=category)
        .order_by("-pub_date")[:NUMOFRECCAT]
    )
    context = {"category": category, "post_list": post_list}
    return render(request, "blog/category.html", context)
