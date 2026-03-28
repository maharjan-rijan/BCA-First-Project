from django.urls import path
from prediction.views import predict_student_result
from prediction.views import get_saved_predictions

app_name = "prediction"

urlpatterns = [
    path('predict-result/', predict_student_result, name='predict_student_result'),
    path('get-predictions/', get_saved_predictions, name='get_saved_predictions'),
]