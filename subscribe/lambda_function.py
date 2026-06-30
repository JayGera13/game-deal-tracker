import json
import boto3

def lambda_handler(event, context):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('Subscribers')
    
    body = json.loads(event['body'])
    email = body['email']
    
    table.put_item(Item={
        'email': email
    })
    
    return {
        'statusCode': 200,
        'headers': {
            'Access-Control-Allow-Origin': '*'
        },
        'body': json.dumps({'message': 'Subscribed successfully'})
    }