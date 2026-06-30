import json
import boto3
import urllib.request
import urllib.parse
from decimal import Decimal

def lambda_handler(event, context):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('Games')
    ses = boto3.client('ses', region_name='us-east-2')
    
    response = table.scan()
    games = response['Items']
    
    for game in games:
        title = game['title']
        target_price = float(game['targetPrice'])
        email = game['email']
        
        encoded_title = urllib.parse.quote(title)
        url = f'https://www.cheapshark.com/api/1.0/games?title={encoded_title}&limit=1'
        
        req = urllib.request.Request(url, headers={'User-Agent': 'GameDealTracker/1.0 (jaygera13@gmail.com)'})
        
        try:
            with urllib.request.urlopen(req) as resp:
                results = json.loads(resp.read())
                
            if results:
                current_price = float(results[0]['cheapest'])
                
                if current_price <= target_price:
                    send_alert_email(ses, email, title, current_price, target_price)
                    
        except Exception as e:
            print(f"Error checking {title}: {str(e)}")
    
    return {
        'statusCode': 200,
        'body': json.dumps({'message': 'Deal check complete'})
    }

def send_alert_email(ses, email, title, current_price, target_price):
    subject = f"Price Drop Alert: {title}"
    body = f"{title} is now ${current_price}, which is below your target of ${target_price}! Go grab it!"
    
    ses.send_email(
        Source=email,
        Destination={'ToAddresses': [email]},
        Message={
            'Subject': {'Data': subject},
            'Body': {'Text': {'Data': body}}
        }
    )