import json
import os
from slacker import Slacker


# Default return for not found or fail to parse is True
# Explicitly setting to 0/False will return a False
def env_var_to_bool(env_var):
    try:
        return int(os.environ.get(env_var, '1'))
    except BaseException:
        return True


def send_to_slack(message, attachment, channel, key):
    status = True
    print("sending slack message " + message)
    emoji = ":closed_lock_with_key:"

    if not channel.startswith('#'):
        channel = '#' + channel

    slack = Slacker(key)
    slack.chat.post_message(
        channel=channel,
        text=message,
        attachments=attachment,
        as_user="false",
        username="AWS IAM Notifier",
        icon_emoji=emoji)

    return status


def lambda_handler(event, context):
    status = True
    policy_name = None
    policy_arn = None
    object_field_name = None
    object_field_value = None
    post_to_slack = False

    if 'slack_api_token' in os.environ:
        slack_api_token = os.environ['slack_api_token']
    else:
        print("FATAL: No slack api token set in the slack_api_token environment variable")
        status = False

    if 'slack_channel' in os.environ:
        slack_channel = os.environ['slack_channel']
    else:
        print("FATAL: No slack channel set in the slack_channel environment variable")
        status = False

    if status:
        region = event['region']
        event_name = event['detail']['eventName']

        if event_name == "CreatePolicy":
            if env_var_to_bool('CREATE_POLICY_NOTIFY'):
                post_to_slack = True
                object_field_name = ""
                object_field_value = ""
                policy_name = event['detail']['requestParameters']['policyName']
                policy_arn = event['detail']['responseElements']['policy']['arn']
            else:
                print('{} environment variable evaluated as False, not notifying slack'.format('CREATE_POLICY_NOTIFY'))
        elif event_name == "CreatePolicyVersion":
            if env_var_to_bool('CREATE_POLICY_VERSION_NOTIFY'):
                post_to_slack = True
                object_field_name = ""
                object_field_value = ""
                policy_name = event['detail']['requestParameters']['policyArn'].split(':')[5]
                policy_arn = event['detail']['requestParameters']['policyArn']
            else:
                print('{} environment variable evaluated as False, not notifying slack'.format('CREATE_POLICY_VERSION_NOTIFY'))
        elif event_name == "AttachGroupPolicy" or event_name == "DetachGroupPolicy":
            if env_var_to_bool('ATTACH_GROUP_POLICY_NOTIFY') and env_var_to_bool('DETACH_GROUP_POLICY_NOTIFY'):
                post_to_slack = True
                object_field_name = "Group"
                object_field_value = event['detail']['requestParameters']['groupName']
                policy_name = event['detail']['requestParameters']['policyArn'].split(':')[5]
                policy_arn = event['detail']['requestParameters']['policyArn']
            else:
                print('{}, {} environment variables evaluated as False, not notifying slack'.format('ATTACH_GROUP_POLICY_NOTIFY', 'DETACH_GROUP_POLICY_NOTIFY'))
        elif event_name == "AttachUserPolicy" or event_name == "DetachUserPolicy":
            if env_var_to_bool('ATTACH_USER_POLICY_NOTIFY') and env_var_to_bool('DETACH_USER_POLICY_NOTIFY'):
                post_to_slack = True
                object_field_name = "User"
                object_field_value = event['detail']['requestParameters']['userName']
                policy_name = event['detail']['requestParameters']['policyArn'].split(':')[5]
                policy_arn = event['detail']['requestParameters']['policyArn']
            else:
                print('{}, {} environment variables evaluated as False, not notifying slack'.format('ATTACH_USER_POLICY_NOTIFY', 'DETACH_USER_POLICY_NOTIFY'))
        elif event_name == "AttachRolePolicy" or event_name == "DetachRolePolicy":
            if env_var_to_bool('ATTACH_ROLE_POLICY_NOTIFY') and env_var_to_bool('DETACH_ROLE_POLICY_NOTIFY'):
                post_to_slack = True
                object_field_name = "Role"
                object_field_value = event['detail']['requestParameters']['roleName']
                policy_name = event['detail']['requestParameters']['policyArn'].split(':')[5]
                policy_arn = event['detail']['requestParameters']['policyArn']
            else:
                print('{}, {} environment variables evaluated as False, not notifying slack'.format('ATTACH_ROLE_POLICY_NOTIFY', 'DETACH_ROLE_POLICY_NOTIFY'))
        else:
            print("No support for event " + event_name)
            print("Received event: " + json.dumps(event, indent=2))

        if post_to_slack:
            print("Posting to slack for " + event_name)
            print("object_field_name " + object_field_name)
            print("object_field_value " + object_field_value)
            print("policy_name " + policy_name)
            print("policy_arn " + policy_arn)

            # Get the user or role who made this change
            if 'userName' in event['detail']['userIdentity']:
                operation_user = event['detail']['userIdentity']['userName']
            else:
                # no user so must be a role
                operation_user = event['detail']['userIdentity']['principalId'].split(':')[1]
                operation_role = event['detail']['userIdentity']['sessionContext']['sessionIssuer']['userName']

                operation_user = operation_user + \
                    " (assuming role: " + operation_role + ")"

            print("user changing policy is " + operation_user)

            iam_policy_console_link = "https://console.aws.amazon.com/iam/home?region=" + region + "#/policies/" + policy_arn + "$jsonEditor"

            slack_message = "IAM policy `" + policy_name + "` has been manipulated by _" + operation_user + "_ in " + region
            slack_attachment = [
                {
                    "fallback": "Check the IAM console for details.",
                    "color": "#36a64f",
                    "title": "View Policy Details in the AWS Console",
                    "title_link": iam_policy_console_link,
                    "fields": [
                        {
                            "title": "Action Performed",
                            "value": event_name,
                            "short": 'false'
                        },
                        {
                            "title": object_field_name,
                            "value": object_field_value,
                            "short": 'false'
                        }
                    ]
                }
            ]

            status = send_to_slack(
                slack_message,
                slack_attachment,
                slack_channel,
                slack_api_token)

    return status
