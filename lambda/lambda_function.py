import json
import boto3
from datetime import datetime
import uuid

# Initialize AWS clients
bedrock_client = boto3.client('bedrock-runtime', region_name='us-east-1')
dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
table = dynamodb.Table('document-analysis-results')

def lambda_handler(event, context):
    """Main Lambda handler for document analysis"""
    
    headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Headers': 'Content-Type',
        'Access-Control-Allow-Methods': 'POST, OPTIONS'
    }
    
    try:
        if event.get('httpMethod') == 'OPTIONS':
            return {
                'statusCode': 200,
                'headers': headers,
                'body': json.dumps({'message': 'CORS preflight successful'})
            }
        
        body = json.loads(event.get('body', '{}'))
        file_content = body.get('file_content')
        
        if not file_content:
            return {
                'statusCode': 400,
                'headers': headers,
                'body': json.dumps({'error': 'Missing file_content'})
            }
        
        prompt = f"""Analyze the following document and provide:
1. A concise summary
2. Key themes and topics
3. Important insights
4. Actionable recommendations

Document:
{file_content}"""

        request_body = {
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": 4096,
            "messages": [{"role": "user", "content": prompt}]
        }
        
        response = bedrock_client.invoke_model(
            modelId='anthropic.claude-3-haiku-20240307-v1:0',
            body=json.dumps(request_body)
        )
        
        response_body = json.loads(response['body'].read())
        ai_analysis = response_body['content'][0]['text']
        
        document_id = str(uuid.uuid4())
        timestamp = datetime.now().isoformat()
        
        table.put_item(
            Item={
                'document_id': document_id,
                'timestamp': timestamp,
                'file_key': body.get('file_key', 'inline_upload'),
                'file_content': file_content[:1000],
                'analysis': ai_analysis,
                'bucket_name': body.get('bucket_name', 'N/A')
            }
        )
        
        return {
            'statusCode': 200,
            'headers': headers,
            'body': json.dumps({
                'message': 'Analysis complete',
                'document_id': document_id,
                'analysis': ai_analysis,
                'timestamp': timestamp
            })
        }
        
    except Exception as e:
        print(f"Error: {str(e)}")
        return {
            'statusCode': 500,
            'headers': headers,
            'body': json.dumps({'error': str(e)})
        }
