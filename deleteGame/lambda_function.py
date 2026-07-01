import json
import boto3
from boto3.dynamodb.conditions import Attr

def lambda_handler(event, context):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('Games')
    
    claims = event['requestContext']['authorizer']['jwt']['claims']
    user_email = claims.get('email') or claims.get('username') or claims.get('cognito:username')
    
    game_id = event['pathParameters']['gameID']
    
    response = table.get_item(Key={'gameID': game_id})
    game = response.get('Item')
    
    if not game or game.get('userID') != user_email:
        return {
            'statusCode': 403,
            'headers': {
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({'message': 'Not authorized to delete this game'})
        }
    
    table.delete_item(Key={'gameID': game_id})
    
    return {
        'statusCode': 200,
        'headers': {
            'Access-Control-Allow-Origin': '*'
        },
        'body': json.dumps({'message': 'Game deleted'})
    }