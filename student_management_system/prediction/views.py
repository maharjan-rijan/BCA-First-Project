import os
import joblib
import numpy as np
from main.models import Student_Result
from django.shortcuts import render
from django.conf import settings

# Create your views here.
MODEL_PATH = os.path.join(settings.BASE_DIR, 'ml', 'performance_model.pkl')
model = joblib.load(MODEL_PATH)
def predict_student_result(request):
    if request.method == 'POST':
        # Get input data from the form
        attendance = float(request.POST.get('attendance', 0))
        assignment_mark = float(request.POST.get('assignment_mark', 0))
        exam_mark = float(request.POST.get('exam_mark', 0))

        # Prepare the input data for prediction
        input_data = np.array([[attendance, assignment_mark, exam_mark]])

        # Make the prediction using the loaded model
        predicted_result = model.predict(input_data)[0]

        # Save the result to the database
        Student_Result.objects.create(
            student_id=request.user.student,
            attendance=attendance,
            assignment_mark=assignment_mark,
            exam_mark=exam_mark,
            final_result=predicted_result
        )

        return render(request, 'result_predict.html', {'predicted_result': predicted_result})

    return render(request, 'result_predict.html')