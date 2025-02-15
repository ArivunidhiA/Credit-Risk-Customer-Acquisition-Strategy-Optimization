import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from datetime import datetime

def generate_synthetic_data(n_samples=1000):
    """Generate synthetic credit data for demonstration"""
    np.random.seed(42)
    
    data = {
        'customer_id': range(1, n_samples + 1),
        'age': np.random.normal(35, 10, n_samples).astype(int),
        'income': np.random.normal(60000, 20000, n_samples),
        'employment_length': np.random.normal(5, 3, n_samples),
        'credit_score': np.random.normal(700, 50, n_samples),
        'debt_to_income': np.random.normal(0.3, 0.1, n_samples),
        'num_credit_lines': np.random.normal(5, 2, n_samples).astype(int),
        'num_late_payments': np.random.poisson(0.5, n_samples),
        'loan_amount': np.random.normal(15000, 5000, n_samples),
        'default': np.random.binomial(1, 0.15, n_samples)
    }
    
    df = pd.DataFrame(data)
    
    # Clean and constrain the data to realistic values
    df['age'] = df['age'].clip(18, 80)
    df['income'] = df['income'].clip(20000, 200000)
    df['employment_length'] = df['employment_length'].clip(0, 40)
    df['credit_score'] = df['credit_score'].clip(300, 850)
    df['debt_to_income'] = df['debt_to_income'].clip(0, 1)
    df['num_credit_lines'] = df['num_credit_lines'].clip(0, 20)
    df['num_late_payments'] = df['num_late_payments'].clip(0, 10)
    df['loan_amount'] = df['loan_amount'].clip(1000, 50000)
    
    return df

def preprocess_data(df):
    """Preprocess the credit data for modeling"""
    # Create copy to avoid modifying original data
    df_processed = df.copy()
    
    # Feature engineering
    df_processed['risk_score'] = (
        df_processed['credit_score'] * 0.5 +
        (1 - df_processed['debt_to_income']) * 100 * 0.3 +
        (1 - df_processed['num_late_payments'] / 10) * 100 * 0.2
    )
    
    # Create customer segments
    df_processed['customer_segment'] = pd.qcut(
        df_processed['risk_score'],
        q=3,
        labels=['high_risk', 'medium_risk', 'low_risk']
    )
    
    # Standardize numerical features
    numerical_features = ['age', 'income', 'employment_length', 'credit_score',
                         'debt_to_income', 'num_credit_lines', 'loan_amount']
    
    scaler = StandardScaler()
    df_processed[numerical_features] = scaler.fit_transform(df_processed[numerical_features])
    
    return df_processed

def save_processed_data(df, output_path='data/processed_credit_data.csv'):
    """Save processed data to CSV"""
    df.to_csv(output_path, index=False)
    print(f"Processed data saved to {output_path}")

if __name__ == "__main__":
    # Generate synthetic data
    raw_data = generate_synthetic_data(n_samples=10000)
    print("Generated synthetic data with shape:", raw_data.shape)
    
    # Process the data
    processed_data = preprocess_data(raw_data)
    print("Processed data with shape:", processed_data.shape)
    
    # Save the data
    save_processed_data(processed_data)
