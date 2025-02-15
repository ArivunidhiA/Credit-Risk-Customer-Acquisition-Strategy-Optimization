import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix
import pickle

class CreditRiskModel:
    def __init__(self):
        self.model = RandomForestClassifier(
            n_estimators=100,
            max_depth=10,
            random_state=42
        )
        self.feature_columns = [
            'age', 'income', 'employment_length', 'credit_score',
            'debt_to_income', 'num_credit_lines', 'num_late_payments',
            'loan_amount', 'risk_score'
        ]
    
    def prepare_features(self, df):
        """Prepare features for model training"""
        return df[self.feature_columns]
    
    def train(self, df):
        """Train the credit risk model"""
        X = self.prepare_features(df)
        y = df['default']
        
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )
        
        # Train model
        self.model.fit(X_train, y_train)
        
        # Evaluate model
        train_score = self.model.score(X_train, y_train)
        test_score = self.model.score(X_test, y_test)
        
        print(f"Train accuracy: {train_score:.3f}")
        print(f"Test accuracy: {test_score:.3f}")
        
        # Generate detailed classification report
        y_pred = self.model.predict(X_test)
        print("\nClassification Report:")
        print(classification_report(y_test, y_pred))
        
        return X_test, y_test, y_pred
    
    def predict_risk(self, customer_data):
        """Predict risk for new customers"""
        features = self.prepare_features(customer_data)
        predictions = self.model.predict_proba(features)
        
        # Add prediction probabilities to customer data
        customer_data['default_probability'] = predictions[:, 1]
        customer_data['risk_category'] = pd.qcut(
            customer_data['default_probability'],
            q=3,
            labels=['Low Risk', 'Medium Risk', 'High Risk']
        )
        
        return customer_data
    
    def save_model(self, filepath='models/credit_risk_model.pkl'):
        """Save the trained model"""
        with open(filepath, 'wb') as f:
            pickle.dump(self.model, f)
        print(f"Model saved to {filepath}")

def calculate_business_metrics(df_with_predictions):
    """Calculate business-relevant metrics"""
    metrics = {
        'total_customers': len(df_with_predictions),
        'high_risk_ratio': (df_with_predictions['risk_category'] == 'High Risk').mean(),
        'low_risk_ratio': (df_with_predictions['risk_category'] == 'Low Risk').mean(),
        'average_default_probability': df_with_predictions['default_probability'].mean(),
        'potential_revenue': (
            df_with_predictions[df_with_predictions['risk_category'] != 'High Risk']['loan_amount'].sum()
        )
    }
    
    return metrics

if __name__ == "__main__":
    # Load processed data
    df = pd.read_csv('data/processed_credit_data.csv')
    
    # Initialize and train model
    risk_model = CreditRiskModel()
    X_test, y_test, y_pred = risk_model.train(df)
    
    # Make predictions on entire dataset
    df_with_predictions = risk_model.predict_risk(df)
    
    # Calculate and display business metrics
    metrics = calculate_business_metrics(df_with_predictions)
    print("\nBusiness Metrics:")
    for metric, value in metrics.items():
        print(f"{metric}: {value:,.2f}")
    
    # Save model
    risk_model.save_model()
