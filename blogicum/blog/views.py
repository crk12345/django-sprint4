from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect
from django.utils import timezone
from django.urls import reverse, reverse_lazy
from django.db.models import Count
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from .forms import CreateCommentForm, CreatePostForm
from .models import Category, Comment, Post, User
from .constants import PAGINATED_BY
from .mixins import (
    PostsQuerySetMixin, PostsEditMixin, CommentEditMixin, AuthorPermissionMixin,
    PostPermissionMixin, CommentPermissionMixin
)


class PostDeleteView(LoginRequiredMixin, PostPermissionMixin,
                     PostsEditMixin, DeleteView):
    success_url = reverse_lazy("blog:index")


class PostUpdateView(LoginRequiredMixin, PostPermissionMixin,
                     PostsEditMixin, UpdateView):
    form_class = CreatePostForm


class PostCreateView(LoginRequiredMixin, PostsEditMixin, CreateView):
    form_class = CreatePostForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self) -> str:
        return reverse(
            "blog:profile",
            kwargs={
                "username": self.request.user.username,
            },
        )


class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CreateCommentForm

    def form_valid(self, form):
        form.instance.post = get_object_or_404(Post, pk=self.kwargs["pk"])
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("blog:post_detail", kwargs={"pk": self.kwargs["pk"]})


class CommentDeleteView(LoginRequiredMixin, CommentPermissionMixin,
                        CommentEditMixin, DeleteView):
    def get_success_url(self):
        return reverse("blog:post_detail", kwargs={"pk": self.kwargs["pk"]})


class CommentUpdateView(LoginRequiredMixin, CommentPermissionMixin,
                        CommentEditMixin, UpdateView):
    form_class = CreateCommentForm

    def get_success_url(self):
        return reverse("blog:post_detail", kwargs={"pk": self.kwargs["pk"]})


class AuthorProfileListView(PostsQuerySetMixin, ListView):
    model = Post
    template_name = "blog/profile.html"
    paginate_by = PAGINATED_BY

    def get_queryset(self):
        author = get_object_or_404(User, username=self.kwargs["username"])

        if self.request.user == author:
            return (
                author.posts.select_related("category", "author", "location")
                .all()
                .annotate(comment_count=Count("comments"))
                .order_by('-pub_date')
            )

        return (
            super()
            .get_queryset()
            .filter(author=author)
            .order_by('-pub_date')
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["profile"] = get_object_or_404(
            User, username=self.kwargs["username"]
        )
        return context


class BlogIndexListView(PostsQuerySetMixin, ListView):
    model = Post
    template_name = "blog/index.html"
    paginate_by = PAGINATED_BY

    def get_queryset(self):
        return super().get_queryset()


class BlogCategoryListView(PostsQuerySetMixin, ListView):
    model = Post
    template_name = "blog/category.html"
    context_object_name = "post_list"
    paginate_by = PAGINATED_BY

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["category"] = get_object_or_404(
            Category, slug=self.kwargs["category_slug"], is_published=True
        )
        return context

    def get_queryset(self):
        self.category = get_object_or_404(
            Category, slug=self.kwargs["category_slug"])
        return (
            super()
            .get_queryset()
            .filter(category=self.category)
            .filter(category__slug=self.kwargs["category_slug"])
        )


class PostDetailView(PostsQuerySetMixin, DetailView):
    model = Post
    template_name = "blog/detail.html"
    pk_url_kwarg = "pk"

    def get_object(self, queryset=None):
        obj = get_object_or_404(Post, pk=self.kwargs['pk'])
        current_time = timezone.now()
        if obj.author == self.request.user:
            return obj
        elif (obj.is_published and obj.category.is_published
              and obj.pub_date <= current_time):
            return obj
        raise Http404("Post not found")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = CreateCommentForm()
        context["comments"] = (
            self.get_object().comments.prefetch_related("author").all()
        )
        return context

    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .prefetch_related(
                "comments",
            )
        )
