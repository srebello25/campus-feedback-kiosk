import json
import uuid
import boto3
from datetime import datetime

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('FeedbackTable')  # make sure this name matches your table

def lambda_handler(event, context):
    # Common CORS + JSON headers
    headers = {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Headers": "Content-Type",
        "Access-Control-Allow-Methods": "OPTIONS,GET,POST",
        "Content-Type": "application/json"
    }

    # Detect HTTP method (for HTTP API Gateway)
    method = event.get("requestContext", {}).get("http", {}).get("method", "GET")

    # Handle CORS preflight
    if method == "OPTIONS":
        return {
            "statusCode": 200,
            "headers": headers,
            "body": json.dumps({"message": "OK"})
        }

    # POST = create new feedback
    if method == "POST":
        body_str = event.get("body") or "{}"

        try:
            body = json.loads(body_str)
        except json.JSONDecodeError:
            return {
                "statusCode": 400,
                "headers": headers,
                "body": json.dumps({"message": "Invalid JSON in request body"})
            }

        feedback_text = (body.get("feedback") or "").strip()
        category = body.get("category", "Other")

        if not feedback_text:
            return {
                "statusCode": 400,
                "headers": headers,
                "body": json.dumps({"message": "Feedback is required"})
            }

        item = {
            "feedbackId": str(uuid.uuid4()),
            "feedback": feedback_text,
            "category": category,
            "createdAt": datetime.utcnow().isoformat()
        }

        table.put_item(Item=item)

        return {
            "statusCode": 200,
            "headers": headers,
            "body": json.dumps({"message": "Feedback submitted successfully"})
        }

    # GET = list all feedback
    if method == "GET":
        response = table.scan()
        items = response.get("Items", [])

        # Optional: sort newest first
        try:
            items.sort(key=lambda x: x.get("createdAt", ""), reverse=True)
        except Exception:
            pass

        return {
            "statusCode": 200,
            "headers": headers,
            "body": json.dumps(items)
        }

    # Anything else
    return {
        "statusCode": 405,
        "headers": headers,
        "body": json.dumps({"message": f"Method {method} not allowed"})
    }