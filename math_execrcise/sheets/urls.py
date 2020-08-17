from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path(
        "add_specific_ab/<int:pages>/<int:ab_max>/<int:a>/<int:b>/",
        views.add_specific_ab,
        name="add_specific_ab",
    ),
    path(
        (
            "add_specific_ans/<int:pages>/<int:ab_max>/"
            "<int:ans>/<int:width>/<int:subtraction>/"
        ),
        views.add_specific_ans,
        name="add_specific_ans",
    ),
    path(
        "diff_specific_ab/pages:<int:pages>/<int:ab_max>/<int:a>/<int:b>/",
        views.diff_specific_ab,
        name="diff_specific_ab",
    ),
]
