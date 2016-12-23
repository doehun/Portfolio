import os
from slacker import Slacker
import json

def mkdir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

def get_history(pageableObject, channelId, pageSize = 100):

    messages = []
    lastTimestamp = None

    while(True):
        response = pageableObject.history(
            channel = channelId,
            latest  = lastTimestamp,
            oldest  = 0,
            count   = pageSize
        ).body

        messages.extend(response['messages'])

        if (response['has_more'] == True):
            lastTimestamp = messages[-1]['ts'] # -1 means last element in a list
        else:
            break
    return messages


def get_channels(slack):

    channels = slack.channels.list().body['channels']

    print("\nchannels: ")
    for channel in channels:
        print(channel['name'])

        parentDir = "channels"
        mkdir(parentDir)

        for channel in channels:
            print("getting history for channel {0}".format(channel['name']))
            fileName = "{parent}/{file}.json".format(parent = parentDir, file = channel['name'])
            messages = get_history(slack.channels, channel['id'])
            channelInfo = slack.channels.info(channel['id']).body['channel']
            with open(fileName, 'w') as outFile:
                print("writing {0} records to {1}".format(len(messages), fileName))
                json.dump({'channel_info': channelInfo, 'messages': messages }, outFile, indent=4)

def main():
    api_token = 'HERE-GOES-YOUR-API-KEY'

    slack = Slacker(api_token)

    get_channels(slack)

if __name__ == '__main__':
    main()
