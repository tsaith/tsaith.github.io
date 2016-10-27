Title: Set up a postgres-backed rails app with ElasticBeanstalk
Date: 2015-05-11
Tags: rails
Category: Web

This article will describe the way I set up a Rails app with ElasticBeanstalk and PostgresSQL.
Here Rails 4.1 based on [Puma](https://github.com/puma/puma) 2.10.2 and [Nginx](http://nginx.org/) 1.6.2 is demonstrated.

### Install ElasticBeanstalk CLI

AWS provides both [Management Console](http://docs.aws.amazon.com/elasticbeanstalk/latest/dg/GettingStarted.UsingAEB.html#GettingStarted.UsingAEB.console) and [EB CLI](http://docs.aws.amazon.com/elasticbeanstalk/latest/dg/command-reference-get-started.html) to work with ElasticBeanstalk.

The CLI requires python and is easier to perform some features of ElasticBeanstalk.

```
pip install awsebcli
```

### Create an IAM user

ElasticBeanstalk will require an IAM user to create app environment.
In case you have no idea how to create an IAM user,
please view this [post](create-an-iam-user-for-elasticbeanstalk.markdown).

### Initialize a git repository

Here `agileorder` is the name of my app.

```
$ cd agileorder
$ git init
$ git add -A
$ git commit -m "Initial commit"
```

### Initialize EB environment

```
$ eb init

Select a default region
1) us-east-1 : US East (N. Virginia)
2) us-west-1 : US West (N. California)
3) us-west-2 : US West (Oregon)
4) eu-west-1 : EU (Ireland)
5) eu-central-1 : EU (Frankfurt)
6) ap-southeast-1 : Asia Pacific (Singapore)
7) ap-southeast-2 : Asia Pacific (Sydney)
8) ap-northeast-1 : Asia Pacific (Tokyo)
9) sa-east-1 : South America (Sao Paulo)
(default is 3): 8

Select an application to use
1) [ Create new Application ]
(default is 1): 1

Enter Application Name: agileorder

It appears you are using Ruby. Is this correct?
(y/n): y

Select a platform version.
1) Ruby 2.2 (Puma)
2) Ruby 2.1 (Puma)
3) Ruby 2.0 (Puma)
4) Ruby 2.2 (Passenger Standalone)
5) Ruby 2.1 (Passenger Standalone)
6) Ruby 2.0 (Passenger Standalone)
7) Ruby 1.9.3
(default is 1): 2
Do you want to set up SSH for your instances?
(y/n): n
```

Please note that `eb init` will add `.elasticbeanstalk` to the `.gitignore`.
Be sure to commit `.gitignore` once again.
```
$ git add .gitignore
$ git commit -m "Update .gitignore"
```

# Configure EB to install postgresql-devel

Under project directory, create `.ebextensions/packages.config` with following content.

{% codeblock .ebextensions/packages.config lang:yaml %}
packages:
  yum:
    postgresql93-devel: []
{% endcodeblock %}

Then add the `.ebextensions` to repository

```
git add .ebextensions
git commit -m "Add .ebextensions"
```

### Create environment

```
$ eb create agileorder-env
```

After waiting for a while, the last part of output messages are shown as

```
INFO: Application available at agileorder-env-jmcrf7dbdr.elasticbeanstalk.com.
ERROR: Create environment operation is complete, but with errors. For more information, see troubleshooting documentation.
INFO: Adding instance 'i-72db7287' to your environment.
```

After checking logs, I figured out the errors come from the missing environment variables used in my app.

### Set up environment variables

Under `Software Configuration` of `Elastic Beanstalk` of `AWS Management Console`,
add essential environments used in app like `SECRET_KEY_BASE`, `SENTRY_DSN`, ...etc.

### Create a RDS instance

Under `Data Tier` of `Elastic Beanstalk` of `AWS Management Console`,
create a new [RDS](http://aws.amazon.com/rds/) database and set the DB engine to `postgres`.

{% img https://c1.staticflickr.com/9/8693/17514909495_6704f394e1_b.jpg %}

After setting `Master Username` and `Master Password`, then click `Save`, environment variables will have been added to EB environment automatically.

### Configure database.yml to work with RDS instance

Under project directory, modify the `database.yml` as

config/database.yml:

    :::yaml
    ... skip the parts of development and test modes ...

    production:
      adapter: postgresql
      encoding: unicode
      database: <%= ENV['RDS_DB_NAME'] %>
      username: <%= ENV['RDS_USERNAME'] %>
      password: <%= ENV['RDS_PASSWORD'] %>
      host: <%= ENV['RDS_HOSTNAME'] %>
      port: <%= ENV['RDS_PORT'] %>

Commit the `database.yml` to repository

```
git add -A
git commit -m "Update database.yml"
```

Finally, deploy the app to AWS.
```
eb deploy
```

To open the app URL in a browser, simply execute
```
eb open
```
