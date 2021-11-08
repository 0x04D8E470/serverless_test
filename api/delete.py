import os

import boto3
dynamodb = boto3.resource('dynamodb')


def delete_task(event, context):
    table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])

    table.delete_item(
        Key={
            'id': event['pathParameters']['id']
        }
    )

    response = {
        "statusCode": 200
    }

    return response
