# Lambda Function Documentation

## Overview
AWS Lambda function that powers DocuMind Intelligence document analysis.

## Function Configuration
- Runtime: Python 3.13
- Memory: 1024 MB
- Timeout: 30 seconds
- Handler: lambda_function.lambda_handler

## Dependencies
boto3>=1.34.0

## Environment Variables
AWS_REGION = us-east-1
DYNAMODB_TABLE = document-analysis-results

## IAM Permissions Required
The Lambda execution role needs:
- bedrock:InvokeModel
- dynamodb:PutItem
- dynamodb:GetItem
- s3:GetObject
- logs:CreateLogGroup
- logs:CreateLogStream
- logs:PutLogEvents

## Deployment
Manual deployment steps:
1. cd lambda
2. zip -r function.zip lambda_function.py
3. aws lambda update-function-code --function-name documind-analysis --zip-file fileb://function.zip

## API Request Format
{
  "file_content": "Your document text here",
  "file_key": "document.txt",
  "bucket_name": "optional-bucket-name"
}

## API Response Format
{
  "message": "Analysis complete",
  "document_id": "unique-uuid",
  "analysis": "AI-generated insights",
  "timestamp": "2025-11-09T18:25:00"
}

## Performance Metrics
- Average execution: 8-10 seconds
- Cold start: 2-3 seconds
- Memory usage: 512 MB average
