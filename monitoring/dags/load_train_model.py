import mlflow

import pandas as pd
from datetime import datetime, timedelta
from sklearn.ensemble import RandomForestClassifier
from airflow import DAG
from airflow.operators.python_operator import PythonOperator

logged_model = 'runs:/ac628f79a56b49299e6fbd7591dda539/models_mlflow'

# Load model.
loaded_model = mlflow.sklearn.load_model(logged_model)

# Define default arguments for the DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Initialize the DAG
dag = DAG(
    'mTelco churn prediction pipeline',
    default_args=default_args,
    description='telco churn prediction pipeline',
    schedule_interval=timedelta(days=1),
    #start_date=datetime(2023, 1, 1),
    catchup=False,
)

# Define the task functions
def load_data():
     """Load Training and scocring Data"""
    #data = pd.read_csv('/data/')
    # Perform any required data loading steps
     print("Data loaded successfully")

def preprocess_data():
    """process Data""""
    # Preprocess the data (e.g., clean, normalize)
    print("Data preprocessed successfully")


def score_data():
    # Evaluate the trained model
    print("Model evaluated successfully")


# Create tasks using the PythonOperator
load_data_task = PythonOperator(
    task_id='load_data',
    python_callable=load_data,
    dag=dag,
)

preprocess_data_task = PythonOperator(
    task_id='preprocess_data',
    python_callable=preprocess_data,
    dag=dag,
)


score_data_task = PythonOperator(
    task_id='score_data',
    python_callable=evaluate_model,
    dag=dag,
)

# Set the task dependencies
load_data_task >> preprocess_data_task >> score_data_task 
