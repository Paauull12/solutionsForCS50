from django.urls import path
from . import views

urlpatterns = [

        path('', views.home, name='home'),
        path('get-file-content/', views.get_file_content, name='get-file-content'),

        path('get-folder-details/', views.get_folder_details, name='get_folder_details'),
    ]