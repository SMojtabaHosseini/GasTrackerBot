import discord
import os
import requests
import json

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

@client.event
async def on_ready():
  print("I'm Live as {0.user}".format(client))

  
def getEthGas():
  apiKey = os.getenv('ETH_API_KEY')
  response = requests.get("https://api.etherscan.io/api?module=gastracker&action=gasoracle&apikey=" + apiKey)
  json_data = json.loads(response.text)
  print (json_data['result'])
  return json_data['result']

def getPolygonGas():
  apiKey = os.getenv('POLYGON_API_KEY')
  response = requests.get("https://api.polygonscan.com/api?module=gastracker&action=gasoracle&apikey=" + apiKey))
  json_data = json.loads(response.text)
  return json_data['result']

def setResult(result):
  safe = result["SafeGasPrice"]
  propose = result["ProposeGasPrice"]
  fast = result["FastGasPrice"]
  gas = "Safe Gas Price: " + safe + "\nPropose Gas Price: " + propose + "\nFast Gas Price: " + fast
  return gas
                        
                          
@client.event
async def on_message(message):
  if message.author == client.user:
    return
  
  if message.content.lower() == "!gas" or message.content.lower() == "!gas eth":
    result = getEthGas()
    gas = setResult(result)
    await message.channel.send(gas)
    
  if message.content.lower() == "!gas polygon":
    result = getPolygonGas()
    gas = setResult(result)
    await message.channel.send(gas)
    
    
## get the token bot from .env file and put it in the run method.
client.run(os.getenv('BOT_TOKEN'))
