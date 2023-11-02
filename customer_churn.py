from airflow import DAG
from datetime import timedelta, datetime
from airflow.operators.python import PythonOperator
from airflow.providers.amazon.aws.hooks.base_aws import AwsGenericHook
import time
from airflow.providers.amazon.aws.sensors.glue import GlueJobSensor

# Define a function to trigger an AWS Glue job
def glue_job_s3_redshift_transfer(job_name, **kwargs):
    """
    Triggers an AWS Glue job to transfer data from S3 to Redshift.

    Args:
        job_name (str): The name of the AWS Glue job to trigger.
        **kwargs: Additional keyword arguments.

    Returns:
        None
    """
    # Create a connection to AWS S3
    session = AwsGenericHook(aws_conn_id='aws_s3_conn')
      
    # Get a Boto3 session in the same region as the Glue job
    boto3_session = session.get_session(region_name='eu-west-2')
    
    # Trigger the Glue job using its name
    client = boto3_session.client('glue')
    client.start_job_run(
        JobName=job_name,
    )

# Define a function to get the run ID of the Glue job
def get_run_id():
    """
    Gets the run ID of the last executed AWS Glue job.

    Returns:
        str: The run ID of the Glue job.
    """
    # Wait for 8 seconds to allow the Glue job to start
    time.sleep(8)

    # Create a connection to AWS S3
    session = AwsGenericHook(aws_conn_id='aws_s3_conn')
    boto3_session = session.get_session(region_name='eu-west-2')

    # Retrieve the run ID of the Glue job
    glue_client = boto3_session.client('glue')
    response = glue_client.get_job_runs(JobName="s3_upload_redshift_gluejob")
    job_run_id = response["JobRuns"][0]["Id"]
    return job_run_id 

# Define default arguments for the DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2023, 8, 1),
    'email': ['myemail@domain.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 2,
    'retry_delay': timedelta(seconds=15)
}

# Create an Apache Airflow DAG
with DAG('my_dag',
        default_args=default_args,
        schedule_interval = '@weekly',    # Set the schedule interval
        catchup=False) as dag:    # Disable catchup to avoid backfilling

        # Define PythonOperator to trigger Glue job
        glue_job_trigger = PythonOperator(
        task_id='tsk_glue_job_trigger',
        python_callable=glue_job_s3_redshift_transfer,
        op_kwargs={
            'job_name': 's3_upload_redshift_gluejob'
        },
        )

        # Define PythonOperator to get Glue job run ID
        grab_glue_job_run_id = PythonOperator(
        task_id='tsk_grab_glue_job_run_id',
        python_callable=get_run_id,
        )

        # Define GlueJobSensor to monitor Glue job completion
        is_glue_job_finish_running = GlueJobSensor(
        task_id="tsk_is_glue_job_finish_running",      
        job_name='s3_upload_redshift_gluejob',
        run_id='{{task_instance.xcom_pull("tsk_grab_glue_job_run_id")}}',
        verbose=True,  # prints glue job logs in airflow logs
        aws_conn_id='aws_s3_conn',
        poke_interval=60,
        timeout=3600,
        )

        # Define task dependencies
        glue_job_trigger >> grab_glue_job_run_id >> is_glue_job_finish_running

