import json
import boto3
from decimal import Decimal
from boto3.dynamodb.conditions import Key

def decimal_default(obj):
    if isinstance(obj, Decimal):
        return float(obj)
    raise TypeError

def lambda_handler(event, context):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('PriceHistory')
    
    title = event['queryStringParameters']['title']
    
    response = table.query(
        KeyConditionExpression=Key('gameTitle').eq(title)
    )
    
    history = response['Items']
    history.sort(key=lambda x: x['timestamp'])
    
    return {
        'statusCode': 200,
        'headers': {
            'Access-Control-Allow-Origin': '*'
        },
        'body': json.dumps(history, default=decimal_default)
    }