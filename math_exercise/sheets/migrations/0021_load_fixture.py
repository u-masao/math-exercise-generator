# Generated by Django 3.1 on 2020-10-31 00:06

from django.core.management import call_command
from django.db import migrations


def load_fixture(apps, schema_editor):
    call_command("loaddata", "sheets/fixture/algorythms.json", app_label="sheets")

    call_command("loaddata", "sheets/fixture/questions.json", app_label="sheets")


class Migration(migrations.Migration):

    dependencies = [
        ("sheets", "0020_question_style"),
    ]

    operations = [
        migrations.RunPython(load_fixture),
    ]
