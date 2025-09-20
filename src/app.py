"""
Flask Web Application for Student Performance Prediction
Serves the trained ML model via REST API endpoints.
"""

from flask import Flask, request, jsonify, render_template_string
import pandas as pd
import numpy as np
import os
import sys
from datetime import datetime

# Add src directory to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '.'))

try:
    from model import StudentPerformanceModel
    from data_generator import StudentDataGenerator
except ImportError:
    print("Required modules not found. Make sure model.py and "
          "data_generator.py are in the same directory.")

app = Flask(__name__)

# Global model instance
model = None


def load_or_train_model():
    """Load existing model or train a new one if not found."""
    global model
    model = StudentPerformanceModel()

    models_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'models')
    model_path = os.path.join(models_dir, 'student_performance_model.joblib')

    if os.path.exists(model_path):
        try:
            model.load_model(models_dir)
            print("Model loaded successfully!")
            return True
        except Exception as e:
            print(f"Error loading model: {e}")
            return False

    return False


@app.route('/')
def home():
    """Home page with API documentation."""
    html_template = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Student Performance Prediction API</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; }
            .endpoint { background-color: #f5f5f5; padding: 15px;
                       margin: 10px 0; border-radius: 5px; }
            .method { color: #007bff; font-weight: bold; }
            .path { color: #28a745; font-weight: bold; }
            code { background-color: #e9ecef; padding: 2px 4px; border-radius: 3px; }
        </style>
    </head>
    <body>
        <h1>Student Performance Prediction API</h1>
        <p>This API provides endpoints for predicting student academic
        performance based on various factors.</p>

        <h2>Available Endpoints:</h2>

        <div class="endpoint">
            <h3><span class="method">GET</span> <span class="path">/</span></h3>
            <p>This documentation page.</p>
        </div>

        <div class="endpoint">
            <h3><span class="method">GET</span> <span class="path">/health</span></h3>
            <p>Check API health status.</p>
        </div>

        <div class="endpoint">
            <h3><span class="method">GET</span> <span class="path">/model/info</span></h3>
            <p>Get information about the trained model including metrics and features.</p>
        </div>

        <div class="endpoint">
            <h3><span class="method">POST</span> <span class="path">/predict</span></h3>
            <p>Predict student performance. Send JSON data with student features.</p>
            <p><strong>Example request body:</strong></p>
            <pre><code>{
    "age": 18,
    "gender": "Female",
    "parental_education": "Bachelor",
    "household_income": 65000,
    "previous_gpa": 3.2,
    "study_hours_per_week": 15,
    "attendance_rate": 85,
    "sleep_hours": 7,
    "exercise_hours_per_week": 4,
    "has_internet": 1,
    "has_computer": 1,
    "extracurricular_hours": 5,
    "school_type": "Public",
    "class_size": 25
}</code></pre>
        </div>

        <div class="endpoint">
            <h3><span class="method">POST</span> <span class="path">/predict/batch</span></h3>
            <p>Predict performance for multiple students. Send JSON array of student data.</p>
        </div>

        <div class="endpoint">
            <h3><span class="method">GET</span> <span class="path">/generate/sample</span></h3>
            <p>Generate sample student data for testing predictions.</p>
        </div>

        <h2>Model Features:</h2>
        <ul>
            <li>age: Student age (16-25)</li>
            <li>gender: Male, Female, or Other</li>
            <li>parental_education: High School, Bachelor, Master, PhD, No Formal Education</li>
            <li>household_income: Family income in USD</li>
            <li>previous_gpa: Previous GPA (0.0-4.0)</li>
            <li>study_hours_per_week: Weekly study hours</li>
            <li>attendance_rate: Class attendance percentage</li>
            <li>sleep_hours: Average sleep hours per night</li>
            <li>exercise_hours_per_week: Weekly exercise hours</li>
            <li>has_internet: Internet access (0 or 1)</li>
            <li>has_computer: Computer access (0 or 1)</li>
            <li>extracurricular_hours: Weekly extracurricular activity hours</li>
            <li>school_type: Public or Private</li>
            <li>class_size: Number of students in class</li>
        </ul>
    </body>
    </html>
    """
    return render_template_string(html_template)


@app.route('/health')
def health():
    """Health check endpoint."""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'model_loaded': model is not None
    })


@app.route('/model/info')
def model_info():
    """Get model information."""
    if model is None:
        return jsonify({'error': 'Model not loaded'}), 500

    return jsonify({
        'model_metrics': model.model_metrics,
        'feature_columns': model.feature_columns,
        'target_column': model.target_column
    })


@app.route('/predict', methods=['POST'])
def predict_single():
    """Predict performance for a single student."""
    if model is None:
        return jsonify({'error': 'Model not loaded'}), 500

    try:
        # Get JSON data from request
        data = request.get_json()

        if not data:
            return jsonify({'error': 'No data provided'}), 400

        # Convert to DataFrame
        df = pd.DataFrame([data])

        # Make prediction
        prediction = model.predict(df)

        return jsonify({
            'prediction': float(prediction[0]),
            'input_data': data,
            'timestamp': datetime.now().isoformat()
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/predict/batch', methods=['POST'])
def predict_batch():
    """Predict performance for multiple students."""
    if model is None:
        return jsonify({'error': 'Model not loaded'}), 500

    try:
        # Get JSON data from request
        data = request.get_json()

        if not data or not isinstance(data, list):
            return jsonify({'error': 'Data should be a list of student records'}), 400

        # Convert to DataFrame
        df = pd.DataFrame(data)

        # Make predictions
        predictions = model.predict(df)

        # Prepare response
        results = []
        for i, (prediction, input_data) in enumerate(zip(predictions, data)):
            results.append({
                'student_index': i,
                'prediction': float(prediction),
                'input_data': input_data
            })

        return jsonify({
            'predictions': results,
            'count': len(results),
            'timestamp': datetime.now().isoformat()
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/generate/sample')
def generate_sample():
    """Generate sample student data for testing."""
    try:
        generator = StudentDataGenerator(num_students=5, random_seed=np.random.randint(1, 1000))
        sample_data = generator.generate_dataset()

        # Remove student_id and final_score for prediction input
        prediction_data = sample_data.drop(['student_id', 'final_score'], axis=1)

        return jsonify({
            'sample_data': prediction_data.to_dict('records'),
            'actual_scores': sample_data['final_score'].tolist(),
            'count': len(sample_data),
            'note': 'Use sample_data for predictions, actual_scores for comparison'
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors."""
    return jsonify({'error': 'Endpoint not found'}), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors."""
    return jsonify({'error': 'Internal server error'}), 500


if __name__ == '__main__':
    print("Starting Student Performance Prediction API...")

    # Try to load existing model
    if not load_or_train_model():
        print("No trained model found. Please train a model first by running model.py")
        sys.exit(1)

    print("Model loaded successfully!")
    print("Starting Flask server...")

    # Run the Flask app
    app.run(debug=True, host='0.0.0.0', port=5000)
