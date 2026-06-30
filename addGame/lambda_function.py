import json
import boto3
import uuid

def lambda_handler(event, context):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('Games')
    
    body = json.loads(event['body'])
    
    game = {
        'gameID': str(uuid.uuid4()),
        'title': body['title'],
        'targetPrice': body['targetPrice'],
        'email': body['email']
    }
    
    table.put_item(Item=game)
    
    return {
        'statusCode': 201,
        'headers': {
            'Access-Control-Allow-Origin': '*'
        },
        'body': json.dumps(game)
    }