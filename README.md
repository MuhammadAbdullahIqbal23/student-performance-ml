# Student Performance Prediction ML Project

A comprehensive machine learning project that predicts student academic performance using regression models. This project includes a unique synthetic dataset, trained ML models, a Flask web API, and a complete CI/CD pipeline setup.

## 🎯 Project Overview

This project is designed for a Machine Learning Operations (MLOps) assignment that demonstrates:
- **Unique Dataset Creation**: Synthetic student performance data with 15+ features
- **Regression Modeling**: Multiple algorithms (Linear Regression, Random Forest)
- **Web API**: Flask application serving the trained model
- **Containerization**: Docker setup for easy deployment
- **CI/CD Pipeline**: GitHub Actions workflows for automated testing and deployment
- **Code Quality**: Automated linting with flake8
- **Unit Testing**: Comprehensive test suite with pytest

## 📊 Dataset Features

The unique synthetic dataset includes the following features to predict student final scores:

### Student Demographics
- **age**: Student age (16-25 years)
- **gender**: Male, Female, or Other
- **student_id**: Unique identifier for each student

### Socioeconomic Factors
- **parental_education**: Education level of parents (High School, Bachelor, Master, PhD, No Formal Education)
- **household_income**: Family income in USD
- **school_type**: Public or Private school
- **has_internet**: Internet access at home (0 or 1)
- **has_computer**: Computer access at home (0 or 1)

### Academic History
- **previous_gpa**: Previous GPA on a 4.0 scale
- **attendance_rate**: Class attendance percentage (0-100%)
- **study_hours_per_week**: Weekly study hours
- **class_size**: Number of students in class

### Lifestyle Factors
- **sleep_hours**: Average sleep hours per night
- **exercise_hours_per_week**: Weekly exercise hours
- **extracurricular_hours**: Weekly extracurricular activity hours

### Target Variable
- **final_score**: Student's final exam score (0-100)

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- Docker (optional)
- Git

### Installation

1. **Clone the repository:**
```bash
git clone <repository-url>
cd student-performance-ml
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Generate dataset and train model:**
```bash
cd src
python data_generator.py
python model.py
```

4. **Run the Flask API:**
```bash
python app.py
```

The API will be available at `http://localhost:5000`

## 🐳 Docker Deployment

### Build and run with Docker:
```bash
# Build the image
docker build -t student-performance-api .

# Run the container
docker run -p 5000:5000 student-performance-api
```

### Using Docker Compose:
```bash
docker-compose up --build
```

## 📁 Project Structure

```
student-performance-ml/
├── src/
│   ├── data_generator.py    # Dataset generation
│   ├── model.py            # ML model training
│   └── app.py              # Flask web API
├── tests/
│   └── test_all.py         # Unit tests
├── models/                 # Trained model files
├── data/                   # Generated datasets
├── .github/workflows/      # GitHub Actions workflows
├── requirements.txt        # Python dependencies
├── Dockerfile             # Container configuration
├── docker-compose.yml     # Multi-container setup
├── .flake8               # Code quality configuration
├── .gitignore            # Git ignore rules
└── README.md             # This file
```

## 🔧 API Endpoints

### GET `/`
Home page with API documentation

### GET `/health`
Health check endpoint
```json
{
    "status": "healthy",
    "timestamp": "2025-09-20T10:30:00",
    "model_loaded": true
}
```

### GET `/model/info`
Get model information and metrics
```json
{
    "model_metrics": {
        "r2_score": 0.95,
        "mse": 12.34,
        "model_type": "random_forest"
    },
    "feature_columns": ["age", "gender", ...],
    "target_column": "final_score"
}
```

### POST `/predict`
Predict single student performance
```json
// Request
{
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
}

// Response
{
    "prediction": 78.5,
    "input_data": {...},
    "timestamp": "2025-09-20T10:30:00"
}
```

### POST `/predict/batch`
Predict multiple students (send array of student objects)

### GET `/generate/sample`
Generate sample data for testing

## 🧪 Testing

Run all tests:
```bash
cd tests
python test_all.py
```

Run with pytest:
```bash
pytest tests/ -v
```

## 📊 Model Performance

The Random Forest model achieves:
- **R² Score**: ~0.95 (excellent predictive power)
- **RMSE**: ~5-10 points (on 0-100 scale)
- **MAE**: ~3-7 points

### Feature Importance
Top factors influencing student performance:
1. Previous GPA (highest impact)
2. Study hours per week
3. Attendance rate
4. Sleep hours
5. Household income

## 🔄 CI/CD Pipeline

### GitHub Actions Workflows

The project uses GitHub Actions for automated CI/CD pipeline. The workflow includes:

1. **Testing and Linting**:
   - Runs on Python 3.8 and 3.9
   - Executes pytest test suite
   - Performs pylint code quality checks
   - Runs on every push and pull request

2. **Docker Build and Push**:
   - Triggers after successful tests
   - Only runs on push to main branch
   - Builds Docker image with caching
   - Pushes to Docker Hub repository

To set up the workflow:
1. Add these secrets to your GitHub repository:
   - `DOCKER_USERNAME`: Your Docker Hub username
   - `DOCKER_PASSWORD`: Your Docker Hub access token
2. Ensure your Docker Hub repository exists
3. The workflow will automatically run on push/PR events

### Branch Strategy
- `dev`: Development branch for new features
- `test`: Testing branch for PR reviews
- `master`: Production-ready code

## 🛠️ Development

### Adding New Features
1. Create feature branch from `dev`
2. Implement changes
3. Run tests locally: `python tests/test_all.py`
4. Check code quality: `flake8 src/`
5. Push to `dev` branch
6. Create PR to `test` branch

### Code Quality
This project uses flake8 for code quality checks:
```bash
flake8 src/ tests/
```

## 📈 Model Training Details

### Data Preprocessing
- Categorical variables encoded using LabelEncoder
- Numerical features scaled using StandardScaler
- No missing values (synthetic data)

### Model Selection
- **Linear Regression**: Baseline model
- **Random Forest**: Production model (better performance)
- Train/Test split: 80/20
- Random seed: 42 (for reproducibility)

### Model Persistence
Models are saved using joblib and include:
- Trained model weights
- Feature scaling parameters
- Label encoders for categorical variables
- Model metadata and metrics

## 🚨 Troubleshooting

### Common Issues

1. **Model not found error**:
   ```bash
   cd src
   python model.py  # Train the model first
   ```

2. **Import errors**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Docker build fails**:
   - Ensure Docker is running
   - Check system dependencies in Dockerfile

4. **API returns 500 error**:
   - Check if model files exist in `models/` directory
   - Verify all required features are provided in request

## 🤝 Contributing

1. Fork the repository
2. Create feature branch: `git checkout -b feature-name`
3. Make changes and test thoroughly
4. Run code quality checks: `flake8 src/`
5. Submit pull request with clear description

## 📄 License

This project is created for educational purposes as part of an MLOps assignment.

## 👥 Team Members

- [Team Member 1 Name]
- [Team Member 2 Name]

## 📞 Support

For questions or issues, please create an issue in the repository or contact the team members.

---

**Assignment**: Machine Learning Operations - CI/CD Pipeline
**Deadline**: September 20, 2025
**Institution**: [Your Institution Name]