import json
import boto3

def lambda_handler(event, context):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('Games')
    
    game_id = event['pathParameters']['gameID']
    
    table.delete_item(
        Key={
            'gameID': game_id
        }
    )
    
    return {
        'statusCode': 200,
        'headers': {
            'Access-Control-Allow-Origin': '*'
        },
        'body': json.dumps({'message': 'Game deleted'})
    }