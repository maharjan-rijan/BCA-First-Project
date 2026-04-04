# urls.py

from django.urls import path
from .views import predict_student_result

urlpatterns = [
    path('predict/', predict_student_result, name='predict_result'),
]