from django.urls import path

from . import views

app_name = "sheets"
_url_params = (
    "/<int:pages>/<int:ab_min>/<int:ab_max>/"
    "<int:ans_min>/<int:ans_max>/<int:a>/<int:b>/"
)
urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path(
        "addition_specific_ab" + _url_params,
        views.addition_specific_ab,
        name="addition_specific_ab",
    ),
    path(
        "addition_specific_ans" + _url_params,
        views.addition_specific_ans,
        name="addition_specific_ans",
    ),
    path(
        "addition_specific_ans" + _url_params,
        views.substraction_specific_ab,
        name="substraction_specific_ab",
    ),
]
