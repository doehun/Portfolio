import os

from data_generator import data_dictionary_form, data_flat_form, users_db
import pandas as pd
import csv

def csv_writer_individual_files(path):
    """

    :param path: path to channel folders
    :return: writes one csv file for each channel
    """
    newpath = '..data/csv_data'

    if not os.path.exists(newpath):
        os.makedirs(newpath)

    data = data_dictionary_form(path)

    for title, data in data.items():
        data.to_csv(newpath+"/{}.csv".format(title), index = False)

    pass


def csv_writer_one_file(path, users_json_path):
    """

    :param path: path to channel folders
    :param users_json_path: path to users.json file
    :return: one file with all the info in it
    """
    path = "..data/slack_data/"

    c = data_flat_form(path)
    df = pd.DataFrame(c, columns = ['channel', 'datetime', 'id', 'text',
                                    'reactions', 'reaction_counts', 'reaction_total_count', 'reaction_type_count'])

    #user_db = users_db(users_json_path)

    #concat = df.merge(user_db, on = 'id', how = 'left')


    df.to_csv("concatenated.csv", index = False, columns = ['channel', 'datetime', 'id', 'text',
                        'reactions', 'reaction_counts', 'reaction_total_count', 'reaction_type_count'])#,
                                                                 #'user_name']), 'real_name'])




def txt_writer_individual_files():

    """takes from the csv files and writes text portion to txt files"""


    newpath = '..data/txt_data'

    if not os.path.exists(newpath):
        os.makedirs(newpath)

    channels = [channel.replace(".csv", "") for channel in os.listdir("csv_data")]

    for channel in channels:

        text_file = open("txt_data/{}.txt".format(channel), "w")
        with open('csv_data/{}.csv'.format(channel)) as f:
            reader = csv.reader(f)
            next(f) #skip first line, which is header
            for row in reader:
                text_file.write(row[2]+'\n')
        text_file.close()



if __name__ == "__main__":
    path = "..data/slack_data/"
    users_json_path =  "..data/slack_data/users.json"


    #csv_writer_individual_files(path)
    csv_writer_one_file(path, users_json_path)

    #txt_writer_individual_files()