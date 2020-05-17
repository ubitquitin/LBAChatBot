import discord
from discord.ext import commands
import os
import asyncio
import nlp as n
import numpy as np
import random

token = "YOUR KEY HERE"

#client = commands.Bot(command_prefix='?', description='A bot that greets the user back.')
client = discord.Client()
mod = n.nlp()
context = {}

@client.event
async def on_ready():
    activity = discord.Game(name="with 3D husbandos! owo")
    await client.change_presence(status=discord.Status.idle, activity=activity)
    print("Logged in as " + client.user.name)
    #servers = list(client.guilds)
    #print("Connected on " + str(len(client.guilds)) + " servers:")
    #for x in range(len(servers)):
    #    print(' ' + servers[x-1].name)

@client.event
async def on_message(message):
    if message.channel.name == "bot_commands":
        if not message.author == client.user:
            channel = discord.utils.get(message.guild.channels, id=message.channel.id)
            #await client.say("Start talking with the bot!")

            inp = ''

            if message.author not in context:
                context[message.author] = "" #initialize user in context dictionary with empty context

            inp = message.content
            #if inp.lower() == "quit":
            #    break

            inp_pr = np.array([mod.bag_of_words(inp, mod.words)])

            #for LSTM/CNN ONLY
            #inp_pr = inp_pr.reshape(inp_pr.shape[0], inp_pr.shape[1], 1)

            results = mod.model.predict(inp_pr)[0]

            #unvalidated = True

            #while unvalidated:
            results_index = np.argmax(results)
            tag = mod.labels[results_index]
                # assumes no duplicate tag names, should only enter if/else below once.
                #for tg in mod.raw_data["intents"]:
                    #if tg['tag'] == tag:
                        #if tg['context_filter'] == context[message.author]:
                        #    unvalidated = False
                        #else:
                        #    results[results_index] = 0 #zero out potentially high prob. class with inappropriate context filter

            if results[results_index] > 0.5:           #HARDCODED UNCERTAINTY THRESHOLD
                for tg in mod.raw_data["intents"]:
                    if tg['tag'] == tag:               #assumes no duplicate tag names.
                        if tg['tag'] == 'prices':      #HARDCODED Context for prices atm
                            if context[message.author] == 'normal_mode':
                                responses = tg['responses_nm']
                            elif context[message.author] == 'trim_req':
                                responses = tg['responses_trim']
                            elif context[message.author] == 'bxp':
                                responses = tg['responses_bxp']
                            elif context[message.author] == 'king':
                                responses = tg['responses_king']
                            else:
                                responses = tg['responses']
                        else:
                            responses = tg['responses']
                        context[message.author] = tg['context_set'] #might have to change to append for multiple contexts

                await channel.send(str(random.choice(responses))) #+ '\n' + str(results) + '\n' + str(message.author) + ': ' + str(context[message.author]))

            else:
                await channel.send("I didn't understand that, please try again!") #+ '\n' + str(results))



client.run(token)