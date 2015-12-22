Title: Create an IAM user for ElasticBeanstalk
Date: 2015-05-11
Tags: aws
Category: Web


To use AWS [ElasticBeanstalk](http://docs.aws.amazon.com/elasticbeanstalk),
we have to create a [IAM](http://aws.amazon.com/iam/) user first.

- After logging in AWS, go to `IAM` under `Services`.

- Click `Create New Group` under `Groups` and specify a group name (here, assumed as `ElasticBeanstalkFullAccess`).

- Attach policy `AWSElasticBeanstalkFullAccess` to the group `ElasticBeanstalkFullAccess`.

- Click `Create New Users` under `Users` to create a new user supposed to use ElasticBeanstalk. During the process, it will prompt you to download security credentials composed by `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY`.

- Under `Users`, add the user to the group `ElasticBeanstalkFullAccess`.

From now on, you should be able to use ElasticBeanstalk with the security credentials downloaded.
