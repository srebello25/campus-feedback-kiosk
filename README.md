# Campus Feedback Kiosk (AWS Cloud-Native Project)

This project is a cloud-native serverless application deployed on AWS. 
It allows students to submit anonymous feedback and allows admin users to view and filter the feedback.

## Folder Structure

backend/
    submitFeedback.py   - Lambda function for storing feedback in DynamoDB
    getFeedback.py      - Lambda function for retrieving feedback for admin

frontend/
    index.html          - Student feedback submission page
    admin.html          - Admin feedback viewing and filtering page

## AWS Services Used

- Amazon S3 (Static hosting for frontend)
- Amazon API Gateway (HTTP API, used to invoke Lambda for POST and GET)
- AWS Lambda (Python backend functions)
- Amazon DynamoDB (NoSQL database)
- Amazon CloudWatch (Logging and monitoring)
- Amazon SNS (Email alerts for Lambda errors)
- AWS IAM (Access control and permissions)

## How the System Works

1. Students open index.html hosted on S3.
2. They submit feedback through a form.
3. Feedback is sent through API Gateway.
4. AWS Lambda (submitFeedback) processes the request and stores data in DynamoDB.
5. Admin opens admin.html to load and filter feedback.
6. Admin fetches data through API Gateway → Lambda (getFeedback) → DynamoDB.

