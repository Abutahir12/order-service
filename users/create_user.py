import boto3
import json
import os

from dotenv import load_dotenv

load_dotenv('.env')

DB_NAME=os.getenv("DB_NAME")
SECRET_ARN=os.getenv("SECRET_ARN")
RESOURCE_ARN=os.getenv("RESOURCE_ARN")
def create_user_with_rds_data_api(username, first_name, last_name=None, approval_group_id=None):
    # Replace these with your own RDS Data API configuration
    database = DB_NAME
    secret_arn = SECRET_ARN
    resource_arn = RESOURCE_ARN

    rds_data = boto3.client("rds-data")

    # Construct the SQL statement
    sql_statement = (
        "INSERT INTO users (username, first_name, last_name, approval_group) "
        "VALUES (:username, :first_name, :last_name, :approval_group_id)"
    )
    sql_statement = "select * from information_schema.tables;"

    try:
        response = rds_data.execute_statement(
            secretArn=secret_arn,
            resourceArn=resource_arn,
            sql=sql_statement,
            database=database
        )

        print(response)
        
        if response["numberOfRecordsUpdated"] == 1:
            print("User created successfully!")
        else:
            print("Failed to create user.")
    except Exception as e:
        print("An error occurred:", e)

# Example usage
username = "unique_username"
first_name = "John"
last_name = "Doe"
approval_group = "group_xyz"

def lambda_handler(event, context):
    create_user_with_rds_data_api(username, first_name, last_name, approval_group)
