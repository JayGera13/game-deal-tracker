import json
import boto3
import urllib.request
import urllib.parse
from decimal import Decimal

def get_api_key():
    ssm = boto3.client('ssm', region_name='us-east-2')
    response = ssm.get_parameter(
        Name='/game-tracker/anthropic-api-key',
        WithDecryption=True
    )
    return response['Parameter']['Value']

def get_best_deal():
    url = 'https://www.cheapshark.com/api/1.0/deals?sortBy=Deal+Rating&pageSize=20&onSale=1'
    req = urllib.request.Request(
        url,
        headers={'User-Agent': 'GameDealTracker/1.0 (jaygera13@gmail.com)'}
    )
    with urllib.request.urlopen(req) as resp:
        deals = json.loads(resp.read())
    return deals

def get_user_games(email):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('Games')
    response = table.scan()
    user_games = [g['title'] for g in response['Items'] if g['email'] == email]
    return user_games

def get_personalized_deal(deals, user_games, api_key):
    deals_text = '\n'.join([
        f"- {d['title']}: ${d['salePrice']} (normally ${d['normalPrice']}, {int(float(d['savings']))}% off)"
        for d in deals[:20]
    ])
    
    games_text = ', '.join(user_games)
    
    prompt = f"""A user enjoys these games: {games_text}

Here are today's top game deals:
{deals_text}

Pick the single best deal for this user based on their taste. Consider genre, style, and game type.
Respond with ONLY a JSON object like this:
{{
    "title": "Game Title",
    "salePrice": "9.99",
    "normalPrice": "29.99",
    "savings": "66",
    "reason": "One sentence explaining why this deal matches their taste"
}}"""

    request_body = json.dumps({
        "model": "claude-haiku-4-5",
        "max_tokens": 512,
        "messages": [{"role": "user", "content": prompt}]
    }).encode('utf-8')

    req = urllib.request.Request(
        'https://api.anthropic.com/v1/messages',
        data=request_body,
        headers={
            'Content-Type': 'application/json',
            'x-api-key': api_key,
            'anthropic-version': '2023-06-01'
        },
        method='POST'
    )

    with urllib.request.urlopen(req) as resp:
        result = json.loads(resp.read())

    text = result['content'][0]['text']
    start = text.find('{')
    end = text.rfind('}') + 1
    return json.loads(text[start:end])

def send_deal_email(ses, email, deal, personalized=False):
    title = deal['title']
    sale_price = deal['salePrice']
    normal_price = deal['normalPrice']
    savings = int(float(deal['savings']))
    reason = deal.get('reason', '')
    
    unsubscribe_url = f"https://wfyzse8zm0.execute-api.us-east-2.amazonaws.com/unsubscribe?email={urllib.parse.quote(email)}"
    
    personalized_text = f"<p style='color:#4ecca3'>🎯 Picked for you: {reason}</p>" if personalized else "<p style='color:#aaa'>Today's best overall deal on Steam</p>"
    
    html_body = f"""
    <html>
    <body style="font-family: Arial; background: #1a1a2e; color: #eee; padding: 40px; max-width: 600px; margin: 0 auto;">
        <h1 style="color: #e94560">🎮 Deal of the Day</h1>
        <div style="background: #16213e; border-radius: 12px; padding: 24px; border-left: 4px solid #e94560;">
            <h2 style="color: #fff; margin-bottom: 8px">{title}</h2>
            {personalized_text}
            <div style="margin-top: 16px">
                <span style="font-size: 2rem; font-weight: bold; color: #e94560">${sale_price}</span>
                <span style="color: #aaa; text-decoration: line-through; margin-left: 12px">${normal_price}</span>
                <span style="background: #4ecca3; color: #1a1a2e; padding: 4px 10px; border-radius: 20px; margin-left: 12px; font-weight: bold">{savings}% OFF</span>
            </div>
        </div>
        <p style="color: #aaa; font-size: 12px; margin-top: 32px">
            <a href="{unsubscribe_url}" style="color: #aaa">Unsubscribe from Deal of the Day</a>
        </p>
    </body>
    </html>
    """
    
    ses.send_email(
        Source='jaygera13@gmail.com',
        Destination={'ToAddresses': [email]},
        Message={
            'Subject': {'Data': f"🎮 Deal of the Day: {title} — {savings}% off!"},
            'Body': {
                'Html': {'Data': html_body}
            }
        }
    )

def lambda_handler(event, context):
    dynamodb = boto3.resource('dynamodb')
    subscribers_table = dynamodb.Table('Subscribers')
    ses = boto3.client('ses', region_name='us-east-2')
    
    response = subscribers_table.scan()
    subscribers = response['Items']
    
    if not subscribers:
        return {
            'statusCode': 200,
            'body': json.dumps({'message': 'No subscribers'})
        }
    
    deals = get_best_deal()
    api_key = get_api_key()
    
    for subscriber in subscribers:
        email = subscriber['email']
        
        try:
            user_games = get_user_games(email)
            
            if user_games:
                deal = get_personalized_deal(deals, user_games, api_key)
                send_deal_email(ses, email, deal, personalized=True)
            else:
                best_deal = deals[0]
                deal = {
                    'title': best_deal['title'],
                    'salePrice': best_deal['salePrice'],
                    'normalPrice': best_deal['normalPrice'],
                    'savings': best_deal['savings']
                }
                send_deal_email(ses, email, deal, personalized=False)
                
        except Exception as e:
            print(f"Error sending to {email}: {str(e)}")
    
    return {
        'statusCode': 200,
        'body': json.dumps({'message': f'Deal of the Day sent to {len(subscribers)} subscribers'})
    }