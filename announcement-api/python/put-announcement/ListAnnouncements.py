import json
import uuid
import boto3

print("Initializing lambda")

ANNOUNCEMENT_TABLE_NAME = "announcements"
PAGINATION_TOKEN = "pagination_token"
TITLE_ATTRIBUTE = "title"
DATE_ATTRIBUTE = "date"
ID_ATTRIBUTE = "AnnouncementId"

dynamo = boto3.resource('dynamodb')
announcementTable = dynamo.Table(ANNOUNCEMENT_TABLE_NAME)

# method to parse the event input
# and retrieve a start key for continuing scan
def parse_event(event):
    if event[PAGINATION_TOKEN]:
        return {
            ID_ATTRIBUTE: event[PAGINATION_TOKEN]
        }

def is_startKey_valid(startKey):
    response = announcementTable.get_item(Key=startKey)
    # print(response)
    
    return 'Item' in response
    
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
    
def lambda_handler(event, context):
    print("Handling event:", event)
    
    startKey = parse_event(event)

    if startKey:
        print('using pagination_token: ', startKey)
        
        if not is_startKey_valid(startKey):
            response = build_response(
                statusCode=400, 
                message="Invalid pagination_token"
                )
        else:
            print('pagination_token is valid')
            
            scanResult = announcementTable.scan(
                    Limit=1,
                    ExclusiveStartKey=startKey
                )
            
            response = build_response(
                statusCode=200,
                message="SUCCESS",
                scanResult=scanResult
                )
    else:
        print('no pagination_token')
        
        scanResult = announcementTable.scan(Limit=1)
        response = build_response(
            statusCode=200,
            message="SUCCESS",
            scanResult=scanResult
            )
    
    print("Returning response: ", response)

    return response
