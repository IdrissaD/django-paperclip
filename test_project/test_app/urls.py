from django.urls import path
from .views import TestView

urlpatterns = [
    path(r'^test_object/<int:pk>/', TestView.as_view()),
]
