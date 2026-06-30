import json
import boto3

def lambda_handler(event, context):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('Subscribers')
    
    email = event['queryStringParameters']['email']
    
    table.delete_item(Key={'email': email})
    
    return {
        'statusCode': 200,
        'headers': {
            'Access-Control-Allow-Origin': '*',
            'Content-Type': 'text/html'
        },
        'body': '''
        <html>
        <body style="font-family: Arial; text-align: center; padding: 60px; background: #1a1a2e; color: #eee;">
            <h1 style="color: #e94560">🎮 Game Deal Tracker</h1>
            <h2>You've been unsubscribed</h2>
            <p style="color: #aaa">You won't receive any more Deal of the Day emails.</p>
            <a href="http://jay-game-tracker.s3-website.us-east-2.amazonaws.com" 
               style="color: #e94560">Go back to the app</a>
        </body>
        </html>
        '''
    }