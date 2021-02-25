# aws-api
Microservice setup in AWS using purely serverless services.

# Description
This project demonstrates a typical API that can be setup in the cloud, making use of serverless services. Here, we are using AWS as the cloud provider and consuming services like AWS Lambda, API Gateway and DynamoDB. The entire application infrastructure is defined using CloudFormation.

# Setting Up
Since the entire infrastructure used in this project is defined using CloudFormation in an infra-as-code manner, the setup can be launched easily just by running CloudFormation:deploy-stack on the main.cfn.yaml file. 

However, please note that the source code S3 bucket referred in this project is specific to the AWS account. You will need to specify the S3 bucket where you deploy all the cloudformation scripts and lambda function code.

# Usage
The micrservice consists of two separate APIs - put_announcement and list_announcements. After deploying the main cloudformation stack, the endpoint URLs of the two APIs are available in the 'Outputs' section of the main stack.
