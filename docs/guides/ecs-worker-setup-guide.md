## Prerequisites

Before you begin, make sure you have the following prerequisites in place:
- An AWS account with permissions to create ECS services and IAM roles.
- The AWS CLI installed on your local machine. You can download it from the AWS website.
- A Docker image of your Prefect worker, which you can build and push to an Amazon ECR registry.
## Step 1: Create an IAM Role for the ECS Task

First, you need to create an IAM role that the ECS task will use to access AWS resources. Here are the steps:
1. Open the IAM console and click on "Roles" in the left sidebar.
2. Click on the "Create role" button.
3. Select "ECS" as the trusted entity type and click on "Next: Permissions".
4. Select the "AmazonECSTaskExecutionRolePolicy" policy and click on "Next: Tags".
5. Add any tags you want to the role and click on "Next: Review".
6. Enter a name for the role (e.g., "prefect-worker-ecs-role") and click on "Create role".
## Step 2: Create a Task Definition

Next, you need to create an ECS task definition that specifies the Docker image for the Prefect worker, the resources it requires, and the command it should run. Here are the steps:
1. Use prefect config view to see the values for `PREFECT_API_URL`. For the `PREFECT_API_KEY`, organization tier can create a [service account](https://docs.prefect.io/latest/cloud/users/service-accounts/) for the worker, personal tiers can pass a user’s API key here.

2. Create a JSON file with the following contents:

```json

{
  "family": "prefect-worker-task",
  "networkMode": "awsvpc",
  "taskRoleArn": "<your-ecs-task-role-arn>",
  "executionRoleArn": "<your-ecs-task-role-arn>",
  "containerDefinitions": [
    {
      "name": "prefect-worker",
      "image": "<your-ecr-image>",
      "cpu": 512,
      "memory": 1024,
      "essential": true,
      "command": [
        "prefect",
        "execute",
        "cloud",
        "--label",
        "worker"
      ]
      "environment": [
        {
          "name": "PREFECT_API_URL",
          "value": "https://api.prefect.cloud/api/accounts <replaced>/workspaces/<replaced>"
        },
        {
          "name": "PREFECT_API_KEY",
          "value": "abc_12345678910"
        }
      ]
    }
  ]
}
```

Replace `<your-ecs-task-role-arn>` with the ARN of the IAM role you created in Step 1, and `<your-ecr-image>` with the URI of the Docker image you pushed to Amazon ECR.
1. Save the JSON file to your local machine.
## Step 3: Create an ECS Service

Finally, you can create an ECS Fargate service that will run your Prefect worker task without needing to manage the underlying EC2 instances. Here are the steps:
1. Open a terminal window and run the following command to create an ECS Fargate service:

```lua

aws ecs create-service \
    --service-name prefect-worker-service \
    --cluster <your-ecs-cluster> \
    --task-definition file://<path-to-task-definition-file>.json \
    --launch-type FARGATE \
    --desired-count 1 \
    --network-configuration "awsvpcConfiguration={subnets=[<your-subnet-ids>],securityGroups=[<your-security-group-ids>]}"
```



Replace `<your-ecs-cluster>` with the name of your ECS cluster, `<path-to-task-definition-file>` with the path to the JSON file you created in Step 2, `<your-subnet-ids>` with a comma-separated list of your VPC subnet IDs, and `<your-security-group-ids>` with a comma-separated list of your VPC security group IDs.
1. Wait for the ECS service to be created. You can check its status by running the following command:

```sql

aws ecs describe
```

*Sanity Check* 
Work pool page will allow you to reference any newly created workers
* Insert screenshot


## Prerequisites

Before you begin, make sure you have the following prerequisites in place:
- An AWS account with permissions to create ECS services and IAM roles.
- The AWS CLI installed on your local machine. You can download it from the AWS website.
- A Docker image of your Prefect worker, which you can build and push to an Amazon ECR registry.
## Step 1: Create an IAM Role for the ECS Task

First, you need to create an IAM role that the ECS task will use to access AWS resources. Here are the steps:
1. Open the IAM console and click on "Roles" in the left sidebar.
2. Click on the "Create role" button.
3. Select "ECS" as the trusted entity type and click on "Next: Permissions".
4. Select the "AmazonECSTaskExecutionRolePolicy" policy and click on "Next: Tags".
5. Add any tags you want to the role and click on "Next: Review".
6. Enter a name for the role (e.g., "prefect-worker-ecs-role") and click on "Create role".
## Step 2: Create a Task Definition

Next, you need to create an ECS task definition that specifies the Docker image for the Prefect worker, the resources it requires, and the command it should run. Here are the steps:
1. Use prefect config view to see the values for `PREFECT_API_URL`. For the `PREFECT_API_KEY`, organization tier can create a [service account](https://docs.prefect.io/latest/cloud/users/service-accounts/) for the worker, personal tiers can pass a user’s API key here.

2. Create a JSON file with the following contents:

```json

{
  "family": "prefect-worker-task",
  "networkMode": "awsvpc",
  "taskRoleArn": "<your-ecs-task-role-arn>",
  "executionRoleArn": "<your-ecs-task-role-arn>",
  "containerDefinitions": [
    {
      "name": "prefect-worker",
      "image": "<your-ecr-image>",
      "cpu": 512,
      "memory": 1024,
      "essential": true,
      "command": [
        "prefect",
        "execute",
        "cloud",
        "--label",
        "worker"
      ]
      "environment": [
        {
          "name": "PREFECT_API_URL",
          "value": "https://api.prefect.cloud/api/accounts <replaced>/workspaces/<replaced>"
        },
        {
          "name": "PREFECT_API_KEY",
          "value": "abc_12345678910"
        }
      ]
    }
  ]
}
```

Replace `<your-ecs-task-role-arn>` with the ARN of the IAM role you created in Step 1, and `<your-ecr-image>` with the URI of the Docker image you pushed to Amazon ECR.
1. Save the JSON file to your local machine.
## Step 3: Create an ECS Service

Finally, you can create an ECS Fargate service that will run your Prefect worker task without needing to manage the underlying EC2 instances. Here are the steps:
1. Open a terminal window and run the following command to create an ECS Fargate service:

```lua

aws ecs create-service \
    --service-name prefect-worker-service \
    --cluster <your-ecs-cluster> \
    --task-definition file://<path-to-task-definition-file>.json \
    --launch-type FARGATE \
    --desired-count 1 \
    --network-configuration "awsvpcConfiguration={subnets=[<your-subnet-ids>],securityGroups=[<your-security-group-ids>]}"
```



Replace `<your-ecs-cluster>` with the name of your ECS cluster, `<path-to-task-definition-file>` with the path to the JSON file you created in Step 2, `<your-subnet-ids>` with a comma-separated list of your VPC subnet IDs, and `<your-security-group-ids>` with a comma-separated list of your VPC security group IDs.
1. Wait for the ECS service to be created. You can check its status by running the following command:

```sql

aws ecs describe
```

*Sanity Check* 
Work pool page will allow you to reference any newly created workers
* Insert screenshot


## Deployment Outline
### Execution environment	
AWS ECS Fargate	ECS allows long-running jobs based on Docker images.

### Application code storage	
Custom Docker image	Storing code in a Docker image allows our local development environment to match production as closely as possible.

Refer to our [image strategy](https://docs.prefect.io/latest/concepts/infrastructure/#choosing-an-image-strategy) guide on how to create your own custom images. 

### Infrastructure as code	Terraform
Writing infrastructure in a language that developers are already familiar with gives us control over our data infrastructure, without having to depend on dev-ops.

### Continuous deployment pipeline	(Github Actions)	
The most streamlined way to automatically build our infrastructure.

## Set up Infrastructure Requirements
Before getting deployed:
### Requirements
- Amazon ECS cluster: Deployment group
- Amazon ECS service: Deployment group
- ~~Application Load Balancer or Network Load Balancer: Deployment group~~
- ~~Production listener: Deployment group~~
- Test listener (optional): Deployment group
- ~~Two target groups: Deployment group~~
- Amazon ECS task definition (Optional)
- ~~Container name: AppSpec file~~
- ~~Container port: AppSpec file~~

Find more set up information at the [AWS Deployments documentation](https://docs.aws.amazon.com/codedeploy/latest/userguide/deployment-steps-ecs.html)
### Here are the steps to set up AWS ECS for deployments:

1. Create a new Amazon ECS cluster: Start by logging into the AWS Management Console and navigating to the Amazon ECS service. Click "Create Cluster" and choose the type of cluster you want to create (EC2 or Fargate). Follow the prompts to set up the basic configuration, including the cluster name, region, and VPC.

2. Create a task definition: A task definition is a blueprint for your containerized application. In the ECS console, click "Task Definitions" and then "Create new Task Definition." Choose the type of task you want to create (EC2 or Fargate) and configure the basic settings, including the task name, IAM role, and network mode.

3. Define your container(s): In the task definition, you'll need to specify the container image, port mappings, and any environment variables or other settings your application requires. You can add multiple containers to a single task definition if needed.


## ECS Worker Documentation
### Pre requisites
- A Fargate [ECS cluster](https://docs.aws.amazon.com/AmazonECS/latest/userguide/getting-started-fargate.html#get-started-windows-fargate-cluster)
  * unless you’re doing EC2 launch type which then requires an EC2 instances running the ECS AMI
- An execution role with permissions for Cloudwatch logs
- A VPC

### Outline
1. Install prefect-aws
2. Create a work pool with ```prefect work-pool create --type ecs ecs```
3. Configure the work pool with a VPC through the UI
4. Start the worker ```prefect worker start -p ecs```

5. Now your worker will be polling for any flows scheduled with the ecs work pool


### ECS Raw dev notes
- What needs to be configured?
- Need VPC and Cluster configured in the work pool if 'default' cluster does not exist and need to specify the region
- Was able to use the ecs task to run the work, but it was pulling from a non existent path in AWS, going to test out the projects way

* Cannot use remote storage blocks, need to configure it through projects or programtically creating deployment objects

### Projects Implementation Notes
- Got the deployment.yaml file correctly configured
- Running prefect deploy does not push to S3
- Need to use projects in order to hook up the storage location correctly (S3?)
- [ECS task is being run](https://app.prefect.cloud/account/0ff44498-d380-4d7b-bd68-9b52da03823f/workspace/80d66ded-76f2-46fe-98e6-576ebe2a707c/flow-runs/flow-run/a1cf0d4c-ceb5-4044-b929-9256294a7c98), but not finding the flow location -> need to refactor to a Project example so its less decoupled


- Can override the infra components of the work pool to specify entrypoints


# ECS Worker Quick Start Guide

## Requirements:

### Prefect's side:
- Create an ECS work pool that will house the ECS workers
- Create an AWS credenentials block 

### AWS Side:
- Create an ECS cluster
- Must set up a preconfigured VPC attached with the ECS cluster
- Create custom task definition (Optional)

### Docker Image:
- 


