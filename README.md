
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

## � CI/CD Pipeline

This project includes a complete CI/CD pipeline with GitHub Actions and Jenkins integration:

### Pipeline Flow
```
Pull Request → GitHub Actions (Tests) → Merge to Master → Build & Push Docker → Trigger Jenkins → Deploy & Notify
```

### Features
- ✅ **Automated Testing**: Runs on every pull request
- ✅ **Code Quality Checks**: flake8 linting and pytest tests
- ✅ **Docker Build & Push**: Automatic containerization on master merge
- ✅ **Jenkins Integration**: Triggers deployment pipeline
- ✅ **Email Notifications**: Administrators notified of deployment status
- ✅ **Multi-environment Support**: Development, testing, and production stages

### Quick Setup
1. **Configure GitHub Secrets**: Add Docker Hub and Jenkins credentials
2. **Set up Jenkins**: Install required plugins and configure job
3. **Configure Email**: Set up SMTP for notifications

📖 **For complete setup instructions, see [PIPELINE_SETUP.md](PIPELINE_SETUP.md)**

## �🐳 Docker Deployment

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

### Production Deployment:
```bash
# Pull the latest production image
docker pull your-username/student-performance-ml:production

# Run in production mode
docker run -d -p 5000:5000 --name student-performance-api \
  your-username/student-performance-ml:production
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
│   └── ci-cd.yml          # Main CI/CD pipeline
├── Jenkinsfile            # Jenkins pipeline configuration
├── PIPELINE_SETUP.md      # CI/CD setup instructions
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

This project implements a comprehensive CI/CD pipeline with automated testing, Docker containerization, and Jenkins deployment. 

### Pipeline Architecture

```
Pull Request → GitHub Actions (Tests) → Merge to Master → GitHub Actions (Trigger Jenkins) → Jenkins (Build & Deploy) → Email Notification
```

### GitHub Actions Workflows

**Automated Testing (Pull Requests)**:
- Runs on Python 3.8, 3.9, and 3.10
- Executes pytest test suite with verbose output
- Performs flake8 linting with extended configuration
- Runs pylint code quality analysis
- Blocks merge if any tests fail

**Jenkins Trigger (Master Branch)**:
- Triggers only on master/main branch pushes
- Calls Jenkins API to start deployment pipeline
- Passes branch name, commit SHA, and commit message
- Provides build status feedback

### Jenkins Pipeline

**Build Process**:
1. **Checkout**: Retrieves latest code from repository
2. **Environment Setup**: Configures Docker image naming and tags
3. **Build**: Creates Docker image with multiple tags (build number, latest, commit SHA)
4. **Test**: Runs health checks on built container
5. **Push**: Deploys to Docker Hub with all tags
6. **Cleanup**: Removes local images and prunes Docker system

**Email Notifications**:
- **Success**: Detailed build information with Docker Hub links
- **Failure**: Error details with console output links
- **Unstable**: Warning notifications for builds with issues

### Setup Requirements

**GitHub Secrets** (Repository Settings → Secrets):
```
DOCKERHUB_USERNAME     # Docker Hub username
DOCKERHUB_TOKEN        # Docker Hub access token
JENKINS_URL            # Jenkins instance URL
JENKINS_USER           # Jenkins username
JENKINS_TOKEN          # Jenkins API token
JENKINS_JOB_NAME       # Jenkins job name
```

**Jenkins Credentials**:
```
dockerhub-credentials  # Docker Hub username/token
admin-email-list       # Comma-separated admin emails
```

**Required Jenkins Plugins**:
- Docker Pipeline Plugin
- Email Extension Plugin
- Pipeline Plugin
- Git Plugin
- Credentials Plugin

### Branch Strategy

- **dev**: Development branch for new features
- **feat/***: Feature branches created from dev
- **master/main**: Production branch (triggers Jenkins deployment)

### Docker Hub Integration

The pipeline publishes Docker images with multiple tags:
- `latest`: Most recent production build
- `build-{number}`: Specific build number
- `{commit-sha}`: Git commit identifier

### Monitoring and Notifications

**GitHub Actions**:
- View workflow status in repository Actions tab
- Real-time build logs and failure details
- Status badges for README display

**Jenkins**:
- Comprehensive build history and logs
- Email notifications to administrators
- Build artifacts and metadata storage

**Email Notifications Include**:
- Build status and duration
- Branch and commit information
- Docker image links and tags
- Console output for failures
- Direct links to Jenkins and Docker Hub

### Quick Setup Guide

1. **Configure GitHub Secrets**: Add all required secrets to repository
2. **Setup Jenkins Job**: Create pipeline job pointing to repository
3. **Configure Jenkins Credentials**: Add Docker Hub and email credentials
4. **Test Pipeline**: Create a pull request to verify automated testing
5. **Deploy**: Merge to master to trigger full deployment pipeline

For detailed setup instructions, see [CI_CD_SETUP.md](CI_CD_SETUP.md)

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