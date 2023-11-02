# Apache Airflow Data Pipeline with AWS Glue Integration

## Overview

This repository contains an Apache Airflow Directed Acyclic Graph (DAG) that defines a data pipeline integrated with AWS Glue. The pipeline is designed to extract data, transform it, and load it into a data storage facility. Additionally, it includes a monitoring component to ensure that the Glue job execution is complete.

The key components of this data pipeline include:

- **DAG Definition**: The DAG is defined in the `my_dag.py` file. It orchestrates the execution of tasks and specifies the execution logic of the data pipeline.

- **Tasks**: The DAG includes three tasks:
  1. `tsk_glue_job_trigger`: This task triggers an AWS Glue job using the specified Glue job name (`s3_upload_redshift_gluejob`).
  2. `tsk_grab_glue_job_run_id`: This task retrieves the job run ID of the triggered Glue job. It waits for 8 seconds to allow time for the Glue job to start.
  3. `tsk_is_glue_job_finish_running`: This task checks if the Glue job execution is complete. It uses the job run ID obtained from the previous task and monitors the Glue job until it finishes. It also provides verbose logging of Glue job progress.

## DAG Configuration

The DAG is configured with the following parameters:

- `owner`: The owner of the DAG (change as needed).
- `depends_on_past`: The DAG does not depend on the past.
- `start_date`: The start date of DAG execution.
- `email`: Email address for notifications.
- `email_on_failure`: Email notifications on task failure (can be configured).
- `email_on_retry`: Email notifications on task retries (can be configured).
- `retries`: Number of task retries.
- `retry_delay`: Time delay between retries.

## Usage

To use this data pipeline, follow these steps:

1. Clone this repository to your local environment.

2. Install Apache Airflow and its dependencies. You can use the following command to install Airflow with the necessary AWS provider package:
   pip install 'apache-airflow[aws]'

3. Configure your Airflow environment, including connections and variables, to work with your specific AWS resources. Make sure to configure the aws_s3_conn connection in Airflow to access your AWS resources.

4. Use the my_dag.py file as a template and modify it to define your own data pipeline tasks. Customize the Glue job name and any other parameters to match your specific use case.

5. Run the Airflow scheduler and web server:
  airflow webserver --port 8080

6. Access the Airflow web UI to trigger and monitor the execution of your data pipeline.

Feel free to contact me if you have any questions or need assistance with this data pipeline.

Happy data processing!
