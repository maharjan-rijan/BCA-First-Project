import os
import sys
import django
import joblib
import pandas as pd
from sklearn.linear_model import LinearRegression

# 🔹 Setup Django Environment
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'student_management_system.settings')
django.setup()

from main.models import Student_Result as Result

# 🔹 Fetch data from database
results = Result.objects.all().values(
    'assignment_mark',
    'attendance_mark',
    'exam_mark',
    'final_result'
    )

df = pd.DataFrame(list(results))

# Safety check
if df.empty:
    raise ValueError("No data found in Result table")

X = df[['assignment_mark', 'attendance_mark', 'exam_mark']]
y = df['final_result']

# 🔹 Train Model
model = LinearRegression()
model.fit(X, y)

# 🔹 Save trained model
joblib.dump(model, 'ml/performance_model.pkl')

print("Model trained using database data")
