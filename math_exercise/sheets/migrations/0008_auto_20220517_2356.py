# Generated by Django 3.2.11 on 2022-05-17 23:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("sheets", "0007_auto_20220511_1156"),
    ]

    operations = [
        migrations.AddField(
            model_name="question",
            name="arg1",
            field=models.IntegerField(default=1),
        ),
        migrations.AlterField(
            model_name="algorythm",
            name="id",
            field=models.BigAutoField(
                auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
            ),
        ),
        migrations.AlterField(
            model_name="question",
            name="id",
            field=models.BigAutoField(
                auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
            ),
        ),
    ]