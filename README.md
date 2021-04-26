# aws-lambda-ses
A small repo to demonstrate making a Lambda function send an email with an attachment via SES.  
Note that SNS can send email but can not attach files. To attach files we need to use the SES raw email functional described [here](https://docs.aws.amazon.com/ses/latest/dg/send-email-raw.html).


## Verify Sender and Reciever email addresses
To send the email you will have to verify both the sender and receiver email addresses in SES. The instructions to do so are clearly defined [here](https://docs.aws.amazon.com/ses/latest/DeveloperGuide/verify-email-addresses-procedure.html). 
When you invoke the Lambda function, you will have to replace `sender@example.com` and `receiver@example.com` with your verified email addresses.

## Place a file in S3 to attached
The Lambda function will copy a file from S3 to the Lambda's local storage and then pass it to SES from there. 
Therefore you must create a S3 bucket file the file to attach in it. When you invoke the Lambda function you will have to 
enter your `<bucket>` and `<file_name>`.


## Create Lambda Function Role
We need to create an IAM role that the can be attached to the lambda function when it is deployed.   
We'll reuse the `lambda-demo` role created in [this](https://github.com/daniel-fudge/aws-s3-trigger) repo. 
You will have to replace `<your lambda role arn>` with your role ARN in the Lambda create command below. 

## Create Lambda to send the email with an attachment 
The following commands will create the lambda function.
```shell
zip package.zip lambda_function.py
aws lambda create-function \
  --function-name demo-ses \
  --role <your lambda role arn> \
  --runtime python3.8 --timeout 10 --memory-size 128 \
  --handler lambda_function.lambda_handler \
  --zip-file fileb://package.zip
rm -f package.zip
```

It may also be useful to update the package through the CLI with the following command.
```shell
rm -f package.zip
zip package.zip lambda_function.py
aws lambda update-function-code --function-name demo-ses --zip-file fileb://package.zip
```

### Test deployed function
```shell
rm response.json
aws lambda invoke \
  --function-name demo-ses \
  --payload '{"sender": "Sender Name <sender@example.com>", "receiver": "receiver@example.com", "bucket": "<bucket>", "file_name": "<file_name>"}' \
  --cli-binary-format raw-in-base64-out \
  response.json
```
You should see a `200` status code and the `response.json` file should contain `{"return_message": "Email sent! Message ID: SOME-LONG-ID"}`. 

## References
- [AWS SES Raw Email](https://docs.aws.amazon.com/ses/latest/dg/send-email-raw.html)
- [AWS SES Email Verification](https://docs.aws.amazon.com/ses/latest/DeveloperGuide/verify-email-addresses-procedure.html)
- [C++ Lambda Function with Python Handler](https://github.com/daniel-fudge/aws-lambda-cpp-python#make-iam-role-for-the-lambda-function)
- [Cloud9 C++ Lambda Repo](https://github.com/daniel-fudge/aws-lambda-cpp-cloud9)
- [AWS CLI - Installation](https://docs.aws.amazon.com/cli/latest/userguide/install-cliv2-linux.html)
- [AWS CLI - Add permissions](https://awscli.amazonaws.com/v2/documentation/api/latest/reference/lambda/add-permission.html)
- [AWS CLI - Invoke Lambda](https://docs.aws.amazon.com/cli/latest/reference/lambda/invoke.html#examples)
- [AWS CLI - Payload Error](https://stackoverflow.com/questions/60310607/amazon-aws-cli-not-allowing-valid-json-in-payload-parameter)
- [AWS Lambda Runtimes](https://docs.aws.amazon.com/lambda/latest/dg/lambda-runtimes.html)
