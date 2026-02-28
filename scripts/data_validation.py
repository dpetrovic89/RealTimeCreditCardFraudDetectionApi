import pandas as pd
import sys
import os

def validate_data(file_path):
    if not os.path.exists(file_path):
        print(f"Error: {file_path} not found.")
        sys.exit(1)
        
    df = pd.read_csv(file_path)
    print(f"Validating dataset from {file_path}...")
    
    errors = []
    
    # 1. Existence of columns
    expected_columns = [f'V{i}' for i in range(1, 29)] + ['Time', 'Amount', 'Class']
    for col in expected_columns:
        if col not in df.columns:
            errors.append(f"Missing column: {col}")
            
    if errors:
        print("Validation FAILED with following errors:")
        for err in errors:
            print(f"- {err}")
        sys.exit(1)
        
    # 2. Null checks
    null_counts = df.isnull().sum()
    if null_counts.any():
        for col, count in null_counts[null_counts > 0].items():
            errors.append(f"Column {col} has {count} null values")

    # 3. Range checks for Class
    if not df['Class'].isin([0, 1]).all():
        errors.append("Column 'Class' contains values other than 0 or 1")
        
    # 4. Range checks for Amount
    if (df['Amount'] < 0).any():
        errors.append("Column 'Amount' contains negative values")

    if errors:
        print("Validation FAILED:")
        for err in errors:
            print(f"- {err}")
        sys.exit(1)
        
    print("Data validation PASSED ✅")

if __name__ == "__main__":
    validate_data('data/creditcard.csv')
