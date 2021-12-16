from django.urls import path
from . import views

urlpatterns = [
    path('', views.PollListView.as_view(), name="home"),
    path('<int:pk>', views.singlePollDetail, name='poll-detail'),
    path('<int:pk>/data', views.poll_data_view, name='poll-data-view'),
    path('<int:pk>/save', views.save_poll_data, name='save-poll-view'),
    path('<int:pk>/result', views.result_data, name='result'),
    path('<int:pk>/result-json/', views.result_json, name='result-data-json'),
    path('create/', views.create_poll, name='create'),


    path('login/', views.loginGoogle, name='login')


  
]