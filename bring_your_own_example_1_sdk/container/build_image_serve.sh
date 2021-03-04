#!/usr/bin/env bash

# This script builds the Docker image and pushes it to ECR to be ready for use

# Update shell session proxy
export HTTPS_PROXY=***
export HTTP_PROXY=***
export NO_PROXY=***

algorithm_name=$1

# Build image
chmod -R +x src/

# Get FCST United ECR account ID
account=$(aws sts get-caller-identity --query Account --output text)
# Get the region defined in the current configuration
region=$(aws configure get region)
fullname="${account}.dkr.ecr.${region}.amazonaws.com/${algorithm_name}:latest"

# If the repository doesn't exist in ECR, create it
aws ecr describe-repositories --repository-names "${algorithm_name}" > /dev/null 2>&1
if [ $? -ne 0 ]
then
    aws ecr create-repository --repository-name "${algorithm_name}" > /dev/null
fi

# Get the login command from ECR and execute it directly
$(aws ecr get-login --region ${region} --registry-ids ${account} --no-include-email)

# Build the docker image locally with the image name and then push it to ECR
# with the full name.
docker build  --no-cache --rm --force-rm --pull \
              --file 'container/Dockerfile_serve' -t ${algorithm_name} \
              .
docker tag ${algorithm_name} ${fullname}
docker push ${fullname}

# Clean
docker rmi ${algorithm_name}
docker rmi ${fullname}