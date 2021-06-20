import requests
from bs4 import BeautifulSoup
import csv
import pandas as pd
import time
from discord.ext import commands

class creds:
    bot_token="Nzg4MTE5OTQwMTUwMzI5MzQ1.X9e35A.8w5dzhLUCwtiMir5kOE5Iq43qjA"            # Discord bot token
    voice_channel_id=42       # The channel you want the bot to play music in (DO NOT USE STrING!)
    text_channel_id=344093490038439936      # The channel you want the bot to write the song name in (can't be a voice channel) (DO NOT USE STING!)





def rs(link):
    token = creds.bot_token
    client = commands.Bot(command_prefix='.')
    print(creds.text_channel_id)

    @client.event
    async def on_ready():
        await client.get_channel(creds.text_channel_id).send(link)


    @client.event
    async def on_message(message):
        if message.content == "!leave":
            await message.channel.send("Leaving")
            for vc in client.voice_clients:
                if vc.guild == message.guild:
                    await vc.disconnect()
    client.run(token)


def rs3_scrape():
    page = requests.get("https://www.runescape.com/community")
    soup = BeautifulSoup(page.content, 'html.parser')
    all_news = soup.find(id="newsSection")
    news = all_news.findAll("div", {"class": "copy"})

    df = pd.read_csv("newsrs3.csv")
    for x in news:
        print(x.find('a')['href'])
        if x.find('a')['href'] not in df["url"].values:
            print("not in df")
            with open('newsrs3.csv','a',newline='\n')as f:
                thewriter = csv.writer(f)
                thewriter.writerow([x.find('a')['href']])
                rs(x.find('a')['href'])

def osrs_scrape():
    page = requests.get("https://oldschool.runescape.com/home")
    soup = BeautifulSoup(page.content, 'html.parser')
    news = soup.find_all("article")

    df = pd.read_csv("newsosrs.csv")
    print(df)
    for x in news:
        print(x.find('a')['href'])
        if x.find('a')['href'] not in df["url"].values:
            print("not in df")
            with open('newsosrs.csv','a',newline='\n')as f:
                thewriter = csv.writer(f)
                thewriter.writerow([x.find('a')['href']])
                rs(x.find('a')['href'])

while True:
    rs3_scrape()
    osrs_scrape()
    time.sleep(20)