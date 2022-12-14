import json
import boto3
import requests
import os
from datetime import datetime, timezone
from decimal import Decimal


dynamoDB = boto3.resource("dynamodb")
table = dynamoDB.Table(os.environ['DynamoDB_table'])


def lambda_handler(event, context):
    
    response = requests.get(f"https://api.openweathermap.org/data/2.5/weather?lat={event['device_lat']}&lon={event['device_lon']}&appid={os.environ['API_Key']}&units=metric")
    temp = json.loads(response.text, parse_float=Decimal)["main"]["temp"]
    sensor_temp = Decimal(str(event["temperature"]))
    
    data = {"timestamp": Decimal(datetime.now(timezone.utc).timestamp()), 
        "device_id": event["device_id"], 
        "sensor_time": event["sensor_time"] ,
        "sensor_temp": sensor_temp,
        "openweather_temp": temp,
        "temp_diff": temp - sensor_temp
    }
    
    table.put_item(Item=data)
    
    
    
    return {
        'statusCode': 200,
        'body': data
    }