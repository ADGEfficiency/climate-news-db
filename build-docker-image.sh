#!/usr/bin/env bash

ACCOUNTNUM=$1
IMAGENAME=$2
DOCKERFILE=$3
AWSPROFILE=${4:-default}

BRAND=$(sysctl -n machdep.cpu.brand_string)
echo "brand is $BRAND"

if [[ $BRAND == "Apple M1" ]];
then
  echo "building M1 - profile $AWSPROFILE - dockerfile $DOCKERFILE"
  aws ecr get-login-password --profile $AWSPROFILE | docker login --username AWS --password-stdin $ACCOUNTNUM.dkr.ecr.ap-southeast-2.amazonaws.com
  docker buildx build --platform linux/amd64 -t $ACCOUNTNUM.dkr.ecr.ap-southeast-2.amazonaws.com/$IMAGENAME:latest -f $DOCKERFILE --load .
  docker push $ACCOUNTNUM.dkr.ecr.ap-southeast-2.amazonaws.com/$IMAGENAME:latest

else
  echo "building intel - aws profile $AWSPROFILE - dockerfile $DOCKERFILE"
  aws ecr get-login-password --profile $AWSPROFILE | docker login --username AWS --password-stdin $ACCOUNTNUM.dkr.ecr.ap-southeast-2.amazonaws.com
  docker build --no-cache -t $ACCOUNTNUM.dkr.ecr.ap-southeast-2.amazonaws.com/$IMAGENAME:latest -f $DOCKERFILE .
  docker push $ACCOUNTNUM.dkr.ecr.ap-southeast-2.amazonaws.com/$IMAGENAME:latest
fi
