import pandas as pd
import json
import os
from datetime import datetime


def get_json(json_path):

    """
    Helper function to get parsed json data

    :param path: the path where all channel folders are. Define in main
    :return: parsed json data
    """
    with open(json_path) as f:
        data = json.load(f)
        return data

def get_dataframe(folder_path):
    """
    Passing path to data crawled as argument creates a list of lists
    that is later written into a dataframe.
    Each list is data about a single message :
    [time, user, text, reaction]

    :param folder_path: path to the crawled Slack data
    :return:
    """
    full = []
    for file in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file)
        json = get_json(file_path)['messages']
        for j in json:
            l = []
            if 'subtype' in j:
                continue

            time = datetime.fromtimestamp(float(j['ts']))
            l.append(file.replace('.json', ''))
            l.append(time)
            l.append(j['user'].encode('utf-8'))
            l.append(j['text'].encode('utf-8'))

            # Get reactions
            reactions = None
            reaction_counts_by_type = None
            reaction_total_count = 0
            reaction_type_count = 0

            if 'reactions' in j:
                reactions = []
                reaction_counts_by_type = []

                for reaction in j['reactions']:
                    reactions.append(reaction['name'])
                    reaction_counts_by_type.append(reaction['count'])
                    reaction_total_count += reaction['count']
                    reaction_type_count += 1

                l.append(reactions)
                l.append(reaction_counts_by_type)
                l.append(int(reaction_total_count))
                l.append(int(reaction_type_count))

                #reaction.extend(j['reactions'])
            else:
                l.append(reactions)
                l.append(reaction_counts_by_type)
                l.append(reaction_total_count)
                l.append(reaction_type_count)

            full.append(l)

            columns = ['channel', 'datetime', 'user_id', 'text', 'reactions', 'reaction_counts',
                      'reaction_total_count', 'reaction_type_count']
            df = pd.DataFrame(full, columns = columns)
    return df

def main():
    full = get_dataframe('/Users/doehun/Desktop/channels')
    full.to_csv("concatenated.csv")

if __name__ == '__main__':
    main()