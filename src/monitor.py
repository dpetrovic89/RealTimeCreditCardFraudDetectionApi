import pandas as pd
from evidently.report import Report
from evidently.metric_preset import DataDriftPreset, TargetDriftPreset, DataQualityPreset
import os

def check_drift(reference_path, current_path, report_path='monitoring/drift_report.html'):
    """
    Compares two datasets and generates an Evidently AI drift report.
    """
    print(f"Checking drift between {reference_path} and {current_path}...")
    
    reference = pd.read_csv(reference_path)
    current = pd.read_csv(current_path)
    
    # Generate drift report
    report = Report(metrics=[
        DataDriftPreset(),
        TargetDriftPreset(),
        DataQualityPreset()
    ])
    
    report.run(reference_data=reference, current_data=current)
    
    os.makedirs(os.path.dirname(report_path), exist_ok=True)
    report.save_html(report_path)
    print(f"Drift report saved to {report_path}")

if __name__ == "__main__":
    # For demo, we'll compare the data with itself to show a "clean" report
    # or skip if only one file exists
    if os.path.exists('data/creditcard.csv'):
        # Create a mock "current" data with some noise to show drift
        ref = pd.read_csv('data/creditcard.csv')
        cur = ref.copy()
        cur['V1'] = cur['V1'] + 5 # Inject drift
        cur.to_csv('data/creditcard_current.csv', index=False)
        
        check_drift('data/creditcard.csv', 'data/creditcard_current.csv')
