# Generated by Django 3.2.11 on 2022-05-18 00:11

from django.core.management import call_command
from django.db import migrations


def load_fixture(apps, schema_editor):
    call_command("loaddata", "sheets/fixture/0009/algorythms.json", app_label="sheets")
    call_command("loaddata", "sheets/fixture/0009/questions.json", app_label="sheets")


class Migration(migrations.Migration):

    dependencies = [
        ("sheets", "0008_auto_20220517_2356"),
    ]

    operations = [
        migrations.RunPython(load_fixture),
    ]