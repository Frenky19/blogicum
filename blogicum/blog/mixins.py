from django.shortcuts import redirect


class AuthorRequiredMixin:
    """Миксин, проверяющий, что текущий пользователь является автором."""

    def dispatch(self, request, *args, **kwargs):
        post = self.get_object()
        if post.author != request.user:
            return redirect('blog:post_detail', post_id=post.pk)
        return super().dispatch(request, *args, **kwargs)
