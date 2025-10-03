# mixins
from django.shortcuts import get_object_or_404, redirect

from .models import Comment, Post


class PostsQuerySetMixin:
    def get_queryset(self):
        return Post.post_list


class PostsEditMixin:
    model = Post
    template_name = "blog/create.html"
    queryset = Post.objects.select_related("author", "location", "category")


class CommentEditMixin:
    model = Comment
    pk_url_kwarg = "comment_pk"
    template_name = "blog/comment.html"


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
            redirect_kwargs = {
                self.redirect_key: self.kwargs[self.redirect_key]}
            return redirect(self.redirect_view, **redirect_kwargs)
        return super().dispatch(request, *args, **kwargs)


class PostPermissionMixin(AuthorPermissionMixin):
    model_class = Post
    redirect_view = "blog:post_detail"


class CommentPermissionMixin(AuthorPermissionMixin):
    model_class = Comment
    object_key = "comment_pk"
    redirect_view = "blog:post_detail"
