from django.shortcuts import render
from django.http import JsonResponse
from main.models import Student, Student_Result, Predicted_Result
from prediction.ml_model import predict_and_store

def view_result(request):
    """Display student result table and predicted results"""
    action = request.GET.get('action', None)
    students = Student.objects.all()
    result = []
    student_id = None

    if action == "show=Students" and request.method == "POST":
        student_id = request.POST.get("student_id")
        result = Student_Result.objects.filter(student_id__id=student_id)

    context = {
        'students': students,
        'result': result,
        'action': action,
        'student_id': student_id
    }
    return render(request, "view_result.html", context)


def predict_student_result(request):
    """Trigger prediction and store in DB"""
    student_id = request.GET.get("student_id")
    if not student_id:
        return JsonResponse({"error": "Student not selected"})

    predictions = predict_and_store(student_id)
    if not predictions:
        return JsonResponse({"error": "Not enough data to predict"})

    return JsonResponse({"success": True})


def get_saved_predictions(request):
    """Fetch predictions from DB for a student"""
    student_id = request.GET.get("student_id")
    predictions = Predicted_Result.objects.filter(student__id=student_id)

    data = [
        {"subject": p.subject.name, "predicted_score": p.predicted_score, "average_percentage": p.average_percentage}
        for p in predictions
    ]

    return JsonResponse({"predictions": data})