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
