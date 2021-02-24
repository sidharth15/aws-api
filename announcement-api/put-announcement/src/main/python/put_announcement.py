import json
import time
import boto3
import logging

ANNOUNCEMENT_TABLE_NAME = "announcements"
TITLE_ATTRIBUTE = "title"
DATE_ATTRIBUTE = "date"
DESCRIPTION_ATTRIBUTE = "description"

logger = logging.getLogger()
logger.setLevel(logging.INFO)
logger.debug("Initializing lambda")

dynamo = boto3.resource('dynamodb')
announcementTable = dynamo.Table(ANNOUNCEMENT_TABLE_NAME)

def get_timestamp():
	return str(time.time()).replace('.', '')

def handle_event(event):
    new_item = {
        "AnnouncementId": get_timestamp(),
        "title": event[TITLE_ATTRIBUTE],
        "date": event[DATE_ATTRIBUTE],
        "description": event[DESCRIPTION_ATTRIBUTE]
    }
        
    announcementTable.put_item(Item=new_item)

def lambda_handler(event, context):
    logger.debug("Handling event " + str(event))
    
    try:
        handle_event(event)
    except Exception as e:
        logger.error("Error occurred while handling event: " + repr(e))
        raise Exception("Internal Server Error")
    
    return {'status':200, 'message':'success'}