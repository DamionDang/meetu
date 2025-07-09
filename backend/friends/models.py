from django.db import models
from users.models import CustomUser
from django.db.models import Q

class FriendRequest(models.Model):
    from_user = models.ForeignKey(
        CustomUser,
        related_name='sent_requests',
        on_delete=models.CASCADE
    )
    to_user = models.ForeignKey(
        CustomUser,
        related_name='received_requests',
        on_delete=models.CASCADE
    )
    accepted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('from_user', 'to_user')

    def __str__(self):
        return f"{self.from_user} -> {self.to_user} ({'Accepted' if self.accepted else 'Pending'})"

    def save(self, *args, **kwargs):
        if self.from_user == self.to_user:
            raise ValueError("发送失败!")
        super().save(*args, **kwargs)


class Friendship(models.Model):
    user1 = models.ForeignKey(
        CustomUser,
        related_name='friends1',
        on_delete=models.CASCADE
    )
    user2 = models.ForeignKey(
        CustomUser,
        related_name='friends2',
        on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user1', 'user2')

    def __str__(self):
        return f"{self.user1} - {self.user2}"
