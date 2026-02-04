from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Activity(models.Model):
    ACTIVITY_CHOICES = [
        ('drink','水を飲んだ'),
        ('outside','外へ出た'),
        ('stroll','散歩をした'),
        ('stretch','ストレッチをした'),
        ('gym','ジムへ行った'),
    ]

    # activity_type = models.CharField(max_length=20,choices=ACTIVITY_CHOICES,unique=True)
    # is_done = models.BooleanField(default=False)
    # user = models.ForeignKey(User, on_delete=models.CASCADE)
    # title = models.CharField(max_length=100)
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,        # ★ migration対策
        blank=True
    )

    activity_type = models.CharField(
        max_length=20,
        choices=ACTIVITY_CHOICES
    )

    title = models.CharField(
        max_length=100,
        default=""        # ★ migration対策
    )
    is_done = models.BooleanField(default=False)

    def __str__(self):
        return self.get_activity_type_display()


class DailyStamp(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # 今日押せるか判定用
    last_stamped_date = models.DateField(null=True, blank=True)
    last_skipped_date = models.DateField(null=True, blank=True)

    # 表示・進行管理用
    total_days = models.IntegerField(default=0)     # 経過日数
    done_days = models.IntegerField(default=0)      # できた日数
    skipped_days = models.IntegerField(default=0)   # パス日数
    growth_stage = models.IntegerField(default=0)  # 0=苗,1=蕾,2=花
    growth_count = models.IntegerField(default=0)  # 成長用カウント

    def can_stamp_today(self):
        today = timezone.localdate()
        return (
            self.last_stamped_date != today
            and self.last_skipped_date != today
        )


class Idea(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    image = models.ImageField(upload_to='idea_images/', blank=True, null=True) 
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.content[:20]

class IdeaReaction(models.Model):
    REACTION_CHOICES = [
        ('heart', '♡'),
        ('like', '👍'),
        ('sad', '😢'),
    ]
    idea = models.ForeignKey(Idea, on_delete=models.CASCADE, related_name='reactions')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    reaction_type = models.CharField(max_length=10, choices=REACTION_CHOICES)