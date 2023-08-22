import boto3
import os
from utils.http_methods import ok_response, bad_request_response

from dotenv import load_dotenv

load_dotenv()

DB_NAME=os.getenv("DB_NAME")
SECRET_ARN=os.getenv("SECRET_ARN")
RESOURCE_ARN=os.getenv("RESOURCE_ARN")

rds_data = boto3.client("rds-data")

def list_users():
    # Replace these with your own RDS Data API configuration
    database = DB_NAME
    secret_arn = SECRET_ARN
    resource_arn = RESOURCE_ARN

    sql_statement = "select * from users;"

    try:
        response = rds_data.execute_statement(
            secretArn=secret_arn,
            resourceArn=resource_arn,
            sql=sql_statement,
            database=database,
            includeResultMetadata=True,
            continueAfterTimeout=True,
        )

        records = response["records"]
        print(records)
        return [
            {
                "id": record[0]["longValue"],
                "username": record[1]["stringValue"],
                "first_name": record[2]["stringValue"],
                "last_name": record[3]["stringValue"],
                "approval_group_id": record[4]["longValue"],
            }
            for record in records
        ]
    except Exception as e:
        print("An error occurred:", e)


def lambda_handler(event, context):
    response= list_users()
    return ok_response(response)