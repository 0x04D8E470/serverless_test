import json
import time
import logging
import os

from api import decimalencoder
import boto3

dynamodb = boto3.resource('dynamodb')


def update_task(event, context):
    timestamp = int(time.time() * 1000)
    data = json.loads(event['body'])
    if 'text' not in data or 'checked' not in data:
        logging.error("Validation Failed")
        raise Exception("Couldn't update the todo item.")
        return
    table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])

    result = table.update_item(
        Key={
            'id': event['pathParameters']['id']
        },
        ExpressionAttributeNames={
            '#todo_text': 'text',
        },
        ExpressionAttributeValues={
            ':text': data['text'],
            ':checked': data['checked'],
            ':updatedAt': timestamp,
        },
        UpdateExpression='SET #todo_text = :text, '
                         'checked = :checked, '
                         'updatedAt = :updatedAt',
        ReturnValues='ALL_NEW',
    )

    response = {
        "statusCode": 200,
        "body": json.dumps(result['Attributes'],
                           cls=decimalencoder.DecimalEncoder)
    }

    return response
