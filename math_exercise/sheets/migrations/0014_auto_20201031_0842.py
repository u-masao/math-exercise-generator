# Generated by Django 3.1 on 2020-10-30 23:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("sheets", "0009_auto_20200823_0017"),
    ]

    operations = [
        migrations.AddField(
            model_name="question",
            name="a_max",
            field=models.IntegerField(default=10),
        ),
        migrations.AddField(
            model_name="question",
            name="a_min",
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name="question",
            name="b_max",
            field=models.IntegerField(default=10),
        ),
        migrations.AddField(
            model_name="question",
            name="b_min",
            field=models.IntegerField(default=0),
        ),
    ]