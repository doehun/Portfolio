import json
import os
import datetime
from nltk.tokenize import PunktSentenceTokenizer
from nltk.tokenize import WordPunctTokenizer
from data_generator import get_json


class Reaction:

    path = "slack_data/"

    def __init__(self, user, reaction, channel):
        self.user = user
        self.reaction = reaction
        self.count = 0
        self.channel = channel

    def __str__(self):
        return "%s has %s counts" % (self.reaction, self.count)


    def get_json(self):
        global path

        with open(path) as f:
            json_string = f.read()
            parsed_json = json.loads(json_string)
            return parsed_json


    def count_reaction(self):
        global path
        path_to_folder = os.path.join(path, self.channel)

        folders = os.listdir(path)

        for folder in folders:
            if folder == self.channel:
                json = self.get_json(path_to_folder)

                for j in json:
                    if self.user != j['real_name']:
                        continue
                    if 'reactions' in j:
                       for l in j['reactions']:
                           if l['name'] == self.reaction:
                               self.count += 1


        return self.count



if __name__ == "__main__":

    channels = [channel for channel in os.listdir("slack_data/") if not
    (channel.endswith(".json") or channel == ".ipynb_checkpoints" or channel == '.DS_Store')]

    #print channels
    reactions = set()

    sum = 0
    for channel in channels:
        count = Reaction("John Betz", "joy", "general")
        print channel, ": ", count
        sum += count
    print sum
    #print instance.count_reaction()


    """
    tokenizer = WordPunctTokenizer()
    text = "This text contains an awful a lot of smile. smile some more. smile helps."

    tokens = tokenizer.tokenize(text)

    for t in tokens:
        if t == "smile":
            smile.add_count('smile')

    print smile.count




    def count_reaction(self):
        global path

        folder = os.listdir(path)

        for f in folder:
            json = get_json(os.path.join(path,f))

            for j in json:
                if 'reactions' in j:
                   for l in j['reactions']:
                       if l['name'] == self.reaction:
                           self.count += 1



        return self.count
    """