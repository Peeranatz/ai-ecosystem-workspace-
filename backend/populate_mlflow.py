import sys
import mlflow

# Set UTF-8 stdout
sys.stdout.reconfigure(encoding='utf-8')

mlflow.set_tracking_uri("http://localhost:5000")
mlflow.set_experiment("conll2003_ner")

print("Logging Run 1...")
with mlflow.start_run(run_name="training_run_job_001"):
    mlflow.log_params({
        "job_id": "job_001",
        "dataset_name": "conll2003",
        "base_model": "bert-base-cased",
        "learning_rate": 0.00002,
        "batch_size": 16,
        "epochs": 3,
        "framework": "PyTorch / Transformers"
    })
    mlflow.log_metrics({
        "final_loss": 0.0621,
        "token_accuracy": 0.981,
        "f1_score": 0.965
    })
    mlflow.log_text("Model Metadata Version 1", "model_metadata.json")

print("Logging Run 2...")
with mlflow.start_run(run_name="training_run_job_002"):
    mlflow.log_params({
        "job_id": "job_002",
        "dataset_name": "wikiann",
        "base_model": "bert-base-uncased",
        "learning_rate": 0.00001,
        "batch_size": 32,
        "epochs": 5,
        "framework": "PyTorch / Transformers"
    })
    mlflow.log_metrics({
        "final_loss": 0.0415,
        "token_accuracy": 0.989,
        "f1_score": 0.978
    })
    mlflow.log_text("Model Metadata Version 2", "model_metadata.json")

print("Successfully logged runs to MLflow Tracking Server!")
