import discord, os, requests, json


client = discord.Client()

@client.event
async def on_ready():
  print("I'm Live as {0.user}".format(client))
  
def getGas():
  apiKey = os.getenv('ApiKey')
  response = requests.get("https://api.etherscan.io/api
                          ?module=gastracker
                          &action=gasoracle
                          &apikey={0}".format(apiKey))
  return response
                        
                          
@client.event
async def on_message(message):
  if message.author == client.user:
    return
  
  if message.content == "!gas":
    gas = getGas()
    json_data = json.load(gas
    
    
////get the token bot from .env file and put it in the run method.
client.run(os.getenv('TOKEN'))
