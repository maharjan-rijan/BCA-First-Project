
from django.http import JsonResponse
from .ml_model import predict_result

def predict_student_result(request):
    student_id = request.GET.get('student_id')

    if not student_id:
        return JsonResponse({'error': 'Student ID missing'})

    result = predict_result(student_id)

    if result is None:
        return JsonResponse({'error': 'No data available'})

    predicted_score, percentage = result

    return JsonResponse({
        'predicted_score': predicted_score,
        'percentage': percentage
    })