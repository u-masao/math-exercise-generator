from django.contrib import admin

from .models import Question, Algorythm


class AlgorythmAdmin(admin.ModelAdmin):
    search_fields = ["name"]
    list_filter = ["modified", "created"]
    list_display = ("name", "description", "modified")


class QuestionAdmin(admin.ModelAdmin):
    search_fields = ["theme_text"]
    list_filter = ["modified", "created"]
    list_display = (
        "theme_text",
        "algorythm",
        "level_text",
        "level_number",
        "modified",
    )


admin.site.register(Question, QuestionAdmin)
admin.site.register(Algorythm, AlgorythmAdmin)
