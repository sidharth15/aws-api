import json

def lambda_handler(event, context):
    print("Received event ", event)

    return {'status':200, 'message':'success'}