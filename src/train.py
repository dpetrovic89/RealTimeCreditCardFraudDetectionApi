import pandas as pd
import lightgbm as lgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, average_precision_score, confusion_matrix
import mlflow
import mlflow.lightgbm
import dagshub
import os

def train_model():
    # 1. Setup DagsHub/MLflow if credentials exist
    # For recruiters/users: Set these in your environment
    # DAGSHUB_REPO_OWNER, DAGSHUB_REPO_NAME, MLFLOW_TRACKING_URI, etc.
    if os.environ.get('DAGSHUB_TOKEN'):
        try:
            dagshub.init(
                repo_owner=os.environ.get('DAGSHUB_REPO_OWNER', 'user'),
                repo_name=os.environ.get('DAGSHUB_REPO_NAME', 'RealTimeCreditCardFraudDetectionApi'),
                mlflow=True
            )
            print("DagsHub MLflow integration initialized.")
        except Exception as e:
            print(f"DagsHub init failed: {e}. Falling back to local MLflow.")
    
    # Enable autologging
    mlflow.lightgbm.autolog()

    # 2. Load and Prepare Data
    print("Loading data...")
    df = pd.read_csv('data/creditcard.csv')
    X = df.drop(['Class', 'Time'], axis=1) # Drop Time as it might be a leak or irrelevant without more context
    y = df['Class']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, stratify=y, random_state=42)

    # 3. Handle Class Imbalance using LightGBM's is_unbalance=True
    # or scale_pos_weight = count(neg) / count(pos)
    scale_pos_weight = (y_train == 0).sum() / (y_train == 1).sum()

    with mlflow.start_run(run_name="LightGBM_Fraud_Detection"):
        print("Starting training...")
        params = {
            "objective": "binary",
            "metric": "auc",
            "is_unbalance": False, # We'll use scale_pos_weight for more control
            "scale_pos_weight": scale_pos_weight,
            "learning_rate": 0.05,
            "num_leaves": 31,
            "feature_fraction": 0.9,
            "bagging_fraction": 0.8,
            "bagging_freq": 5,
            "verbose": -1
        }
        
        train_data = lgb.Dataset(X_train, label=y_train)
        valid_data = lgb.Dataset(X_test, label=y_test, reference=train_data)

        model = lgb.train(
            params,
            train_data,
            valid_sets=[train_data, valid_data],
            valid_names=['train', 'valid'],
            num_boost_round=1000,
            callbacks=[lgb.early_stopping(stopping_rounds=50)]
        )

        # 4. Evaluation
        y_pred_prob = model.predict(X_test)
        y_pred = (y_pred_prob > 0.5).astype(int)

        print("\nClassification Report:")
        print(classification_report(y_test, y_pred))
        
        auprc = average_precision_score(y_test, y_pred_prob)
        print(f"AUPRC: {auprc:.4f}")
        
        # Log manual metrics not captured by autolog
        mlflow.log_metric("auprc", auprc)
        
        # Save model locally for the next phase
        model.save_model('src/model.txt')
        print("Model saved to src/model.txt")

if __name__ == "__main__":
    train_model()
