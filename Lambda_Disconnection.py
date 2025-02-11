import json

def lambda_handler(event, context):
    print(f"Disconnected: {event['requestContext']['connectionId']}")
    return {'statusCode': 200, 'body': 'Disconnected'}

