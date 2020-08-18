from django.db import models


class Question(models.Model):
    created = models.DateTimeField("date created")
    modified = models.DateTimeField("date modified")
    theme_text = models.CharField(max_length=200)
    level_text = models.CharField(max_length=20)
    level_number = models.IntegerField(default=0)
    action = models.CharField(max_length=100)
    params_text = models.CharField(max_length=100)

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
