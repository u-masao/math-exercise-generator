from django.urls import path

from . import views

app_name = "sheets"
urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path(
        (
            "addition_specific_ab/<int:pages>/<int:ab_min>/"
            "<int:ab_max>/<int:a>/<int:b>/"
        ),
        views.addition_specific_ab,
        name="addition_specific_ab",
    ),
    path(
        (
            "addition_specific_ans/<int:pages>/<int:ab_min>/<int:ab_max>/"
            "<int:min_ans>/<int:max_ans>/<int:subtraction>/"
        ),
        views.addition_specific_ans,
        name="addition_specific_ans",
    ),
    path(
        (
            "substraction_specific_ab/pages:<int:pages>/<int:ab_min>/"
            "<int:ab_max>/<int:a>/<int:b>/"
        ),
        views.substraction_specific_ab,
        name="substraction_specific_ab",
    ),
]
