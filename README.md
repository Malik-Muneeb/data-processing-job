# Data Processing Job

To deploy this Terraform code, execute the following commands:

```bash
git clone git@github.com:Malik-Muneeb/data-processing-job.git
cd data-processing-job
```

Open the `terraform.tf` file, provide your AWS profile with active credentials, and save it.

```bash
terraform init
terraform apply
```

When prompted, enter the S3 bucket name and press enter.

Review the Terraform plan, type "yes," and press enter.

Once all resources are deployed:

Go to AWS Lambda.
Open the Lambda Function named "data-processing-function."
Click on the "Test" button.
Configure the test event by passing the following JSON as an event:

```json
{
  "number_of_files": 3,
  "s3_bucket": "provide-bucket-name-here",
  "customers_file": "customers_20220130.csv",
  "items_file": "items_20220130.csv",
  "orders_file": "orders_20220130.csv",
  "sqs_queue_url": "https://sqs.<AWS_REGION>.amazonaws.com/<AWS_ACCOUNT_ID>/customer-order-message-queue"
}
```

Replace placeholders with actual values for s3_bucket, <AWS_REGION>, and <AWS_ACCOUNT_ID>.

Save the event and test the function.
You can verify the SQS message by opening the AWS SQS Queue and polling for the latest messages.

# Tasks

## Task 1
### Explain how this can be achieved in a serverless setup using services such as AWS Lambda. 

As the task states that we are getting files in an S3 bucket once a day, then we don't need to deploy servers (EC2) on AWS. This can be easily achieved by AWS Lambda functions like I did in this assignment. My lambda function is reading csv files from S3 bucket, convert into dataframe and further process it to generate and compose the results in json format and eventually I'm pushing json messages to AWS SQS so that it can utilized by the further components of the system/

## Task 2
### Write the code for the lambda function in a programming language you are familiar with 

I coded it in Python 3.10 language. You may find the code [here](https://github.com/Malik-Muneeb/data-processing-job/blob/main/lambda/lambda_function.py)


## Task 3
### Discuss the problem and your solution. 
The problem is that our partners uploads inputs in csv files while our current system is compatible to read json inputs so to generate results, we have to first convert csv into json, and my solution is exactly doing this job. Along with conversion, we need to aggregate customer data in a single message and generate error messages if there is some ambiguity in data.

### Explains how it scales
If we are getting 3 records, AWS Lambda process it and push the results into queue. However, if we starting getting thousands of records, Lambda would still process it and push the results. It scales by itself. However, If we getting so much data and lambda would not be able to process all in 15 minutes then it would timeout. In this case, we may need to consider other solutions like AWS Glue.

### what permanent storage solution will you choose for the processed data
I would choose AWS S3 for the permanent solution.

### what can be done to improve the setup 

We can do below improvents

1. This solution is not complete. It is mentioned in the assignment that we need to process the data as soon as it lands on S3 bucket. We can configure PUT events on S3 buckets and trigger the Lambda function. Lambda function validates from DynamoDB to check if all three files are uploaded or not. If all files are upload then it would trigger the final lambda to start processing the data
2. The current csv files have multiple attributes in a single column. We first have to clean the data to further process it. I think we should hand over this job to another lambda so that our solution remain scalable

## Task 4
### You are expected to create the assignment environment with the Infrastructure as Code framework of your choice. If there are additional manual steps or scripts you used, please add them to your repository as well 

I used Terraform to implement my solution. Addionally, I performed [these steps](https://github.com/Malik-Muneeb/data-processing-job/blob/main/lambda/readme.md) to create a zip package for my Lambda function.


