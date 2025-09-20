"""
Student Performance Dataset Generator
Creates a unique synthetic dataset for predicting student academic performance.
"""

import numpy as np
import pandas as pd
# from datetime import datetime  # unused import
import os


class StudentDataGenerator:
    """Generate synthetic student performance data."""

    def __init__(self, num_students=500, random_seed=42):
        """
        Initialize the data generator.

        Args:
            num_students (int): Number of student records to generate
            random_seed (int): Random seed for reproducibility
        """
        self.num_students = num_students
        self.random_seed = random_seed
        np.random.seed(random_seed)

    def generate_dataset(self):
        """
        Generate a comprehensive student performance dataset.

        Returns:
            pd.DataFrame: Generated student performance data
        """
        # Reset random seed to ensure reproducibility
        np.random.seed(self.random_seed)

        # Basic demographic information
        student_ids = [f"STU{str(i).zfill(4)}" for i in range(1, self.num_students + 1)]
        ages = np.random.normal(18.5, 1.5, self.num_students).clip(16, 25).astype(int)
        genders = np.random.choice(['Male', 'Female', 'Other'],
                                   self.num_students, p=[0.45, 0.50, 0.05])

        # Socioeconomic factors
        parental_education = np.random.choice(
            ['High School', 'Bachelor', 'Master', 'PhD', 'No Formal Education'],
            self.num_students,
            p=[0.3, 0.35, 0.2, 0.1, 0.05]
        )

        household_income = np.random.lognormal(10.5, 0.8, self.num_students).clip(20000, 200000)

        # Academic history
        previous_gpa = np.random.beta(2, 1, self.num_students) * 4.0  # GPA out of 4.0
        previous_gpa = np.round(previous_gpa, 2)

        # Study habits and behavior
        study_hours_per_week = np.random.gamma(2, 3, self.num_students).clip(1, 40)
        attendance_rate = np.random.beta(5, 1, self.num_students) * 100  # Percentage

        # Health and lifestyle factors
        sleep_hours = np.random.normal(7, 1.2, self.num_students).clip(4, 12)
        exercise_hours_per_week = np.random.exponential(3, self.num_students).clip(0, 20)

        # Technology access
        has_internet = np.random.choice([0, 1], self.num_students, p=[0.1, 0.9])
        has_computer = np.random.choice([0, 1], self.num_students, p=[0.15, 0.85])

        # Extracurricular activities
        extracurricular_hours = np.random.poisson(3, self.num_students).clip(0, 15)

        # School environment
        school_type = np.random.choice(['Public', 'Private'], self.num_students, p=[0.7, 0.3])
        class_size = np.random.normal(25, 5, self.num_students).clip(10, 50).astype(int)

        # Generate final performance score based on multiple factors
        # This creates realistic relationships between variables
        performance_base = (
            previous_gpa * 15 +  # Strong correlation with past performance
            study_hours_per_week * 1.2 +  # Study time matters
            attendance_rate * 0.3 +  # Attendance is important
            sleep_hours * 2 +  # Adequate sleep helps
            exercise_hours_per_week * 0.5 +  # Physical health
            has_internet * 3 +  # Technology access
            has_computer * 4 +  # Computer access
            extracurricular_hours * 0.3 +  # Well-rounded students
            (household_income / 10000) * 0.2 +  # Socioeconomic factor
            np.where(parental_education == 'PhD', 5,
                     np.where(parental_education == 'Master', 3,
                              np.where(parental_education == 'Bachelor', 1, 0))) +
            np.where(school_type == 'Private', 2, 0) +
            (30 - class_size) * 0.1  # Smaller classes are better
        )

        # Add some noise and normalize to 0-100 scale
        noise = np.random.normal(0, 5, self.num_students)
        final_score = performance_base + noise

        # Normalize to 0-100 scale
        final_score = ((final_score - final_score.min()) /
                       (final_score.max() - final_score.min())) * 100
        final_score = np.round(final_score, 2)

        # Create DataFrame
        data = pd.DataFrame({
            'student_id': student_ids,
            'age': ages,
            'gender': genders,
            'parental_education': parental_education,
            'household_income': np.round(household_income, 2),
            'previous_gpa': previous_gpa,
            'study_hours_per_week': np.round(study_hours_per_week, 2),
            'attendance_rate': np.round(attendance_rate, 2),
            'sleep_hours': np.round(sleep_hours, 2),
            'exercise_hours_per_week': np.round(exercise_hours_per_week, 2),
            'has_internet': has_internet,
            'has_computer': has_computer,
            'extracurricular_hours': extracurricular_hours,
            'school_type': school_type,
            'class_size': class_size,
            'final_score': final_score
        })

        return data

    def save_dataset(self, data, filename="student_performance_dataset.csv"):
        """
        Save the dataset to a CSV file.

        Args:
            data (pd.DataFrame): Dataset to save
            filename (str): Name of the output file
        """
        # Create data directory if it doesn't exist
        data_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data')
        os.makedirs(data_dir, exist_ok=True)

        filepath = os.path.join(data_dir, filename)
        data.to_csv(filepath, index=False)
        print(f"Dataset saved to: {filepath}")

        # Print dataset statistics
        print("\nDataset Statistics:")
        print(f"Number of students: {len(data)}")
        print(f"Number of features: {len(data.columns) - 1}")  # Excluding target variable
        print(f"Target variable range: {data['final_score'].min():.2f} - "
              f"{data['final_score'].max():.2f}")
        print(f"Mean final score: {data['final_score'].mean():.2f}")
        print(f"Standard deviation: {data['final_score'].std():.2f}")


if __name__ == "__main__":
    # Generate and save the dataset
    generator = StudentDataGenerator(num_students=500)
    dataset = generator.generate_dataset()
    generator.save_dataset(dataset)

    # Display first few rows
    print("\nFirst 10 rows of the dataset:")
    print(dataset.head(10))

    # Display data types and info
    print("\nDataset Info:")
    print(dataset.info())
