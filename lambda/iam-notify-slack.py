import boto3
import json
import sys,os
# from slacker import Slacker

#def send_to_slack(message,attachment,channel,key):
#    status = True
#    print "sending slack message " + message
#    emoji=":closed_lock_with_key:"

#    if not channel.startswith( '#' ):
#        channel = '#' + channel

#    slack = Slacker(key)
#    slack.chat.post_message(
#        channel=channel,
#        text=message,
#        attachments=attachment,
#        as_user="false",
#        username="AWS IAM Notifier",
#        icon_emoji=emoji)

#    return status

def lambda_handler(event, context):
    #print("Received event: " + json.dumps(event, indent=2))
    status = True
    response = None
    post_to_slack = False

    if 'slack_api_token' in os.environ:
        slack_api_token=os.environ['slack_api_token']
    else:
        print("FATAL: No slack api token set in the slack_api_token environment variable")
        status=False

    if 'slack_channel' in os.environ:
        slack_channel=os.environ['slack_channel']
    else:
        print("FATAL: No slack channel set in the slack_channel environment variable")
        status=False

    if status:
        region=event['region']
        event_name=event['detail']['eventName']

        if event_name == "AttachGroupPolicy":
            post_to_slack = True
        elif event_name == "DetachGroupPolicy":
            post_to_slack = True
        elif event_name == "CreatePolicy":
            post_to_slack = True
        elif event_name == "CreatePolicyVersion":
            post_to_slack = True
        elif event_name == "AttachUserPolicy":
            post_to_slack = True
        elif event_name == "DetachUserPolicy":
            post_to_slack = True
        elif event_name == "AttachRolePolicy":
            post_to_slack = True
        elif event_name == "DetachRolePolicy":
            post_to_slack = True
        else:
            print "No support for event " + event_name

        if post_to_slack:
            print "Posting to slack for " + event_name

    return status
