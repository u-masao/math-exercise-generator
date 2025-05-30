# Generated by Django 3.2.11 on 2022-01-30 09:16

from django.core.management import call_command
from django.db import migrations


def load_fixture(apps, schema_editor):
    call_command("loaddata", "sheets/fixture/0005/algorythms.json", app_label="sheets")
    call_command("loaddata", "sheets/fixture/0005/questions.json", app_label="sheets")


class Migration(migrations.Migration):

    dependencies = [
        ("sheets", "0004_auto_20220130_0906"),
    ]

    operations = [
        # migrations.RunPython(load_fixture),
    ]
