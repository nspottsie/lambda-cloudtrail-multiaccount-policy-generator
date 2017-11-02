import logging
import json
import os

# setup logger
logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)


def lambda_handler(event: dict, context):
    # parse environment variables and event data
    bucket_name = os.environ['BUCKET_NAME']
    log_prefix = os.environ['CLOUDTRAIL_LOG_PREFIX']
    accounts_per_bucket = int(os.environ['ACCOUNTS_PER_BUCKET'])
    accounts = event['accountIds']

    # segment the total list of accounts to limit the accounts per bucket
    account_segments = [accounts[i:i + accounts_per_bucket] for i in range(0, len(accounts), accounts_per_bucket)]

    # iterate over the segments, creating a bucket policy for each
    for account_segment in account_segments:
        policy = create_policy(bucket_name, log_prefix, account_segment)
        json_text = json.dumps(policy, indent=4, separators=(',', ': '))
        log.info(json_text)


def create_policy(bucket_name, log_prefix, account_ids):
    # create the S3 bucket policy based off the documentation found here:
    # http://docs.aws.amazon.com/awscloudtrail/latest/userguide/cloudtrail-set-bucket-policy-for-multiple-accounts.html

    # turn the list of account ids into full amazon resource namespaces
    account_arns = list(map(lambda account_id: "arn:aws:s3:::" + bucket_name + "/" + log_prefix + "/AWSLogs/" + account_id + "/*", account_ids))

    # create the bucket policy with the current list of account arns
    return {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Sid": "AWSCloudTrailAclCheck20131101",
                "Effect": "Allow",
                "Principal": {
                    "Service": "cloudtrail.amazonaws.com"
                },
                "Action": "s3:GetBucketAcl",
                "Resource": "arn:aws:s3:::" + bucket_name
            },
            {
                "Sid": "AWSCloudTrailWrite20131101",
                "Effect": "Allow",
                "Principal": {
                    "Service": "cloudtrail.amazonaws.com"
                },
                "Action": "s3:PutObject",
                "Resource": account_arns,
                "Condition": {
                    "StringEquals": {
                        "s3:x-amz-acl": "bucket-owner-full-control"
                    }
                }
            }
        ]
    }
