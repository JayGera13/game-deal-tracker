# 🎮 Game Deal Tracker

A fully serverless, event-driven application that tracks PC game prices, 
automatically sends email alerts when a game drops below your target price, 
visualizes price history, and uses AI to recommend games based on your taste.

## Live Demo
http://jay-game-tracker.s3-website.us-east-2.amazonaws.com

## Features
- Track unlimited games with custom price thresholds
- Fully automated daily price monitoring via EventBridge — no manual triggers needed
- Real-time price data from CheapShark API across Steam and other stores
- Email alerts via Amazon SES when deals are found
- Price history tracking stored in DynamoDB with interactive Chart.js visualization
- AI-powered game recommendations using Claude (Anthropic) via Lambda
- Serverless architecture — zero servers to manage

## How It Works

### Deal Tracker
1. User adds a game, target price, and email through the web app
2. AWS EventBridge triggers a price check every 24 hours automatically
3. Lambda queries the CheapShark API for current game prices
4. Current price is saved to PriceHistory table in DynamoDB
5. If a deal is found, Amazon SES sends an email alert instantly

### Price History
1. Every daily price check saves a timestamped price entry to DynamoDB
2. User selects a game from the Price History tab
3. Lambda queries DynamoDB for all historical prices
4. Frontend renders an interactive line chart using Chart.js

### AI Recommendations
1. User enters 2-3 games they enjoy
2. Lambda sends a request to Claude AI via the Anthropic API
3. Claude analyzes the user's taste and returns 5 personalized recommendations
4. Results are displayed with genre tags and explanations

## Architecture
- **Frontend** — HTML/CSS/JavaScript hosted on Amazon S3
- **API** — Amazon API Gateway with REST endpoints
- **Backend** — AWS Lambda functions written in Python
- **Database** — Amazon DynamoDB (NoSQL) — Games + PriceHistory tables
- **Scheduler** — Amazon EventBridge (runs price checks daily)
- **Email** — Amazon SES (sends deal alert emails)
- **AI** — Anthropic Claude via Lambda (game recommendations)
- **Secrets** — AWS Systems Manager Parameter Store (secure API key storage)
- **Price Data** — CheapShark API (free public game pricing API)
- **Charts** — Chart.js (price history visualization)

## AWS Services Used
- AWS Lambda
- Amazon API Gateway
- Amazon DynamoDB
- Amazon S3
- Amazon EventBridge
- Amazon SES
- AWS IAM
- AWS Systems Manager Parameter Store

## API Endpoints
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /games | Retrieve all tracked games |
| POST | /games | Add a new game to track |
| GET | /history | Get price history for a game |
| POST | /recommend | Get AI game recommendations |

## Lambda Functions
| Function | Trigger | Description |
|----------|---------|-------------|
| addGame | API Gateway POST /games | Saves a new game to DynamoDB |
| getGames | API Gateway GET /games | Returns all tracked games |
| checkDeals | EventBridge (daily) | Checks prices, saves history, sends alerts |
| getPriceHistory | API Gateway GET /history | Returns price history for a game |
| recommendGames | API Gateway POST /recommend | Returns AI game recommendations |

## Deployment
All Lambda functions are deployed via AWS CLI using zip packaging.
API keys are stored securely in AWS Systems Manager Parameter Store.
Infrastructure is hosted entirely on AWS.

## Notes
- SES is configured in sandbox mode for development
- In production, SES would be moved out of sandbox to send to any address
- Price history grows richer over time as the daily EventBridge schedule runs