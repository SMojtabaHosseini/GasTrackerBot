import discord
import os
import requests
import json
import time
from keep_alive import keep_alive

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
  return json_data['result']

def getPolygonGas():
  apiKey = os.getenv('POLYGON_API_KEY')
  response = requests.get("https://api.polygonscan.com/api?module=gastracker&action=gasoracle&apikey=" + apiKey)
  json_data = json.loads(response.text)
  return json_data['result']



def embedMaker(result, chain):
  safe = result["SafeGasPrice"]
  propose = result["ProposeGasPrice"]
  fast = result["FastGasPrice"]
  
  description = "\n**:turtle:  |  Slow :**\t"+safe+"\n\n**:person_walking:  |  Avarage:**\t"+propose+"\n\n**:person_running:  |  Fast:**\t"+fast
  
  gas = discord.Embed(title=":fuelpump: {0} Gas Price".format(chain), description=description, color=0x29252b)
  gas.set_footer(text="\npowered by {0}scan".format(chain))
  
  return gas
                        
                          
@client.event
async def on_message(message):
  if message.author == client.user:
    return
  
  if message.content.lower() == "!gas" or message.content.lower() == "!gas eth":
    result = getEthGas()
    gas = embedMaker(result,"Ether")
    await message.reply(embed=gas)
    
  if message.content.lower() == "!gas polygon":
    result = getPolygonGas()
    gas = embedMaker(result, "Polygon")
    await message.reply(embed=gas)
    
    
## get the token bot from .env file and put it in the run method.
keep_alive()
try:
  client.run(os.getenv("BOT_TOKEN"))
except discord.HTTPException as e:
  if e.status == 429:
    print("The Discord servers denied the connection for making too many requests")
    print("\n\n\nBLOCKED BY RATE LIMITS\nRESTARTING NOW\n\n\n")
    os.system("python restarter.py")
    os.system('kill 1')
        #print("Get help from https://stackoverflow.com/questions/66724687/in-discord-py-how-to-solve-the-error-for-toomanyrequests")
  else:
    raise e
