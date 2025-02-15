import pandas as pd
import numpy as np
from datetime import datetime, timedelta

class StrategyTester:
    def __init__(self, data):
        self.data = data
        self.baseline_metrics = None
        self.test_metrics = None
    
    def calculate_strategy_metrics(self, df):
        """Calculate key performance metrics for a strategy"""
        metrics = {
            'approval_rate': (df['risk_category'] != 'High Risk').mean(),
            'expected_default_rate': df['default_probability'].mean(),
            'average_loan_amount': df[df['risk_category'] != 'High Risk']['loan_amount'].mean(),
            'total_loan_volume': df[df['risk_category'] != 'High Risk']['loan_amount'].sum(),
            'low_risk_ratio': (df['risk_category'] == 'Low Risk').mean()
        }
        
        # Calculate expected profit (simplified model)
        interest_rate = 0.1  # 10% interest rate
        default_loss_ratio = 0.5  # Recover 50% of defaulted loans
        
        expected_profit = (
            metrics['total_loan_volume'] * interest_rate * (1 - metrics['expected_default_rate']) -
            metrics['total_loan_volume'] * metrics['expected_default_rate'] * default_loss_ratio
        )
        
        metrics['expected_profit'] = expected_profit
        
        return metrics
    
    def run_ab_test(self, strategy_function, test_size=0.5):
        """Run A/B test comparing baseline to new strategy"""
        # Split data into control and test groups
        np.random.seed(42)
        mask = np.random.random(len(self.data)) < test_size
        
        control_group = self.data[~mask].copy()
        test_group = self.data[mask].copy()
        
        # Apply new strategy to test group
        test_group = strategy_function(test_group)
        
        # Calculate metrics for both groups
        self.baseline_metrics = self.calculate_strategy_metrics(control_group)
        self.test_metrics = self.calculate_strategy_metrics(test_group)
        
        # Calculate relative improvements
        improvements = {}
        for metric in self.baseline_metrics.keys():
            relative_change = (
                (self.test_metrics[metric] - self.baseline_metrics[metric]) /
                self.baseline_metrics[metric]
            ) * 100
            improvements[metric] = relative_change
        
        return improvements

def conservative_strategy(df):
    """Example strategy: More conservative credit policy"""
    df = df.copy()
    
    # Adjust risk categories based on stricter criteria
    df.loc[df['credit_score'] < 650, 'risk_category'] = 'High Risk'
    df.loc[df['debt_to_income'] > 0.4, 'risk_category'] = 'High Risk'
    
    return df

def aggressive_strategy(df):
    """Example strategy: More aggressive credit policy"""
    df = df.copy()
    
    # Adjust risk categories based on looser criteria
    df.loc[df['income'] > 80000, 'risk_category'] = 'Low Risk'
    df.loc[df['credit_score'] > 700, 'risk_category'] = 'Low Risk'
    
    return df

if __name__ == "__main__":
    # Load data with risk predictions
    df = pd.read_csv('data/processed_credit_data.csv')
    
    # Initialize strategy tester
    tester = StrategyTester(df)
    
    # Test conservative strategy
    print("\nTesting Conservative Strategy:")
    conservative_results = tester.run_ab_test(conservative_strategy)
    for metric, change in conservative_results.items():
        print(f"{metric}: {change:+.2f}%")
    
    # Test aggressive strategy
    print("\nTesting Aggressive Strategy:")
    aggressive_results = tester.run_ab_test(aggressive_strategy)
    for metric, change in aggressive_results.items():
        print(f"{metric}: {+.2f}%")
