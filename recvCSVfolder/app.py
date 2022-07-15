import json
import boto3
import csv
import io
import pandas as pd 
from pandas import DataFrame
import awswrangler as wr
# import pyodbc 
from datetime import datetime
import typing

s3Client = boto3.client('s3')

# def form_message(df:DataFrame) -> object:
#     for i in range(len(df)):
#         # print(df.loc[i, "Name"], df.loc[i, "Age"])
#         employeeNumber = df.loc[i, "employeeNumber"]
#         lastName = df.loc[i, "lastName"]
#         firstName = df.loc[i, "firstName"]
#         extension = df.loc[i, "extension"]
#         email = df.loc[i, "email    "]
#         officeCode = df.loc[i, "officeCode"]
#         reportsTo = df.loc[i, "reportsTo"]
#         jobTitle = df.loc[i, "jobTitle"]

sqsClient = boto3.client('sqs')
    
#     return {"subject": "none"}


def lambda_handler(event, context):

    bucket = event['Records'][0]['s3']['bucket']['name']
    ingest_key = event['Records'][0]['s3']['object']['key']

    print(bucket, ingest_key)

    response = s3Client.get_object(Bucket=bucket, Key=ingest_key)
    queue_url = "https://sqs.ap-southeast-2.amazonaws.com/549219412834/bridge.fifo"

    lambda_arn = "arn:aws:lambda:ap-southeast-2:549219412834:function:recvCSVapp-ReceiveCSVFunc-78QJuAD3jS0t"


    try:
        df_in_data = pd.read_csv(response['Body'], sep=',')
        if 'op' in df_in_data:
            message1 = None
            # form_message(df_in_data)
            message_group_id = 0
            for i in range(len(df_in_data)):
                # employeeNumber = df.loc[i, "employeeNumber"]
                # lastName = df.loc[i, "lastName"]
                # firstName = df.loc[i, "firstName"]
                # extension = df.loc[i, "extension"]
                # email = df.loc[i, "email"]
                # officeCode = df.loc[i, "officeCode"]
                # reportsTo = df.loc[i, "reportsTo"]
                # jobTitle = df.loc[i, "jobTitle"]
                message_group_id += 1
                message1 = {
                    "op": df_in_data.loc[i, "op"],
                    "employeeNumber": int(df_in_data.loc[i, "employeeNumber"]),
                    "lastName": df_in_data.loc[i, "lastName"],
                    "firstName": df_in_data.loc[i, "firstName"],
                    "extension": df_in_data.loc[i, "extension"],
                    "email": df_in_data.loc[i, "email"],
                    "officeCode": int(df_in_data.loc[i, "officeCode"]),
                    "reportsTo": df_in_data.loc[i, "reportsTo"],
                    "jobTitle": df_in_data.loc[i, "jobTitle"]
                }

                lambda_arn = "arn:aws:lambda:ap-southeast-2:549219412834:function:recvCSVapp-ReceiveCSVFunc-78QJuAD3jS0t"

                body = {
                    "lambda_arn": lambda_arn,
                    "data": message1
                }

                response = sqsClient.send_message(
                    QueueUrl=queue_url,
                    MessageGroupId=str(message_group_id),
                    MessageBody=json.dumps(body)
                )

        else:
            message2 = None
            message_group_id = 0
            for i in range(len(df_in_data)):
                message_group_id += 1
                message2 = {
                    "employeeNumber": int(df_in_data.loc[i, "employeeNumber"]),
                    "lastName": df_in_data.loc[i, "lastName"],
                    "firstName": df_in_data.loc[i, "firstName"],
                    "extension": df_in_data.loc[i, "extension"],
                    "email": df_in_data.loc[i, "email"],
                    "officeCode": int(df_in_data.loc[i, "officeCode"]),
                    "reportsTo": df_in_data.loc[i, "reportsTo"],
                    "jobTitle": df_in_data.loc[i, "jobTitle"]
                }

                body = {
                    "lambda_arn": lambda_arn,
                    "data": message2
                }

                response = sqsClient.send_message(
                    QueueUrl=queue_url,
                    MessageGroupId=str(message_group_id),
                    MessageBody=json.dumps(body)
                )

    except Exception as e:
        raise e 



    return None
