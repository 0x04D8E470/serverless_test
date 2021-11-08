import os
import json

from api import decimalencoder
import boto3
dynamodb = boto3.resource('dynamodb')


def get_task(event, context):
    table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])

    result = table.get_item(
        Key={
            'id': event['pathParameters']['id']
        }
    )

    response = {
        "statusCode": 200,
        "body": json.dumps(result['Item'],
                           cls=decimalencoder.DecimalEncoder)
    }

    return response
