from blog.models import Comment, Post
from django_unicorn.components import UnicornView


class CommentsView(UnicornView):
    comments = []
    post_id = None
    new_comment = ""

    def mount(self):
        if self.post_id:
            self.load_comments()

    def load_comments(self):
        self.comments = list(Comment.objects.filter(post_id=self.post_id).order_by('-created_at'))

    def add_comment(self):
        if self.new_comment.strip():
            post = Post.objects.get(id=self.post_id)
            user = self.request.user
            Comment.objects.create(post=post, user=user, text=self.new_comment.strip())
            self.new_comment = ""
            self.load_comments()
