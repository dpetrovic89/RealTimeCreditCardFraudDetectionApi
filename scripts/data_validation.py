import great_expectations as ge
import pandas as pd
import sys

def validate_data(file_path):
    df = ge.dataset.PandasDataset(pd.read_csv(file_path))
    
    # Validation Suite
    # 1. Existence of columns
    expected_columns = [f'V{i}' for i in range(1, 29)] + ['Time', 'Amount', 'Class']
    for col in expected_columns:
        df.expect_column_to_exist(col)
        
    # 2. Type checks
    df.expect_column_values_to_be_in_type_list('Class', ['int', 'int64'])
    
    # 3. Range checks
    df.expect_column_values_to_be_between('Class', 0, 1)
    df.expect_column_values_to_be_between('Amount', 0, None) # Amount cannot be negative
    
    # 4. Null checks
    for col in expected_columns:
        df.expect_column_values_to_not_be_null(col)
        
    results = df.validate()
    
    if not results['success']:
        print("Data validation FAILED")
        # Print failed expectations for debugging
        for res in results['results']:
            if not res['success']:
                print(f"Failed: {res['expectation_config']['expectation_type']} on {res['expectation_config']['kwargs'].get('column')}")
        sys.exit(1)
        
    print("Data validation PASSED")

if __name__ == "__main__":
    validate_data('data/creditcard.csv')
