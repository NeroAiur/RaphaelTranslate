import discord
from json import load
from random import randint
from src import gemini

with open("assets/config.json", "r") as cnf_file:
    config = load(cnf_file)
    
with open("assets//text_template.txt", "r", encoding="windows-1252") as tmpl_file:
    text_template = tmpl_file.read()
    
intents = discord.Intents.default()
intents.message_content = True
intents.guild_messages = True
intents.guilds = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f"{client.user} is now online!")

@client.event
async def on_raw_reaction_add(payload):
    try:
        message = await client.get_channel(payload.channel_id).fetch_message(payload.message_id)
        emoji = payload.emoji.name
        user = payload.member
        channel = payload.channel_id
        
        if str(user) != "hdgames" and message.author.id == config["TARGET_UID"] and emoji == "❓":
            
            api_request = text_template.format(discord_message=message.content)
            response = gemini.generate_text_response(api_request, config["API_KEY"])
            
            response_array = response.splitlines()
            bot_messages = []
            for text in response_array:
                split_text = text.split(": ")
                actual = split_text[1]
                bot_messages.append(actual)
            
            coefficient = randint(1, 100)
            if coefficient <= 5:
                bot_response = bot_messages[1]
            elif coefficient >= 95:
                bot_response = bot_messages[2]
            else:
                bot_response = bot_messages[0]
            
            await message.channel.send("Originale Nachricht: \"" + message.content + "\"\n\nÜbersetzung: \"" + bot_response + "\"")
    except ValueError:
        print("ValueError - wahrscheinlich hat es Gemini abgefangen.")
        await channel.send("BEEP BOOP FEHLER FEHLER - SATZ ZU VERWIRREND - FEHLERCODE 1")
    except IndexError:
        print("IndexError - überprüfen und für die Zukunft fixen.")
        print(response)
        await channel.send("BEEP BOOP FEHLER FEHLER - SATZ ZU VERWIRREND - FEHLERCODE 2")
        
        
client.run(config["BOT_TOKEN"])