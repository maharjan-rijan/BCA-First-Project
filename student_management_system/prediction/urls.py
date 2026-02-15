from django.urls import path
from .views import predict_student_result

urlpatterns = [
    path(
        'predict/<int:student_id>/<int:subject_id>/',predict_student_result,name='predict_student_result'
    ),
]
