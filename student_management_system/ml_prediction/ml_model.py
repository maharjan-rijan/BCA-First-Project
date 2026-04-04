# ml_model.py

import numpy as np
from main.models import Student_Result

class LinearRegression:
    def __init__(self, learning_rate=0.0001, iterations=1000):
        self.lr = learning_rate
        self.iterations = iterations

    def fit(self, X, y):
        self.m, self.n = X.shape
        self.weights = np.zeros(self.n)
        self.bias = 0

        for _ in range(self.iterations):
            y_pred = np.dot(X, self.weights) + self.bias

            # gradients
            dw = (1 / self.m) * np.dot(X.T, (y_pred - y))
            db = (1 / self.m) * np.sum(y_pred - y)

            # update weights
            self.weights -= self.lr * dw
            self.bias -= self.lr * db

    def predict(self, X):
        return np.dot(X, self.weights) + self.bias

def predict_result(student_id):
    all_data = Student_Result.objects.all()
    student_data = Student_Result.objects.filter(student_id=student_id)

    if not all_data.exists() or not student_data.exists():
        return None

    # Training Data
    X = []
    y = []
    for row in all_data:
        X.append([
            row.exam_mark,
            row.assignment_mark,
            row.attendance_mark
        ])
        y.append(row.final_result)
    X = np.array(X, dtype=float)
    y = np.array(y, dtype=float)

    # Train custom model
    model = LinearRegression()
    model.fit(X, y)

    # Student Average Input
    exam = np.mean([i.exam_mark for i in student_data])
    assignment = np.mean([i.assignment_mark for i in student_data])
    attendance = np.mean([i.attendance_mark for i in student_data])
    prediction = model.predict(
        np.array([[exam, assignment, attendance]])
    )[0]
    percentage = (prediction / 150) * 100
    return round(prediction, 2), round(percentage, 2)