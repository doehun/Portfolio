import pandas as pd
import json
import os
from datetime import datetime


def get_json(path):

    """
    Helper function to get parsed json data

    :param path: the path where all channel folders are. Define in main
    :return: parsed json data
    """
    with open(path) as f:
        json_string = f.read()
        parsed_json = json.loads(json_string)
        return parsed_json


def get_channel_data(path, channel):
    """
    Passing channel name in parenthesis in argument creates a list of lists
    where each list is data about a single message :
    [time, user, text, reaction]

    Ex) get_channel_data("hoops")
    """

    full = []
    path = os.path.join(path, str(channel)) # get_channel( path = "slack_data/" , channel = "blue")
    folder = os.listdir(path)

    for f in folder:
        json = get_json(os.path.join(path,f))

        for j in json:
            l = []


            #skip lines with no 'text' or 'user'
            if 'subtype' in j:
                if (j['subtype'] == 'channel_leave') or (j['subtype'] == 'channel_join') \
                    or (j['subtype'] == 'file_share') or (j['subtype'] == 'channel_purpose'):

                    continue
            if not 'user' in j:
                continue


            time = datetime.fromtimestamp(float(j['ts']))
            l.append(str(channel))
            l.append(time)
            l.append(j['user'].encode('utf-8'))
            l.append(j['text'].encode('utf-8'))

            # Get reactions
            reactions = []
            reaction_counts = []
            reaction_count = 0
            reaction_type_count = 0

            if 'reactions'  in j:
                for reaction in j['reactions']:
                    reactions.append(reaction['name'])
                    reaction_counts.append(reaction['count'])
                    reaction_count += reaction['count']
                    reaction_type_count += 1

                l.append(reactions)
                l.append(reaction_counts)
                l.append(int(reaction_count))
                l.append(int(reaction_type_count))

                #reaction.extend(j['reactions'])

            full.append(l)
    return full


def users_db(users_json_path):
    """
    Creates Dataframe from users.json

    :param user_json_path: The path to where users.json is
    :return: Dataframe with "id" "name" "real_name"
    """
    users = get_json(users_json_path)

    id_list = []
    username = []
    real_name = []


    for user in users:
        id_list.append(user["id"])
        username.append(user["name"])
        real_name.append(user["real_name"])

    df = pd.DataFrame(zip(id_list, username, real_name), columns= ["id", "user_name", "real_name"])
    return df

def channels_db(channels_json_path):
    """
    Creates DataFrame from channels.json

    :param path: path to where channels.json is
    :return: DataFrame with "channel" "creator" "members"
    """
    channels = get_json(channels_json_path)

    channel_list = []
    creator_list = []
    members_list = []

    for channel in channels :
        channel_list.append(channel['name'])
        creator_list.append(channel['creator'])
        members_list.append(channel['members'])

    df = pd.DataFrame(zip(channel_list, creator_list, members_list),
                      columns= ["channel", "creator", "members"])

    return df


def data_dictionary_form(path):
    """
    Combines user_db with data

    :param path: path to channel folders. Defaulted to "slack_data" if no input
    :return: dictionary of DataFrames
    """
    users_json_path =  path + "users.json"
    users = users_db(users_json_path)

    channels = [channel for channel in os.listdir(path) if not
    (channel.endswith(".json") or channel == ".ipynb_checkpoints" or channel == '.DS_Store')]

    names = ['channel', 'datetime', 'id', 'text', 'reactions', 'reaction_counts', 'reaction_total_count',
             'reaction_type_count']

    data = {}

    #create a dictionary of dataframes, where each dataframe is texts of
    for channel in channels:
        c = pd.DataFrame(get_channel_data(path, channel), columns = names)
        d = c.merge(users, on = 'id', how = 'left')

        data[channel] = d



    return data


def data_flat_form(path):
    channels = [channel for channel in os.listdir(path) if not
    (channel.endswith(".json") or channel == ".ipynb_checkpoints" or channel == '.DS_Store')]

    full = []
    for channel in channels:
        full.extend(get_channel_data(path, channel))

    return full


