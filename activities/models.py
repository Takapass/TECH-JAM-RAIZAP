from django.db import models

class Activity(models.Model):
    ACTIVITY_CHOICES = [
        ('drink','水を飲んだ'),
        ('outside','外へ出た'),
        ('stroll','散歩をした'),
        ('stretch','ストレッチをした'),
        ('gym','ジムへ行った'),
    ]

    activity_type = models.CharField(max_length=20,choices=ACTIVITY_CHOICES,unique=True)
    is_done = models.BooleanField(default=False)

    def __str__(self):
        return self.get_activity_type_display()
