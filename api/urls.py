from django.urls import path

from . import views

app_name = "api"

urlpatterns = [
    path('modify-color/', views.modify_color, name="modify-color"),
    path('convert-color/', views.convert_color, name="convert-color"),
]
