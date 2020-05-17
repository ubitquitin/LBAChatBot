import discord
from discord.ext.commands import Bot
from discord import Game
import requests
#import text scraping library
import random
import asyncio
import nlp as n
import numpy as np


BOT_PREFIX = ("?", "!")
TOKEN = "NTIxMDY5MzI0NDI2MDE4ODUz.XnbC5g.0Hr98i24IPW0zSPUusLY8ZCsRhc"

client = Bot(command_prefix=BOT_PREFIX)

@client.command(name='8ball',
                description="Randomly samples some responses",
                brief="Answers you.",
                aliases=['eight_ball','eightball'],
                pass_context=True)
async def eight_ball(context):
    possible_response = [
        'No way in hell baka',
        'Who tf are you?',
        'Choice 3'
    ]
    #"context.message.author.mention" to mention user
    await client.say(random.choice(possible_response) + ", " + context.message.author.mention)

@client.command()
async def square(number):
    val = int(number) * int(number)
    await client.say(str(number) + " squared is " + str(val) + ".")

@client.event
async def on_ready():
    await client.change_presence(game=Game(name="with 3D husbandos! owo"))
    print("Logged in as " + client.user.name)

@client.command()
async def bitcoin():
    url = 'https://api.coindesk.com/v1/bpi/currentprice/BTC.json'
    response = requests.get(url)
    value = response.json()['bpi']['USD']['rate']
    await client.say("Bitcoin price is: " + str(value))

# function to chat with bot
@client.command()
async def chat(context):

    def check(author):
        def inner_check(message):
            return message.author == author

        return inner_check

    await client.say("Start talking with the bot!")
    mod = n.nlp()


    while True:
        inp = ''

        #wait for next message as message.
        msg = await client.wait_for('message', check=check(context.author), timeout=30)

        inp = msg.content
        if inp.lower() == "quit":
            break

        inp_pr = np.array([mod.bag_of_words(inp, mod.words)])
        results = mod.model.predict(inp_pr)

        results_index = np.argmax(results)
        tag = mod.labels[results_index]

        for tg in mod.raw_data["intents"]:
            if tg['tag'] == tag:
                responses = tg['responses']

        await client.say(client.get_channel(), "RoBot: " + str(random.choice(responses)))





client.loop.create_task(list_servers())
client.run(TOKEN)