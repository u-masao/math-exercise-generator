from django.urls import path

from . import views

handler500 = views.my_customized_server_error

app_name = "sheets"
_url_params = ()
urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path(
        (
            "pdf/<str:action>/"
            "<int:pages>/<int:ab_min>/<int:ab_max>/"
            "<int:ans_min>/<int:ans_max>/<int:a>/<int:b>/"
            "<int:a_min>/<int:a_max>/<int:b_min>/<int:b_max>/<str:style>/"
        ),
        views.pdf,
        name="pdf",
    ),
]
