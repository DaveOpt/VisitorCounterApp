import boto3
import json
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('VisitorCount')

def lambda_handler(event, context):
    logger.info('Function started, attempting to update visitor count.')
    try:
        response = table.update_item(
            Key={'visitorID': 'total_visits'},
            UpdateExpression="set #count = if_not_exists(#count, :start) + :inc",
            ExpressionAttributeNames={'#count': 'count'},
            ExpressionAttributeValues={':inc': 1, ':start': 0},
            ReturnValues="UPDATED_NEW"
        )
        
        current_count = int(response['Attributes']['count'])
        logger.info(f'Updated count to: {current_count}')
        
        return {
            'statusCode': 200,
            'body': json.dumps({'visitor_count': current_count}),
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Content-Type': 'application/json'
            }
        }
    except Exception as e:
        logger.error(f'Failed to update visitor count: {e}')
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)}),
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Content-Type': 'application/json'
            }
        }