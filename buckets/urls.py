from django.urls import path
from . import views

app_name = 'buckets'

urlpatterns = [
    path('', views.BucketListView.as_view(), name='list'),
    path('create/', views.BucketCreateView.as_view(), name='create'),
    path('<int:pk>/edit/', views.BucketUpdateView.as_view(), name='edit'),
    path('<int:pk>/delete/', views.BucketDeleteView.as_view(), name='delete'),
]
