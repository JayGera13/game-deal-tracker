# 🎮 Game Deal Tracker

A fully serverless, event-driven web application that tracks PC game prices, sends personalized email alerts, visualizes price history, and uses AI to recommend games and deliver a daily personalized deal — all running automatically on AWS with zero servers to manage.

## Live Demo
https://d2ehydjq9wvkn8.cloudfront.net

## Features
- **User Authentication** — Secure sign up and login via Amazon Cognito. Each user only sees and manages their own tracked games
- **Deal Tracker** — Track unlimited games with custom price thresholds and get emailed when the price drops
- **Price History** — Interactive Chart.js visualization showing how a game's price has changed over time
- **AI Recommendations** — Enter games you love and get 5 personalized recommendations powered by Claude AI
- **Deal of the Day** — Subscribe to a daily 9am email with the best game deal, personalized to your taste
- **HTTPS via CloudFront** — Frontend served globally via AWS CloudFront CDN with full HTTPS support

## How It Works

### Authentication
1. User signs up or logs in via Amazon Cognito hosted UI
2. Cognito issues a JWT token on successful login
3. All game tracking requests include the JWT token in the Authorization header
4. API Gateway validates the token via a JWT authorizer before allowing access
5. Lambda functions read the user's identity from the token to isolate their data

### Deal Tracker
1. User adds a game and target price through the authenticated web app
2. AWS EventBridge triggers a price check every 24 hours automatically
3. Lambda queries the CheapShark API for current game prices
4. Current price is saved to PriceHistory table in DynamoDB
5. If a deal is found, Amazon SES sends a styled HTML email alert instantly

### Price History
1. Every daily price check saves a timestamped price entry to DynamoDB
2. User selects a game from the Price History tab
3. Lambda queries DynamoDB for all historical prices
4. Frontend renders an interactive line chart using Chart.js

### AI Recommendations
1. User enters 2-3 games they enjoy
2. Lambda sends a request to Claude AI via the Anthropic API
3. Claude analyzes the user's taste and returns 5 personalized recommendations
4. Results display with genre tags and explanations

### Deal of the Day
1. User subscribes with their email on the Deal of the Day tab
2. EventBridge triggers the dealOfTheDay Lambda every morning at 9am EST
3. Lambda fetches the top 20 deals from CheapShark
4. If the subscriber has tracked games, Claude AI picks the best deal matching their taste
5. A styled HTML email is delivered with a one-click unsubscribe link

## Architecture
- **Frontend** — HTML/CSS/JavaScript hosted on Amazon S3, served via CloudFront CDN with HTTPS
- **Authentication** — Amazon Cognito user pool with hosted UI and JWT token validation
- **API** — Amazon API Gateway with REST endpoints and JWT authorizer
- **Backend** — AWS Lambda functions written in Python
- **Database** — Amazon DynamoDB (NoSQL) — Games, PriceHistory, Subscribers tables
- **Scheduler** — Amazon EventBridge (price checks daily, Deal of the Day at 9am EST)
- **Email** — Amazon SES with styled HTML emails
- **AI** — Anthropic Claude via Lambda (recommendations + personalized deals)
- **Secrets** — AWS Systems Manager Parameter Store (secure API key storage)
- **Price Data** — CheapShark API (free public game pricing API)
- **Charts** — Chart.js (price history visualization)
- **CDN** — Amazon CloudFront (global content delivery with HTTPS)

## AWS Services Used
- AWS Lambda
- Amazon API Gateway
- Amazon DynamoDB
- Amazon S3
- Amazon CloudFront
- Amazon Cognito
- Amazon EventBridge
- Amazon SES
- AWS IAM
- AWS Systems Manager Parameter Store

## API Endpoints
| Method | Endpoint | Auth Required | Description |
|--------|----------|--------------|-------------|
| GET | /games | ✅ Yes | Retrieve user's tracked games |
| POST | /games | ✅ Yes | Add a new game to track |
| DELETE | /games/{gameID} | ✅ Yes | Delete a tracked game |
| GET | /history | No | Get price history for a game |
| POST | /recommend | No | Get AI game recommendations |
| POST | /subscribe | No | Subscribe to Deal of the Day |
| GET | /unsubscribe | No | Unsubscribe from Deal of the Day |

## Lambda Functions
| Function | Trigger | Description |
|----------|---------|-------------|
| addGame | API Gateway POST /games | Saves a new game tied to authenticated user |
| getGames | API Gateway GET /games | Returns only the authenticated user's games |
| deleteGame | API Gateway DELETE /games/{gameID} | Deletes game only if owned by authenticated user |
| checkDeals | EventBridge (daily) | Checks prices, saves history, sends alerts |
| getPriceHistory | API Gateway GET /history | Returns price history for a game |
| recommendGames | API Gateway POST /recommend | Returns AI game recommendations |
| subscribe | API Gateway POST /subscribe | Adds email to Subscribers table |
| unsubscribe | API Gateway GET /unsubscribe | Removes email from Subscribers table |
| dealOfTheDay | EventBridge (9am EST daily) | Sends personalized daily deal email |

## DynamoDB Tables
| Table | Partition Key | Sort Key | Description |
|-------|--------------|----------|-------------|
| Games | gameID (String) | — | Tracked games with target prices and userID |
| PriceHistory | gameTitle (String) | timestamp (String) | Daily price snapshots |
| Subscribers | email (String) | — | Deal of the Day subscribers |

## Security
- All game management routes protected by Cognito JWT authorizer
- Users can only read and delete their own games — enforced at the Lambda level
- API keys stored securely in AWS Systems Manager Parameter Store
- Frontend served over HTTPS via CloudFront

## Deployment
All Lambda functions are deployed via AWS CLI using zip packaging.
Frontend is hosted on S3 and distributed globally via CloudFront.

## Infrastructure as Code
The complete infrastructure is defined in `template.yaml` using AWS CloudFormation.
To deploy a fresh copy of this application to a new AWS account:

```bash
aws cloudformation deploy \
  --template-file template.yaml \
  --stack-name game-tracker-stack \
  --capabilities CAPABILITY_NAMED_IAM \
  --parameter-overrides AnthropicApiKey=YOUR_API_KEY
```

This will provision all DynamoDB tables, Lambda functions, API Gateway routes, 
EventBridge schedules, IAM roles, and S3 bucket automatically.

## Notes
- SES is configured in sandbox mode — in production it would be moved to production access
- Price history grows richer over time as the daily EventBridge schedule runs
- Deal of the Day personalization matches subscriber email to their tracked games email