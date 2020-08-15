from django.contrib import admin  # noqa: F401

from .models import Question

admin.site.register(Question)
