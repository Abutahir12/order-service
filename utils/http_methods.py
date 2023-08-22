from http import HTTPStatus

import json

headers = {
    "Content-Type": "application/json"
}

def ok_response(body="success"):
    return {
        "statusCode": HTTPStatus.OK.value,
        "body": json.dumps(body),
        "headers": headers
    }

def forbidden_response(body="Forbidden"):
    return {
        "statusCode": HTTPStatus.FORBIDDEN.value,
        "body": json.dumps(body),
        "headers": headers
    }

def bad_request_response(body="Bad Request"):
    return {
        "statusCode": HTTPStatus.BAD_REQUEST.value,
        "body": json.dumps(body),
        "headers": headers
    }

def internal_server_error_response(body="Internal Server Error"):
    return {
        "statusCode": HTTPStatus.INTERNAL_SERVER_ERROR.value,
        "body": json.dumps(body),
        "headers": headers
    }

def create_response(body="Resource created successfully"):
    return {
        "statusCode": HTTPStatus.CREATED.value,
        "body": json.dumps(body),
        "headers": headers
    }

