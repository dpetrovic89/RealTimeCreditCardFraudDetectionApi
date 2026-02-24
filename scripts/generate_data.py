import pandas as pd
import numpy as np

def generate_mock_data(n_samples=10000):
    """
    Generates a mock credit card fraud dataset since downloading from Kaggle 
    requires authentication. This ensures the pipeline is 100% free and runnable.
    """
    np.random.seed(42)
    
    # Feature columns (V1-V28 are PCA transformed features in the real dataset)
    data = {f'V{i}': np.random.randn(n_samples) for i in range(1, 29)}
    
    # Time and Amount
    data['Time'] = np.sort(np.random.uniform(0, 172792, n_samples))
    data['Amount'] = np.random.exponential(scale=88, size=n_samples)
    
    # Class (0: Normal, 1: Fraud) - Imbalanced (0.17% fraud in real dataset)
    data['Class'] = np.random.choice([0, 1], size=n_samples, p=[0.9983, 0.0017])
    
    df = pd.DataFrame(data)
    df.to_csv('data/creditcard.csv', index=False)
    print("Mock dataset generated at data/creditcard.csv")

if __name__ == "__main__":
    generate_mock_data()
