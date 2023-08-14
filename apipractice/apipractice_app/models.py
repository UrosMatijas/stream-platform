from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models import Avg
from django.contrib.auth.models import User


class StreamPlatform(models.Model):
    name = models.CharField(max_length=40)
    website = models.URLField(max_length=150)

    def __str__(self):
        return self.name

class Video(models.Model):
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=200)
    avg_rating = models.DecimalField(max_digits=3, decimal_places=2, null=True, editable=False)
    platform = models.ForeignKey(StreamPlatform, on_delete=models.CASCADE, related_name='videos')
    active = models.BooleanField(default=True)

    def update_avg_rating(self):
        average = self.reviews.aggregate(Avg('rating')).get('rating__avg')
        if average is not None:
            self.avg_rating = round(average, 2)
        else:
            self.avg_rating = None

    def __str__(self):
        return self.title

class Review(models.Model):
    review_user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    rating = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    comment = models.CharField(max_length=200, null=True)
    video = models.ForeignKey(Video, on_delete=models.CASCADE, related_name='reviews')
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        is_new_review = not self.pk
        super().save(*args, **kwargs)

        if is_new_review:
            self.video.update_avg_rating()
            self.video.save()

    def __str__(self):
        return str(self.rating)