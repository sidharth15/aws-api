import json
import uuid
import boto3
import logging

ANNOUNCEMENT_TABLE_NAME = "announcements"
PAGINATION_TOKEN = "pagination_token"
TITLE_ATTRIBUTE = "title"
DATE_ATTRIBUTE = "date"
ID_ATTRIBUTE = "AnnouncementId"
MAX_ITEMS_LIMIT = 5

logger = logging.getLogger()
logger.setLevel(logging.INFO)
logger.debug("Initializing lambda")
dynamo = boto3.resource('dynamodb')
announcementTable = dynamo.Table(ANNOUNCEMENT_TABLE_NAME)

# method to parse the event input
# and retrieve a start key for continuing scan
def parse_event(event):
    if event[PAGINATION_TOKEN].strip():
        return { ID_ATTRIBUTE: event[PAGINATION_TOKEN] }

# determines if pagination_token provided is valid
# by checking if item with provided primary key exists in the table
def is_startKey_valid(startKey):
    response = announcementTable.get_item(Key=startKey)
    return 'Item' in response
    
# builds response object to be returned to API gateway
def build_response(statusCode, message, scanResult = None):
    items = []
    response =  {
        'statusCode': statusCode,
        'message': message
    }
    
    if scanResult:
        if 'Items' in scanResult:
            for item in scanResult['Items']:
                del item[ID_ATTRIBUTE]
                items.append(item)

        response['items'] = items
        if 'LastEvaluatedKey' in scanResult:
            response[PAGINATION_TOKEN] = scanResult['LastEvaluatedKey'][ID_ATTRIBUTE]
        
    return response
    
# handles event and returns response object
def handle_event(event):
    startKey = parse_event(event)

    if startKey:
        logger.debug('using pagination_token: ' + str(startKey))
        if not is_startKey_valid(startKey):
            response = build_response(
                statusCode=400, 
                message="Invalid pagination_token"
                )
        else:
            logger.debug('pagination_token is valid')
            scanResult = announcementTable.scan(
                    Limit=MAX_ITEMS_LIMIT,
                    ExclusiveStartKey=startKey
                )
            
            response = build_response(
                statusCode=200,
                message="SUCCESS",
                scanResult=scanResult
                )
    else:
        logger.debug('no pagination_token')
        scanResult = announcementTable.scan(Limit=MAX_ITEMS_LIMIT)
        response = build_response(
            statusCode=200,
            message="SUCCESS",
            scanResult=scanResult
            )
    
    return response

# entrypoint for lambda function
def lambda_handler(event, context):
    logger.info("Handling event:"+ str(event))
    
    try:
        response = handle_event(event)
    except Exception as e:
        logger.error("Error occured while handling event: " + repr(e))
        response = build_response(statusCode=500, message="Internal Server Error")
    
    logger.info("Returning response: ", response)

    return response
