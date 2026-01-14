import json
import boto3

# Create DynamoDB resource client
dynamodb = boto3.resource('dynamodb')

# Reference the DynamoDB table named "FeedbackTable"
table = dynamodb.Table('FeedbackTable')

def lambda_handler(event, context):
    
    # Scan the table to retrieve all items (full table read)
    response = table.scan()

    # Extract items from scan response, defaulting to empty list if missing
    items = response.get('Items', [])

    
    # Return HTTP response with status code, CORS headers, and JSON body
    return {
        "statusCode": 200,
        "headers": {
            "Access-Control-Allow-Origin": "*",                   # Allow access from any domain
            "Access-Control-Allow-Headers": "content-type",       # Allow specific request headers
            "Access-Control-Allow-Methods": "GET,POST,OPTIONS",   # Allowed HTTP methods
            "Content-Type": "application/json"                    # Specify response format
        },
        "body": json.dumps(items)                                 # Convert Python list to JSON string
    }

