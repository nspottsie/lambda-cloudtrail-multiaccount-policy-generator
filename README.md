## About
Lambda function using to handle creating a S3 Cloudtrail bucket policy for multiple AWS account ids

## Prerequisits
1. Install [Docker](https://docs.docker.com/engine/installation/)
2. Install [SAM Local](https://github.com/awslabs/aws-sam-local#installation)

## Usage
For testing the function locally, run the following command:
`sam local invoke CloudTrailMultiAccountPolicyGenerator --event event.json`

## Environment Variables
The function takes the following configurable environment variables:

| Name                  | Description                                                       | Required |
| --------------------- | ----------------------------------------------------------------- | -------- |
| BUCKET_NAME           | The target S3 bucket name for CloudTrail events                   | True     |
| CLOUDTRAIL_LOG_PREFIX | The log prefix configured for CloudTrail events                   | True     |
| ACCOUNTS_PER_BUCKET   | The total number of accounts to associate with a single S3 bucket | True     |

## Event Configuration
The event data passed into the Lambda function should include an array of account ids that are allowed to write CloudTrail events into the destination bucket.

```
{
  "resources": ...,
  "accountIds": [
    "123456789",
    "987654321"
  ]
}
```
