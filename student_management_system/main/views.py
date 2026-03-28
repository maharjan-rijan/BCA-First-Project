from django.http import JsonResponse
from .models import Student_Result
from prediction.ml_model import train_model
import numpy as np

def predict_student_result(request):
    student_id = request.GET.get("student_id")
    
    results = Student_Result.objects.filter(student_id__id=student_id)

    print("Results count:", results.count())

    if not results.exists():
        return JsonResponse({
            "predictions": [],
            "error": "No student data found"
        })

    model = train_model()

    if model is None:
        return JsonResponse({
            "predictions": [],
            "error": "Not enough data to train model"
        })

    predictions = []

    for r in results:
        data = np.array([[
            r.assignment_mark,
            r.attendance_mark,
            r.exam_mark
        ]])

        predicted = model.predict(data)[0]

        predictions.append({
            "subject": r.subject_id.name,
            "predicted_score": round(predicted, 2)
        })

    print("Predictions:", predictions)

    return JsonResponse({
        "predictions": predictions
    })