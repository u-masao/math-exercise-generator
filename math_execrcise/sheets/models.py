from django.db import models


class Algorythm(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=100)
    usage = models.CharField(max_length=300)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Question(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    theme_text = models.CharField(max_length=200)
    level_text = models.CharField(max_length=20)
    level_number = models.IntegerField(default=0)
    algorythm = models.ForeignKey(Algorythm, on_delete=models.CASCADE)
    pages = models.IntegerField(default=5)
    ans_min = models.IntegerField(default=0)
    ans_max = models.IntegerField(default=10)
    ab_min = models.IntegerField(default=0)
    ab_max = models.IntegerField(default=10)
    a = models.IntegerField(default=0)
    b = models.IntegerField(default=0)

    def __str__(self):
        return "{} {}-{:03d}".format(
            self.theme_text, self.level_text, self.level_number
        )

    """
    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now

    was_published_recently.admin_order_field = "pub_date"  # type: ignore
    was_published_recently.boolean = True  # type: ignore
    was_published_recently.short_description = (  # type: ignore
        "Published recently?"
    )
    """
