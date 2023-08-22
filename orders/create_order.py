import boto3
import os
import uuid

from dotenv import load_dotenv
from utils.http_methods import (
    ok_response,
    bad_request_response,
    internal_server_error_response,
)
from utils.constants import ORDER_STATUS

load_dotenv()

DB_NAME = os.getenv("DB_NAME")
SECRET_ARN = os.getenv("SECRET_ARN")
RESOURCE_ARN = os.getenv("RESOURCE_ARN")

rds_data = boto3.client("rds-data")


def insert_order_values(created_by):
    # Replace these with your own RDS Data API configuration
    database = DB_NAME
    secret_arn = SECRET_ARN
    resource_arn = RESOURCE_ARN

    new_order_id = uuid.uuid4()
    # Construct the SQL statement
    sql_statement = (
        "INSERT INTO orders (order_id, order_status, created_by) "
        f"VALUES ('{new_order_id}', '{ORDER_STATUS['INITIATED']}', '{created_by}')"
    )

    print(sql_statement)

    return rds_data.execute_statement(
        secretArn=secret_arn,
        resourceArn=resource_arn,
        sql=sql_statement,
        database=database,
    )


def lambda_handler(event, context):
    print("Input to lambda", event, type(event["body"]))
    body = event["body"]
    created_by = body["created_by"]
    try:
        if not created_by:
            return bad_request_response("Missing mandatory fields: created_by")
        response = insert_order_values(created_by)

        if response["numberOfRecordsUpdated"]:
            return ok_response("Order initiated successfully!")
    except Exception as e:
        return internal_server_error_response(str(e))
