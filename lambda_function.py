import json
import os
import boto3
from botocore.exceptions import ClientError
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication

s3 = boto3.client("s3")

def lambda_handler(event, context):
    
    # Echo the received event package for debugging and parce it
    # --------------------------------------------------------------------------
    print(event)
    sender = event['sender']
    receiver = event['receiver']
    bucket = event['bucket']
    file_name = event['file_name']
    
    # Set some simple parameters
    # --------------------------------------------------------------------------
    region = os.environ['AWS_REGION']
    subject = "Testing SES 1"
    
    # Download file and create attachment object
    # --------------------------------------------------------------------------
    attachment_path = '/tmp/' + file_name
    s3.download_file(bucket, file_name, attachment_path)
    attachment = MIMEApplication(open(attachment_path, 'rb').read())
    attachment.add_header('Content-Disposition', 'attachment', 
                          filename=file_name)
    
    # Create, encode and attach message body 
    # --------------------------------------------------------------------------
    html_body = """\
    <html>
    <head></head>
    <body>
    <h1>Hello!</h1>
    <p>This is a test email (HTML).</p>
    </body>
    </html>
    """
    CHARSET = "utf-8"
    encoded_body = MIMEText(html_body.encode(CHARSET), 'html', CHARSET)
    message_body = MIMEMultipart('alternative')
    message_body.attach(encoded_body)
    
    # Create mixed message object and attach child objects
    # --------------------------------------------------------------------------
    message = MIMEMultipart('mixed')
    message['Subject'] = subject
    message['From'] = sender
    message['To'] = receiver
    message.attach(attachment)
    message.attach(message_body)

    # Send the email!!!
    # --------------------------------------------------------------------------
    client = boto3.client('ses', region_name=region)
    try:
        response = client.send_raw_email(
            Source=sender,
            Destinations=[receiver],
            RawMessage={'Data':message.as_string()})
    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        return_message = "Email sent! Message ID: " + response['MessageId']
        print(return_message)
        return {'return_message': return_message}
