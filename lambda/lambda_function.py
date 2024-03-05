import pandas as pd
import json
import boto3
from io import StringIO

def lambda_handler(event, context):
    sqs_queue_url = event['sqs_queue_url']
    s3_bucket = event['s3_bucket']
    customers_key = event['customers_file']
    orders_key = event['orders_file']
    items_key = event['items_file']

    # Read CSV files from S3
    customers_df = read_csv_from_s3(s3_bucket, customers_key)
    orders_df = read_csv_from_s3(s3_bucket, orders_key)
    items_df = read_csv_from_s3(s3_bucket, items_key)

    customers_df[['customer_reference', 'status']] = customers_df['customer_reference status'].str.split(' ', expand=True)
    customers_df.drop('customer_reference status', axis=1, inplace=True)

    # print(customers_df)

    orders_df[['order_status', 'order_reference', 'order_timestamp']] = orders_df['order_status order_reference order_timestamp'].str.split(' ', expand=True)
    orders_df.drop('order_status order_reference order_timestamp', axis=1, inplace=True)

    # print(orders_df)

    items_df[['item_name', 'quantity', 'total_price']] = items_df['item_name quantity total_price'].str.split(' ', expand=True)
    items_df.drop('item_name quantity total_price', axis=1, inplace=True)

    # print(items_df)

    messages = []
    error_messages = []

    # Process customers
    for index, customer_row in customers_df.iterrows():
        customer_reference = customer_row['customer_reference']
        customer_orders = orders_df[orders_df['customer_reference'] == customer_reference]
        if customer_orders.empty:
            error_messages.append({
                "type": "error_message",
                "customer_reference": customer_reference,
                "order_reference": None,
                "message": "Something went wrong!"
            })
        else:
            total_amount_spent = 0
            for _, order_row in customer_orders.iterrows():
                order_reference = order_row['order_reference']
                order_items = items_df[items_df['order_reference'] == order_reference]
                for _, item_row in order_items.iterrows():
                    total_amount_spent += float(item_row['total_price'])
            
            messages.append({
                "type": "customer_message",
                "customer_reference": customer_reference,
                "number_of_orders": len(customer_orders),
                "total_amount_spent": total_amount_spent
            })

    for message in messages:
        print(json.dumps(message))
        send_message_to_sqs(sqs_queue_url, json.dumps(message))


    for error_message in error_messages:
        print(json.dumps(error_message))
        send_message_to_sqs(sqs_queue_url, json.dumps(error_message))

def send_message_to_sqs(sqs_queue_url,message_body):
    sqs = boto3.client('sqs')
    response = sqs.send_message(
        QueueUrl=sqs_queue_url,
        MessageBody=message_body
    )
    return response

def read_csv_from_s3(bucket, key):
    s3 = boto3.client('s3')
    response = s3.get_object(Bucket=bucket, Key=key)
    content = response['Body'].read().decode('utf-8')
    return pd.read_csv(StringIO(content))
