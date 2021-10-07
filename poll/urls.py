from django.urls import path
from . import views

urlpatterns = [
    path('', views.PollListView.as_view(), name="home"),
    path('<int:pk>', views.singlePollDetail, name='poll-detail'),
    path('<int:pk>/data', views.poll_data_view, name='poll-data-view'),
    path('<int:pk>/save', views.save_poll_data, name='save-poll-view'),
    path('<int:pk>/result', views.option_count_data, name='option-count-data'),
    path('create/', views.create_poll, name='create')


  
]