from django.db import models
from account.models import User


class Comment(models.Model):
    ticket = models.ForeignKey(
        'Ticket',
        on_delete=models.CASCADE,
        related_name='comments'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.user} on {self.ticket}"
