from django.urls import path
from swearoff_site import views

urlpatterns = [
	path('', views.uploadView, name="upload"),
	path('result/', views.downloadView, name="download")
]