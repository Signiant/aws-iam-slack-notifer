# aws-iam-policy-slack-notifer
Notifies slack when an IAM policy is created, changed or assigned to a role

[![Build Status](https://travis-ci.org/Signiant/aws-iam-slack-notifer.svg?branch=master)](https://travis-ci.org/Signiant/aws-iam-slack-notifer)

# Purpose
Notifies a slack channel when an AWS IAM policy is manipulated

# Sample Output

![Sample Slack Posts](https://raw.githubusercontent.com/Signiant/aws-iam-slack-notifier/master/images/slack-sample.jpg)

# Installing and Configuring

## Slack Setup
Before installing anything to AWS, you will need to configure a "bot" in Slack to handle the posts for you.  To do this:
* In Slack, choose _Manage Apps_ -> _Custom Integrations_ -> _Bots_
  * Add a new bot configuration
  * username: aws-iam-notifier
  * Copy the API Token.
  * Don't worry about other parameters - the notifier over-rides them anyway

## AWS Setup
* Grab the latest Lambda function zip from [Releases](https://github.com/Signiant/aws-iam-slack-notifer/releases)
* Create a new cloudformation stack using the template in the cfn folder

The stack asks for the function zip file location in S3, the slack API Key and the slack channel to post notifications to. Once the stack is created, a cloudwatch event is created to subscribe the lambda function to several IAM events around policy manipulation.
