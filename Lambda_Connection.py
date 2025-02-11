import json

def lambda_handler(event, context):
    print(f"Connection ID: {event['requestContext']['connectionId']}")
    return {'statusCode': 200, 'body': 'Connected'}

