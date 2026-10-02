from django.db import models

# Create your models here.
class Tag(models.Model):
    name = models.CharField(
        max_length=255,
        unique=True
    )

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Task(models.Model):
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    deadline = models.DateTimeField(null=True, blank=True)
    is_done = models.BooleanField(default=False)
    tags = models.ManyToManyField(Tag, related_name="tasks", blank=True)

    class Meta:
        ordering = ["is_done", "-created_at"]

    @property
    def datetime(self):
        return self.created_at

    def __str__(self):
        return f"{self.content} ({'Done' if self.is_done else 'Not done'})"
