# Cleanup Notes

After finishing your demo, delete the CloudFormation stack to avoid ongoing charges.

## Delete the stack

```bash
aws cloudformation delete-stack --stack-name cloud-platform-demo
```

## Confirm deletion

```bash
aws cloudformation describe-stacks --stack-name cloud-platform-demo
```

Once deletion completes, the following resources will be removed:
- EC2 instance
- Security group
- IAM role and instance profile
- CloudWatch log group and metric filter
- CloudWatch alarm

## S3 bucket

CloudFormation **cannot** delete a non-empty S3 bucket. Empty it first:

```bash
aws s3 rm s3://cloud-platform-demo-artifacts-<YOUR_ACCOUNT_ID> --recursive
```

Then re-run the stack deletion, or delete the bucket manually:

```bash
aws s3 rb s3://cloud-platform-demo-artifacts-<YOUR_ACCOUNT_ID> --force
```

## Estimated cost

Running a `t2.micro` instance for a few hours falls within the AWS free tier
(750 hours/month for new accounts). CloudWatch Logs ingestion is minimal for
this demo workload. Always verify against your account's free-tier status.
