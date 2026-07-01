import json
import boto3
from decimal import Decimal
from boto3.dynamodb.conditions import Attr

def decimal_default(obj):
    if isinstance(obj, Decimal):
        return float(obj)
    raise TypeError

def lambda_handler(event, context):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('Games')
    
    claims = event['requestContext']['authorizer']['jwt']['claims']
    user_email = claims.get('email') or claims.get('username') or claims.get('cognito:username')
    
    response = table.scan(
        FilterExpression=Attr('userID').eq(user_email)
    )
    games = response['Items']
    
    return {
        'statusCode': 200,
        'headers': {
            'Access-Control-Allow-Origin': '*'
        },
        'body': json.dumps(games, default=decimal_default)
    }