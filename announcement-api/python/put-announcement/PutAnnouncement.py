import json
import uuid
import boto3

print("Initializing lambda")

ANNOUNCEMENT_TABLE_NAME = "announcements"
TITLE_ATTRIBUTE = "title"
DATE_ATTRIBUTE = "date"

dynamo = boto3.resource('dynamodb')
announcementTable = dynamo.Table(ANNOUNCEMENT_TABLE_NAME)

def lambda_handler(event, context):
    print("Handling event ", event)
    
    new_item = {
        "AnnouncementId": str(uuid.uuid4()),
        "title": event[TITLE_ATTRIBUTE],
        "date": event[DATE_ATTRIBUTE]
    }
        
    announcementTable.put_item(Item=new_item)
    
    return {'status':200, 'message':'success'}