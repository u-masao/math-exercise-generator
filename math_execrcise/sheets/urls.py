from django.urls import path

from . import views

app_name = "sheets"
_url_params = (
    "/<int:pages>/<int:ab_min>/<int:ab_max>/"
    "<int:ans_min>/<int:ans_max>/<int:a>/<int:b>/"
)
urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("action/<str:action>" + _url_params, views.action, name="action",),
]
