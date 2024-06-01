from django.urls import path
from . import views

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('upload', views.upload_file, name='post_upload_file'),
    path('view/<str:model_name>', views.view_data, name='view_data'),     # <--- передаём model_name через URL
    path('view_all', views.view_all_data, name='view_all_data'),  # <--- новый путь для отображения всех данных
]


