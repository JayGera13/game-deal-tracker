import json
import boto3
import uuid

def lambda_handler(event, context):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('Games')
    
    claims = event['requestContext']['authorizer']['jwt']['claims']
    user_email = claims.get('email') or claims.get('username') or claims.get('cognito:username')
    
    body = json.loads(event['body'])
    
    task = {
        'gameID': str(uuid.uuid4()),
        'title': body['title'],
        'targetPrice': body['targetPrice'],
        'email': user_email,
        'userID': user_email
    }
    
    table.put_item(Item=task)
    
    return {
        'statusCode': 201,
        'headers': {
            'Access-Control-Allow-Origin': '*'
        },
        'body': json.dumps(task)
    }