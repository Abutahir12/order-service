import boto3
import json
import os

from dotenv import load_dotenv
from utils.http_methods import (
    ok_response,
    bad_request_response,
    internal_server_error_response,
)

load_dotenv()

DB_NAME = os.getenv("DB_NAME")
SECRET_ARN = os.getenv("SECRET_ARN")
RESOURCE_ARN = os.getenv("RESOURCE_ARN")

rds_data = boto3.client("rds-data")


def insert_user_values(
    username, first_name, last_name=None, approval_group_id=None
):
    # Replace these with your own RDS Data API configuration
    database = DB_NAME
    secret_arn = SECRET_ARN
    resource_arn = RESOURCE_ARN

    # Construct the SQL statement
    sql_statement = (
        "INSERT INTO users (username, first_name, last_name, approval_group_id) "
        f"VALUES ('{username}', '{first_name}', '{last_name}', {approval_group_id})"
    )

    return rds_data.execute_statement(
        secretArn=secret_arn,
        resourceArn=resource_arn,
        sql=sql_statement,
        database=database,
    )


def lambda_handler(event, context):
    print("Input to lambda", event, type(event["body"]))
    body = event["body"]
    username = body["username"]
    first_name = body["first_name"]
    last_name = body["last_name"]
    approval_group_id = body["approval_group_id"]

    try:
        if not len(username) or not len(first_name):
            return bad_request_response("Missing mandatory fields: username/first_name")
        response = insert_user_values(
            username, first_name, last_name, approval_group_id
        )

        if response["numberOfRecordsUpdated"]:
            return ok_response("User created successfully!")
    except Exception as e:
        if "duplicate key value" in str(e):
            return bad_request_response("Username already exists")
        return internal_server_error_response(str(e))
