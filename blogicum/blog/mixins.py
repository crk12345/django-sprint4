# mixins
from django.shortcuts import get_object_or_404, redirect
from django.utils import timezone

from django.db.models import Count

from .models import Category, Comment, Post, User

class PostsQuerySetMixin:
    
    def get_object(self, queryset=None):
        obj = get_object_or_404(Post, pk=self.kwargs['pk'])
        current_time = timezone.now()
        if obj.author == self.request.user: 
            return obj
        elif obj.is_published and obj.category.is_published and obj.pub_date <= current_time:
            return obj
        raise Http404("Post not found")

    def get_queryset(self):
        return Post.post_list.annotate(comment_count=Count("comments"))

class AuthorPermissionMixin:
    model_class = None
    object_key = "pk"
    redirect_view = None
    redirect_key = "pk"
    
    def get_object(self):
        key = self.kwargs.get(self.object_key)
        return get_object_or_404(self.model_class, pk=key)
    
    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if request.user != obj.author and not request.user.is_superuser:
            redirect_kwargs = {self.redirect_key: self.kwargs[self.redirect_key]}
            return redirect(self.redirect_view, **redirect_kwargs)
        return super().dispatch(request, *args, **kwargs)

class PostPermissionMixin(AuthorPermissionMixin):
    model_class = Post
    redirect_view = "blog:post_detail"

class CommentPermissionMixin(AuthorPermissionMixin):
    model_class = Comment
    object_key = "comment_pk"
    redirect_view = "blog:post_detail"


class PostsEditMixin:
    model = Post
    template_name = "blog/create.html"
    queryset = Post.objects.select_related("author", "location", "category")


class CommentEditMixin:
    model = Comment
    pk_url_kwarg = "comment_pk"
    template_name = "blog/comment.html"
