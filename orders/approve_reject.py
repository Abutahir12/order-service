import boto3
import os
from datetime import datetime

from dotenv import load_dotenv
from utils.http_methods import (
    ok_response,
    bad_request_response,
    internal_server_error_response,
)
from utils.constants import ORDER_STATUS, ORDER_STATUS_REVERSE_MAP

load_dotenv()

DB_NAME = os.getenv("DB_NAME")
SECRET_ARN = os.getenv("SECRET_ARN")
RESOURCE_ARN = os.getenv("RESOURCE_ARN")

rds_data = boto3.client("rds-data")

# Replace these with your own RDS Data API configuration
database = DB_NAME
secret_arn = SECRET_ARN
resource_arn = RESOURCE_ARN


def approve_reject_order(created_by, order_id, admin_id, approval_status):

    # Restricting the order to be updated only if the the current approval status is the next update status in sequence
    sql_statement = f"""UPDATE orders set order_status = CASE 
        WHEN {approval_status} > order_status 
        THEN {approval_status} END,
        updated_at='{datetime.utcnow()}'
        where created_by = '{created_by}' and order_id = '{order_id}'"""

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
    admin_id = body["admin_id"]
    approval_status = body["approval_status"]
    try:
        if not created_by or not order_id or not admin_id:
            return bad_request_response(
                "Missing mandatory fields: created_by/order_id/admin_id"
            )

        #  check if the admin belongs to any approval group
        check_admin_query = f"SELECT * from users where id = '{admin_id}' and approval_group_id is not null"
        result = rds_data.execute_statement(
            secretArn=secret_arn,
            resourceArn=resource_arn,
            sql=check_admin_query,
            database=database,
        )

        if not len(result["records"]):
            return bad_request_response(
                "User is not authorized to perform this operation"
            )

        response = approve_reject_order(created_by, order_id, admin_id, approval_status)
        if response["numberOfRecordsUpdated"]:
            return ok_response("Order updated successfully")
    except Exception as e:
        return internal_server_error_response(str(e))
