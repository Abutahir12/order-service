import boto3
import os
from datetime import datetime

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


def mark_order_under_review(created_by, order_id):
    # Replace these with your own RDS Data API configuration
    database = DB_NAME
    secret_arn = SECRET_ARN
    resource_arn = RESOURCE_ARN

    # Construct the SQL statement
    sql_statement = (
        f"UPDATE orders set order_status = {ORDER_STATUS['UNDER_REVIEW']}, updated_at='{datetime.utcnow()}' "
        f"where created_by = '{created_by}' and order_id = '{order_id}'"
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
    order_id = body["order_id"]
    try:
        if not created_by:
            return bad_request_response("Missing mandatory fields: created_by/order_id")
        response = mark_order_under_review(created_by, order_id)

        if response["numberOfRecordsUpdated"]:
            return ok_response("Order Marked Under Review")
    except Exception as e:
        return internal_server_error_response(str(e))
