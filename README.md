# 🎮 Game Deal Tracker

A fully serverless, event-driven application that tracks PC game prices and automatically 
sends email alerts when a game drops below your target price.

## Live Demo
http://jay-game-tracker.s3-website.us-east-2.amazonaws.com

## How It Works
1. User adds a game, target price, and email through the web app
2. AWS EventBridge triggers a price check every 24 hours automatically
3. A Lambda function queries the CheapShark API for current prices
4. If a deal is found, Amazon SES sends an email alert instantly

## Architecture
- **Frontend** — HTML/CSS/JavaScript hosted on Amazon S3
- **API** — Amazon API Gateway with REST endpoints
- **Backend** — AWS Lambda functions written in Python
- **Database** — Amazon DynamoDB (NoSQL)
- **Scheduler** — Amazon EventBridge (runs price checks daily)
- **Email** — Amazon SES (sends deal alert emails)
- **Price Data** — CheapShark API (free public game pricing API)

## AWS Services Used
- AWS Lambda
- Amazon API Gateway
- Amazon DynamoDB
- Amazon S3
- Amazon EventBridge
- Amazon SES
- AWS IAM

## Features
- Track unlimited games with custom price thresholds
- Fully automated daily price monitoring — no manual triggers needed
- Real-time price data from CheapShark across Steam and other stores
- Email alerts when deals are found
- Serverless architecture — zero servers to manage

## API Endpoints
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /games | Retrieve all tracked games |
| POST | /games | Add a new game to track |

## Deployment
All Lambda functions are deployed via AWS CLI using zip packaging.
Infrastructure is hosted entirely on AWS free tier services.

## Notes
- SES is configured in sandbox mode — emails are sent from and to verified addresses only
- In a production environment, SES would be moved out of sandbox mode to send to any address