from django.urls import path

from . import views

app_name = 'task'


urlpatterns = [
    path('', views.home_view, name='home'),
    path('mytasks/', views.tasks, name='my_tasks'),
    path('task_detail/<str:pk>/', views.task_detail, name='task_detail'),
    path('task_update/<str:pk>/', views.task_update, name='task_update'),
    # path('task_status/<int:pk>/', views.task_status, name='task_status'),
    path('task_delete/<int:pk>/', views.task_delete, name='task_delete'),
]
