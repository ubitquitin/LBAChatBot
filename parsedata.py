import numpy as np
import pandas as pd
import json

df = pd.read_csv('C:/Users/rohan/Downloads/lbadata8000.csv', error_bad_lines=False)

tagged_df = df[~df['tag'].isnull()]
tagged_df = tagged_df[['message', 'tag']]

#create a dataframe for each tag and feed the list of messages into the json
#tags: greeting, goodbye, nm, points, bxp, king, trial, prices, todo
#todo: change to a loop through valuecounts of tagged_df['tag']
greeting_df = tagged_df[tagged_df['tag'] == 'greeting']
greeting_msg_list = list(greeting_df['message'])
print('greeting: ', len(greeting_msg_list))

goodbye_df = tagged_df[tagged_df['tag'] == 'goodbye']
goodbye_msg_list = list(goodbye_df['message'])
print('goodbye: ', len(goodbye_msg_list))

nm_df = tagged_df[tagged_df['tag'] == 'nm']
nm_msg_list = list(nm_df['message'])
print('nm: ', len(nm_msg_list))

points_df = tagged_df[tagged_df['tag'] == 'points']
points_msg_list = list(points_df['message'])
print('points: ', len(points_msg_list))

bxp_df = tagged_df[tagged_df['tag'] == 'bxp']
bxp_msg_list = list(bxp_df['message'])
print('bxp: ', len(bxp_msg_list))

king_df = tagged_df[tagged_df['tag'] == 'king']
king_msg_list = list(king_df['message'])
print('king: ', len(king_msg_list))

trial_df = tagged_df[tagged_df['tag'] == 'trial']
trial_msg_list = list(trial_df['message'])
print('trial: ', len(trial_msg_list))

prices_df = tagged_df[tagged_df['tag'] == 'prices']
prices_msg_list = list(prices_df['message'])
print('prices: ', len(prices_msg_list))

todo_df = tagged_df[tagged_df['tag'] == 'todo']
todo_msg_list = list(todo_df['message'])
print('todo: ', len(todo_msg_list))

with open("intents.json", 'r') as file:
    data = json.load(file)
    intents = data['intents']

    for intent in intents:

        tag = intent['tag']

        if tag == 'greeting':
            intent['patterns'] = greeting_msg_list
        elif tag == 'goodbye':
            intent['patterns'] = goodbye_msg_list
        elif tag == 'nm':
            intent['patterns'] = nm_msg_list
        elif tag == 'points':
            intent['patterns'] = points_msg_list
        elif tag == 'bxp':
            intent['patterns'] = bxp_msg_list
        elif tag == 'king':
            intent['patterns'] = king_msg_list
        elif tag == 'trial':
            intent['patterns'] = trial_msg_list
        elif tag == 'prices':
            intent['patterns'] = prices_msg_list
        elif tag == 'todo':
            intent['patterns'] = todo_msg_list

    with open("intents.json", 'w') as fw:
        json.dump(data, fw)