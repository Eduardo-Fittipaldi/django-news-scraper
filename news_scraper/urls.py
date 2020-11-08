from django.urls import path
from . import views

app_name = "news"

urlpatterns = [
    path('', views.NewspapersIndexView.as_view(), name='index'),
    path("<int:pk>/", views.newspaper, name='newspaper')
]