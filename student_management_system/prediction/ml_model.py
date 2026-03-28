import numpy as np
from sklearn.linear_model import LinearRegression
from main.models import Student_Result, Predicted_Result

def train_model():
    """Train Linear Regression on existing Student_Result data"""
    data = Student_Result.objects.exclude(final_result__isnull=True)

    if not data.exists():
        return None

    X, y = [], []
    for d in data:
        X.append([d.assignment_mark, d.attendance_mark, d.exam_mark])
        y.append(d.final_result)

    model = LinearRegression()
    model.fit(X, y)
    return model

def predict_and_store(student_id):
    """Predict student's results and store in Predicted_Result"""
    model = train_model()
    if model is None:
        return None

    student_results = Student_Result.objects.filter(student_id=student_id)
    if not student_results.exists():
        return None

    # Remove old predictions
    Predicted_Result.objects.filter(student_id=student_id).delete()

    predictions = []
    for r in student_results:
        X_input = np.array([[r.assignment_mark, r.attendance_mark, r.exam_mark]])
        predicted_score = model.predict(X_input)[0]
        average_percentage = (predicted_score / 150) * 100 

        # Save to DB
        pr = Predicted_Result.objects.create(
            student=r.student_id,
            subject=r.subject_id,
            predicted_score=round(predicted_score, 2),
            average_percentage=round(average_percentage)
        )
        predictions.append(pr)

    return predictions