"""
Student Performance Regression Model
Machine Learning model to predict student academic performance.
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
import joblib
import os
from datetime import datetime


class StudentPerformanceModel:
    """Regression model for predicting student performance."""
    
    def __init__(self):
        """Initialize the model."""
        self.model = None
        self.scaler = StandardScaler()
        self.label_encoders = {}
        self.feature_columns = None
        self.target_column = 'final_score'
        self.model_metrics = {}
    
    def preprocess_data(self, data):
        """
        Preprocess the data for training/prediction.
        
        Args:
            data (pd.DataFrame): Raw data
            
        Returns:
            pd.DataFrame: Preprocessed data
        """
        # Create a copy to avoid modifying original data
        processed_data = data.copy()
        
        # Handle categorical variables
        categorical_columns = ['gender', 'parental_education', 'school_type']
        
        for col in categorical_columns:
            if col in processed_data.columns:
                if col not in self.label_encoders:
                    self.label_encoders[col] = LabelEncoder()
                    processed_data[col] = self.label_encoders[col].fit_transform(processed_data[col])
                else:
                    # For prediction on new data
                    processed_data[col] = self.label_encoders[col].transform(processed_data[col])
        
        return processed_data
    
    def prepare_features(self, data):
        """
        Prepare features for training/prediction.
        
        Args:
            data (pd.DataFrame): Preprocessed data
            
        Returns:
            tuple: (X, y) features and target
        """
        # Define feature columns (excluding student_id and target)
        exclude_columns = ['student_id', self.target_column]
        
        if self.feature_columns is None:
            self.feature_columns = [col for col in data.columns if col not in exclude_columns]
        
        X = data[self.feature_columns]
        y = data[self.target_column] if self.target_column in data.columns else None
        
        return X, y
    
    def train(self, data, model_type='random_forest'):
        """
        Train the regression model.
        
        Args:
            data (pd.DataFrame): Training data
            model_type (str): Type of model ('linear' or 'random_forest')
        """
        print("Starting model training...")
        
        # Preprocess data
        processed_data = self.preprocess_data(data)
        
        # Prepare features
        X, y = self.prepare_features(processed_data)
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )
        
        # Scale features
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)
        
        # Initialize model
        if model_type == 'linear':
            self.model = LinearRegression()
        else:
            self.model = RandomForestRegressor(
                n_estimators=100,
                random_state=42,
                max_depth=10,
                min_samples_split=5
            )
        
        # Train model
        if model_type == 'linear':
            self.model.fit(X_train_scaled, y_train)
            y_pred = self.model.predict(X_test_scaled)
        else:
            self.model.fit(X_train, y_train)
            y_pred = self.model.predict(X_test)
        
        # Evaluate model
        mse = mean_squared_error(y_test, y_pred)
        rmse = np.sqrt(mse)
        mae = mean_absolute_error(y_test, y_pred)
        r2 = r2_score(y_test, y_pred)
        
        # Store metrics
        self.model_metrics = {
            'mse': mse,
            'rmse': rmse,
            'mae': mae,
            'r2_score': r2,
            'model_type': model_type,
            'training_date': datetime.now().isoformat(),
            'train_size': len(X_train),
            'test_size': len(X_test)
        }
        
        print(f"Model Training Complete!")
        print(f"Model Type: {model_type}")
        print(f"Mean Squared Error: {mse:.4f}")
        print(f"Root Mean Squared Error: {rmse:.4f}")
        print(f"Mean Absolute Error: {mae:.4f}")
        print(f"R² Score: {r2:.4f}")
        
        # Feature importance for Random Forest
        if model_type == 'random_forest':
            feature_importance = pd.DataFrame({
                'feature': self.feature_columns,
                'importance': self.model.feature_importances_
            }).sort_values('importance', ascending=False)
            
            print("\nTop 10 Most Important Features:")
            print(feature_importance.head(10))
            
            self.model_metrics['feature_importance'] = feature_importance.to_dict('records')
    
    def predict(self, data):
        """
        Make predictions using the trained model.
        
        Args:
            data (pd.DataFrame): Data to predict on
            
        Returns:
            np.array: Predictions
        """
        if self.model is None:
            raise ValueError("Model not trained yet. Call train() first.")
        
        # Preprocess data
        processed_data = self.preprocess_data(data)
        
        # Prepare features
        X, _ = self.prepare_features(processed_data)
        
        # Scale features if using linear regression
        if isinstance(self.model, LinearRegression):
            X = self.scaler.transform(X)
        
        # Make predictions
        predictions = self.model.predict(X)
        
        return predictions
    
    def save_model(self, model_dir="../models"):
        """
        Save the trained model and preprocessors.
        
        Args:
            model_dir (str): Directory to save the model
        """
        if self.model is None:
            raise ValueError("No model to save. Train the model first.")
        
        # Create models directory if it doesn't exist
        if not os.path.isabs(model_dir):
            model_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'models')
        os.makedirs(model_dir, exist_ok=True)
        
        # Save model
        model_path = os.path.join(model_dir, 'student_performance_model.joblib')
        joblib.dump(self.model, model_path)
        
        # Save scaler
        scaler_path = os.path.join(model_dir, 'scaler.joblib')
        joblib.dump(self.scaler, scaler_path)
        
        # Save label encoders
        encoders_path = os.path.join(model_dir, 'label_encoders.joblib')
        joblib.dump(self.label_encoders, encoders_path)
        
        # Save feature columns and metrics
        metadata = {
            'feature_columns': self.feature_columns,
            'target_column': self.target_column,
            'metrics': self.model_metrics
        }
        metadata_path = os.path.join(model_dir, 'model_metadata.joblib')
        joblib.dump(metadata, metadata_path)
        
        print(f"Model saved to: {model_dir}")
    
    def load_model(self, model_dir="../models"):
        """
        Load a trained model and preprocessors.
        
        Args:
            model_dir (str): Directory containing the model files
        """
        if not os.path.isabs(model_dir):
            model_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'models')
        
        # Load model
        model_path = os.path.join(model_dir, 'student_performance_model.joblib')
        self.model = joblib.load(model_path)
        
        # Load scaler
        scaler_path = os.path.join(model_dir, 'scaler.joblib')
        self.scaler = joblib.load(scaler_path)
        
        # Load label encoders
        encoders_path = os.path.join(model_dir, 'label_encoders.joblib')
        self.label_encoders = joblib.load(encoders_path)
        
        # Load metadata
        metadata_path = os.path.join(model_dir, 'model_metadata.joblib')
        metadata = joblib.load(metadata_path)
        self.feature_columns = metadata['feature_columns']
        self.target_column = metadata['target_column']
        self.model_metrics = metadata['metrics']
        
        print(f"Model loaded from: {model_dir}")
        print(f"Model type: {self.model_metrics.get('model_type', 'unknown')}")
        print(f"R² Score: {self.model_metrics.get('r2_score', 'unknown')}")


def main():
    """Main function to demonstrate model training."""
    # Load data
    data_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'student_performance_dataset.csv')
    
    if not os.path.exists(data_path):
        print("Dataset not found. Generating dataset...")
        from data_generator import StudentDataGenerator
        generator = StudentDataGenerator(num_students=500)
        data = generator.generate_dataset()
        generator.save_dataset(data)
    else:
        data = pd.read_csv(data_path)
    
    print(f"Loaded dataset with {len(data)} students")
    
    # Initialize and train model
    model = StudentPerformanceModel()
    
    # Train with Random Forest (better performance)
    model.train(data, model_type='random_forest')
    
    # Save the trained model
    model.save_model()
    
    # Make sample predictions
    sample_data = data.head(5).copy()
    predictions = model.predict(sample_data)
    
    print("\nSample Predictions:")
    for i, (actual, predicted) in enumerate(zip(sample_data['final_score'], predictions)):
        print(f"Student {i+1}: Actual = {actual:.2f}, Predicted = {predicted:.2f}")


if __name__ == "__main__":
    main()