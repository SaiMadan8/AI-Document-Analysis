# Setup Guide

Complete deployment steps for DocuMind Intelligence.

## Step 1: IAM Role Setup
Create Lambda execution role with permissions:
- bedrock:InvokeModel
- dynamodb:PutItem
- dynamodb:GetItem
- logs:CreateLogGroup
- logs:CreateLogStream
- logs:PutLogEvents

## Step 2: DynamoDB Table
Create table with these settings:
- Table name: document-analysis-results
- Partition key: document_id (String)
- Billing mode: On-demand

## Step 3: Lambda Function
- Upload lambda_function.py
- Runtime: Python 3.13
- Memory: 1024 MB
- Timeout: 30 seconds
- Attach IAM role from Step 1

## Step 4: API Gateway
- Create REST API
- Add resource: /upload
- Add method: POST
- Enable CORS
- Integrate with Lambda function
- Deploy to stage (prod)

## Step 5: S3 Website
- Create S3 bucket
- Enable static website hosting
- Upload index.html
- Make bucket publicly readable
- Update API_ENDPOINT in index.html

## Step 6: Testing
- Upload test document through web interface
- Check CloudWatch logs
- Verify DynamoDB entries
- Test error handling
