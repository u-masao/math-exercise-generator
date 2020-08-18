from django.contrib import admin

from .models import Question


class QuestionAdmin(admin.ModelAdmin):
    search_fields = ["theme_text"]
    list_filter = ["modified", "created"]
    list_display = ("theme_text", "modified", "action")


admin.site.register(Question, QuestionAdmin)
