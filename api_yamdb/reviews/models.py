from django.db import models

from .constants import CHARS_PER_STR

CHOICES = (
    (1, 1),
    (2, 2),
    (3, 3),
    (4, 4),
    (5, 5),
    (6, 6),
    (7, 7),
    (8, 8),
    (9, 9),
    (10, 10),
)

class Review(models.Model):
    """Модель Review(отзыв)."""

    title_id = models.ForeignKey(Titles, on_delete=models.CASCADE)
    text = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.IntegerField(choices=CHOICES)
    pub_date = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.text[:CHARS_PER_STR]


class Comments(models.Model):
    """Модель Comments(комментарии)."""

    review_id = models.ForeignKey(Review, on_delete=models.CASCADE)
    text = models.TextField()
    pub_date = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.text[:CHARS_PER_STR]
