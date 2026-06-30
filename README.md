# 🎮 Game Deal Tracker

A fully serverless, event-driven web application that tracks PC game prices, sends personalized email alerts, visualizes price history, and uses AI to recommend games and deliver a daily personalized deal — all running automatically on AWS with zero servers to manage.

## Live Demo
http://jay-game-tracker.s3-website.us-east-2.amazonaws.com

## Features
- **Deal Tracker** — Track unlimited games with custom price thresholds and get emailed when the price drops
- **Price History** — Interactive Chart.js visualization showing how a game's price has changed over time
- **AI Recommendations** — Enter games you love and get 5 personalized recommendations powered by Claude AI
- **Deal of the Day** — Subscribe to a daily 9am email with the best game deal, personalized to your taste based on games you track

## How It Works

### Deal Tracker
1. User adds a game, target price, and email through the web app
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
5. If not, the highest-rated deal is sent instead
6. A styled HTML email is delivered with an unsubscribe link
7. Clicking unsubscribe instantly removes the user — no login required

## Architecture
- **Frontend** — HTML/CSS/JavaScript hosted on Amazon S3
- **API** — Amazon API Gateway with REST endpoints
- **Backend** — AWS Lambda functions written in Python
- **Database** — Amazon DynamoDB (NoSQL) — Games, PriceHistory, Subscribers tables
- **Scheduler** — Amazon EventBridge (price checks daily, Deal of the Day at 9am EST)
- **Email** — Amazon SES with styled HTML emails
- **AI** — Anthropic Claude via Lambda (recommendations + personalized deals)
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
| POST | /subscribe | Subscribe to Deal of the Day |
| GET | /unsubscribe | Unsubscribe from Deal of the Day |

## Lambda Functions
| Function | Trigger | Description |
|----------|---------|-------------|
| addGame | API Gateway POST /games | Saves a new game to DynamoDB |
| getGames | API Gateway GET /games | Returns all tracked games |
| checkDeals | EventBridge (daily) | Checks prices, saves history, sends alerts |
| getPriceHistory | API Gateway GET /history | Returns price history for a game |
| recommendGames | API Gateway POST /recommend | Returns AI game recommendations |
| subscribe | API Gateway POST /subscribe | Adds email to Subscribers table |
| unsubscribe | API Gateway GET /unsubscribe | Removes email from Subscribers table |
| dealOfTheDay | EventBridge (9am EST daily) | Sends personalized daily deal email |

## DynamoDB Tables
| Table | Partition Key | Sort Key | Description |
|-------|--------------|----------|-------------|
| Games | gameID (String) | — | Tracked games with target prices |
| PriceHistory | gameTitle (String) | timestamp (String) | Daily price snapshots |
| Subscribers | email (String) | — | Deal of the Day subscribers |

## Deployment
All Lambda functions are deployed via AWS CLI using zip packaging.
API keys are stored securely in AWS Systems Manager Parameter Store.
Infrastructure is hosted entirely on AWS.

## Notes
- SES is configured in sandbox mode for development — in production it would be moved to production access to send to any address
- Price history grows richer over time as the daily EventBridge schedule runs
- Deal of the Day personalization requires the subscriber's email to match their tracked games email