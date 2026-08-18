from .views import RegisterView
from django.urls import path

urlpatterns = [
    path('signup/', RegisterView.as_view(), name='register'),
   
]