# aws-iam-policy-slack-notifer
Notifies slack when an IAM policy is created, changed or assigned to a role

[![Build Status](https://travis-ci.org/Signiant/aws-iam-slack-notifer.svg?branch=master)](https://travis-ci.org/Signiant/aws-iam-slack-notifer)

# Purpose
Notifies a slack channel when an AWS IAM policy is manipulated

# Sample Output

![Sample Slack Posts](https://raw.githubusercontent.com/Signiant/aws-iam-slack-notifer/master/images/slack-sample.jpg)

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

## Filtering Slack Alerts

Using some optional environment variables defined on the Lambda function, you can also exclude certain Slack notifications for specific policy manipultation events.  Set the following variables on the function to `0` if you wish to exclude these events from notifying Slack:

* CREATE_POLICY_NOTIFY
* CREATE_POLICY_VERSION_NOTIFY
* ATTACH_GROUP_POLICY_NOTIFY  /  DETACH_GROUP_POLICY_NOTIFY
* ATTACH_USER_POLICY_NOTIFY  / DETACH_USER_POLICY_NOTIFY
* ATTACH_ROLE_POLICY_NOTIFY  /  DETACH_ROLE_POLICY_NOTIFY

## Slacker Updates Needed

In order for this to work with new bot tokens, changes need to be made to Slacker.__init__.py 
I've added the new __init.py__ file with deprecated parameters removed and support for the Authorization token being sent in the header vs param. 
(Authorization changes simply include changing line 69 (of the latest version) to change from `kwargs.setdefault('params', {})['token'] = self.token` to `kwargs.setdefault('headers', {})['Authorization'] = "Bearer " + self.token`
