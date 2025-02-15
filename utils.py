import pandas as pd
import numpy as np
from datetime import datetime
import logging

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def validate_data(df):
    """Validate input data for required columns and data types"""
    required_columns = [
        'customer_id', 'age', 'income', 'employment_length',
        'credit_score', 'debt_to_income', 'num_credit_lines',
        'num_late_payments', 'loan_amount'
    ]
    
    # Check for required columns
    missing_columns = set(required_columns) - set(df.columns)
    if missing_columns:
        raise ValueError(f"Missing required columns: {missing_columns}")
    
    # Validate data types and ranges
    validation_rules = {
        'age': {'type': np.number, 'min': 18, 'max': 100},
        'income': {'type': np.number, 'min': 0},
        'credit_score': {'type': np.number, 'min': 300, 'max': 850},
        'debt_to_income': {'type': np.number, 'min': 0, 'max': 1},
        'loan_amount': {'type': np.number, 'min': 0}
    }
    
    for column, rules in validation_rules.items():
        # Check data type
        if not np.issubdtype(df[column].dtype, rules['type']):
            raise TypeError(f"Column {column} must be numeric")
        
        # Check ranges
        if 'min' in rules and df[column].min() < rules['min']:
            logger.warning(f"Values in {column} below minimum {rules['min']}")
        if 'max' in rules and df[column].max() > rules['max']:
            logger.warning(f"Values in {column} above maximum {rules['max']}")
    
    return True

def calculate_financial_metrics(df):
    """Calculate key financial metrics from the data"""
    metrics = {
        'total_loan_volume': df['loan_amount'].sum(),
        'average_loan_size': df['loan_amount'].mean(),
        'total_customers': len(df),
        'average_income': df['income'].mean(),
        'average_credit_score': df['credit_score'].mean(),
        'high_risk_ratio': (df['risk_category'] == 'High Risk').mean(),
        'approval_rate': (df['risk_category'] != 'High Risk').mean()
    }
    
    return metrics

def detect_anomalies(df, columns, threshold=3):
    """Detect anomalies in specified columns using Z-score method"""
    anomalies = {}
    
    for column in columns:
        if np.issubdtype(df[column].dtype, np.number):
            z_scores = np.abs((df[column] - df[column].mean()) / df[column].std())
            anomalies[column] = df[z_scores > threshold].index.tolist()
    
    return anomalies

def generate_summary_report(df, metrics, anomalies):
    """Generate a summary report of the analysis"""
    report = {
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'data_summary': {
            'total_records': len(df),
            'time_period': f"{df['application_date'].min()} to {df['application_date'].max()}"
        },
        'key_metrics': metrics,
        'risk_distribution': df['risk_category'].value_counts().to_dict(),
        'anomalies_detected': {
            col: len(indices) for col, indices in anomalies.items()
        }
    }
    
    return report

def save_report(report, filepath='reports/summary_report.json'):
    """Save the summary report to a JSON file"""
    import json
    import os
    
    # Create reports directory if it doesn't exist
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    
    with open(filepath, 'w') as f:
        json.dump(report, f, indent=4)
    
    logger.info(f"Report saved to {filepath}")
