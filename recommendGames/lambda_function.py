import json
import boto3
import urllib.request

def get_api_key():
    ssm = boto3.client('ssm', region_name='us-east-2')
    response = ssm.get_parameter(
        Name='/game-tracker/anthropic-api-key',
        WithDecryption=True
    )
    return response['Parameter']['Value']

def lambda_handler(event, context):
    body = json.loads(event['body'])
    games = body['games']
    
    api_key = get_api_key()
    
    prompt = f"""You are a video game recommendation expert. 
    Based on these games the user enjoys: {', '.join(games)}
    
    Recommend 5 similar games they would love. For each game provide:
    - Game title
    - One sentence explaining why they'd like it based on their taste
    - Genre
    
    Format your response as a JSON array like this:
    [
        {{
            "title": "Game Name",
            "reason": "You'd love this because...",
            "genre": "Action RPG"
        }}
    ]
    
    Return ONLY the JSON array, no other text."""
    
    request_body = json.dumps({
        "model": "claude-haiku-4-5",
        "max_tokens": 1024,
        "messages": [
            {"role": "user", "content": prompt}
        ]
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
    start = text.find('[')
    end = text.rfind(']') + 1
    recommendations = json.loads(text[start:end])
    
    return {
        'statusCode': 200,
        'headers': {
            'Access-Control-Allow-Origin': '*'
        },
        'body': json.dumps(recommendations)
    }