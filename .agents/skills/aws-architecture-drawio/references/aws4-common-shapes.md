# Verified Common AWS4 Shapes

These names are intended for draw.io's built-in AWS4 library.

Use the resource icon pattern:

```text
shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.<name>;
```

Common verified resource-icon names:

| AWS service | AWS4 `resIcon` name |
|---|---|
| AWS Lambda | `lambda` |
| Amazon API Gateway | `api_gateway` |
| Amazon S3 | `s3` |
| Amazon SQS | `sqs` |
| Amazon SNS | `sns` |
| AWS Step Functions | `step_functions` |
| Amazon DynamoDB | `dynamodb` |
| AWS Glue Data Catalog | `glue_data_catalog` |
| Amazon Aurora | `aurora` |
| Amazon RDS | `rds` |
| Amazon Cognito | `cognito` |
| Amazon Bedrock | `bedrock` |
| Amazon SageMaker | `sagemaker` |
| Amazon Textract | `textract` |
| Amazon Comprehend | `comprehend` |
| AWS Amplify | `amplify` |
| Amazon OpenSearch Service | `elasticsearch_service` |
| Amazon EC2 | `ec2` |
| Amazon Route 53 | `route_53` |
| Amazon CloudFront | `cloudfront` |
| AWS Identity and Access Management | `identity_and_access_management` |
| AWS Secrets Manager | `secrets_manager` |
| AWS Key Management Service | `key_management_service` |
| AWS WAF | `waf` |
| Amazon EventBridge | `eventbridge` |
| Amazon CloudWatch | `cloudwatch_2` |

`elasticsearch_service` is the verified AWS4 resource-icon identifier currently used by draw.io for Amazon OpenSearch Service. Do not rename it to an inferred `opensearch` identifier.

For services not listed here, do not infer the stencil name from the marketing name. Search or inspect the current AWS4 shape catalog first.

When a new service is verified, add it to this table before using it. Keep the service's canonical label separate from the stencil identifier; the two often differ.

## Important model/icon rule

A foundation model such as Claude, Amazon Titan, or another Bedrock-hosted model is not automatically a separate AWS service stencil.

When a dedicated model glyph is unavailable, use the Amazon Bedrock service icon and label it with the specific model, for example:

`Amazon Bedrock`
`Claude model`

Do not invent a fake `mxgraph.aws4.*` name.
