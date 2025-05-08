from .models import Comment

# a view that counts the number of unapproved comments and adds it to the context
class UnapprovedCommentCountMixin:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['unapproved_comment_count'] = Comment.objects.filter(approved=False).count()
        return context