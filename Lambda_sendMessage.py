import boto3
import json
import time
import logging

# Initialize DynamoDB resource
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('ChatMessages')

# Configure logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    try:
        # Parse the request body
        body = json.loads(event.get('body', '{}'))
        message = body.get('message', '').strip()
        connection_id = event.get('requestContext', {}).get('connectionId')
        timestamp = body.get('timestamp', int(time.time()))  # Default to current timestamp if not provided

        # Validate required fields
        if not message or not connection_id:
            logger.warning("Validation failed: Missing 'message' or 'connectionId'")
            return {
                'statusCode': 400,
                'body': json.dumps({'error': 'Fields "message" and "connectionId" are required.'})
            }

        # Log the incoming data
        logger.info(f"Storing message for ConnectionId: {connection_id} at {timestamp}")

        # Save the data in DynamoDB
        table.put_item(
            Item={
                'ConnectionId': connection_id,  # Partition key
                'Timestamp': int(timestamp),   # Sort key (optional)
                'Message': message
            }
        )

        # Success response
        return {
            'statusCode': 200,
            'body': json.dumps({'message': 'Message stored successfully'})
        }

    except Exception as e:
        # Error handling
        logger.error(f"Error storing data: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({'error': 'Failed to store data', 'details': str(e)})
        }
