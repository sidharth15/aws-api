import json
import uuid
import boto3

print("Initializing lambda")

ANNOUNCEMENT_TABLE_NAME = "announcements"
TITLE_ATTRIBUTE = "title"
DATE_ATTRIBUTE = "date"

dynamo = boto3.resource('dynamodb')
announcementTable = dynamo.Table(ANNOUNCEMENT_TABLE_NAME)

def validate_input(event):
    return TITLE_ATTRIBUTE in event and DATE_ATTRIBUTE in event and event[TITLE_ATTRIBUTE] and event[DATE_ATTRIBUTE]

def lambda_handler(event, context):
    print("Handling event ", event)
    
    if validate_input(event):
        new_item = {
            "AnnouncementId": str(uuid.uuid4()),
            "title": event[TITLE_ATTRIBUTE],
            "date": event[DATE_ATTRIBUTE]
        }
        
        announcementTable.put_item(Item=new_item)
    else:
        print("Invalid input received.")

    return {'status':200, 'message':'success'}