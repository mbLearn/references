# This file is your Lambda function
import json
import boto3


def save_to_bucket(event, context):
    AWS_BUCKET_NAME = 'my-bucket-name'
    s3 = boto3.resource('s3')
    bucket = s3.Bucket(AWS_BUCKET_NAME)
    path = 'my-path-name.txt'
    data = b'Here we have some data'
    bucket.put_object(
        ACL='public-read',
        ContentType='application/json',
        Key=path,
        Body=data,
    )

    body = {
        "uploaded": "true",
        "bucket": AWS_BUCKET_NAME,
        "path": path,
    }
    return {
        "statusCode": 200,
        "body": json.dumps(body)
    }
