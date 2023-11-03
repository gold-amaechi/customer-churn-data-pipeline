# Apache Airflow Data Pipeline with AWS Glue Integration

## Overview

This repository contains an Apache Airflow Directed Acyclic Graph (DAG) that defines a data pipeline integrated with Aamazon Web Services (AWS) Glue. The pipeline is designed to extract data, transform it and load. It creates a Glue job to crawl an Amazon S3 bucket and load to Amazon Redshift (orchestrated using Airflow), then connects Amazon Redshift to Power BI for visualisation. Additionally, it includes a monitoring component to ensure that the Glue job execution is complete. 

The key components of this data pipeline include:

- **DAG Definition**: The DAG is defined in the `customer_churn.py` file. It orchestrates the execution of tasks and specifies the execution logic of the data pipeline.

- **Tasks**: The DAG includes three tasks:
  1. `tsk_glue_job_trigger`: This task triggers an AWS Glue job using the specified Glue job name (`s3_upload_redshift_gluejob`).
  2. `tsk_grab_glue_job_run_id`: This task retrieves the job run ID of the triggered Glue job. It waits for 8 seconds to allow time for the Glue job to start.
  3. `tsk_is_glue_job_finish_running`: This task checks if the Glue job execution is complete. It uses the job run ID obtained from the previous task and monitors the Glue job until it finishes. It also provides verbose logging of Glue job progress.

## Usage

To use this data pipeline, follow these steps:

1. Clone this repository to your local environment.
   
2. Obtain the telco customer churn dataset from kaggle, save as csv file instead of xlsx (this makes life easier when creating your S3 data source).

3. Create an AWS account.

4. Launch an EC2 instance, use Ubuntu, you'll need a t2 medium instance type because Airflow might freeze and act up with a samller size (but you will have to pay for this), and create a key pair, allow HTTP & SSH traffic.

5. EC2 connect to open your terminal, then install dependencies:
      - sudo apt update : To update
      - sudo apt install python3-pip : To install pip
      - sudo apt install python3.10-venv : To instal virtual environment
      - python3 -m venv 'insert_your_virtual_environment_name_here'_venv : To create your virtual environment
      - source customer_churn_youtube_venv/bin/activate : To activate your virtual environment
      - sudo pip install apache-airflow : To install Airflow
      - pip install apache-airflow-providers-amazon : You need this provider because you will be interacting with AWS services
      - First, pip install --upgrade awscli, then aws configure : You will need AWS access key, secret access key and to know your region
      - airflow standalone : To activate Airflow, make note of your user name and password

6. Copy Public IPV4 from your EC2 instance, edit inbound rules to give permission to port 8080. Paste the IPV4 in a new tab, add :8080 to the end, you can now access the airflow U.I.

7. Login with your airflow user name and password.

8. Remotely SSH (connect) Visual Studio Code to AWS.

9. Create your S3 bucket, make sure it has a globally unique name and has the same region as your EC2 instance.

10. Upload your csv file to the S3 bucket.

11. Create a glue crawler for the S3 bucket, this will crawl the dataset and infer schema (it will get headers, etc.).

12. Ceate a database to temporarily store data from the S3 bucket, the glue crawler will create a table.

13. Create a Redshift cluster, make note of your user name and password; then create a table on the Redshift cluster, choosing only the columns that you want to use. You will also need to create a connection between the Glue and Redshift and to create a second Glue crawler for the Redshift cluster. Make sure to enable endpoint services.

14. Create a glue job to bind the two crawlers together.

15. The customer_churn.py file defines the data pipeline tasks we mentioned earlier. Customise the Glue job name and any other parameters to match your specific use case.

16. Refresh your airflow U.I. to see the DAGs created.

17. Create a connection between Airflow and AWS services, this can be done by navigating to the admin section in your Airflow U.I. and clicking connection.

18. You should now be able to trigger and monitor the execution of your data pipeline from the Airflow U.I.

Feel free to contact me if you have any questions or need assistance with this data pipeline.

Happy data processing!
