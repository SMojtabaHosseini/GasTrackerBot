import discord
import os
import requests
import json
import time
from replit import db
from keep_alive import keep_alive

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

@client.event
async def on_ready():
  print("I'm Live as {0.user}".format(client))
    
## Just to avoid to reach api limit create a function to send request each 5 seconds. set the time in db to epoch. if the bot is restarted send a request for the first time.
db["time"] = 0

def getEthGas():
  dbTime = db["time"]
  if time.time() - dbTime >= 5:
    apiKey = os.getenv('ETH_API_KEY')
    response = requests.get("https://api.etherscan.io/api?module=gastracker&action=gasoracle&apikey=" + apiKey)
    json_data = json.loads(response.text)
    db["ethResult"] = json_data['result']
    db["time"] = time.time()
    #return data from api response
    return json_data['result']
  else:
    #return data from database
    return db['ethResult']

## Do the same for polygon
def getPolyGas():
  dbTime = db["time"]
  if time.time() - dbTime >= 5:
    apiKey = os.getenv('POLYGON_API_KEY')
    response = requests.get("https://api.polygonscan.com/api?module=gastracker&action=gasoracle&apikey=" + apiKey)
    json_data = json.loads(response.text)
    db["polyResult"] = json_data['result']
    db["time"] = time.time()
    return json_data['result']
  else:
    return db["polyResult"]

def msgMaker(ethGas, polyGas):
  ethSafe = ethGas["SafeGasPrice"]
  ethPropose = ethGas["ProposeGasPrice"]
  ethFast = ethGas["FastGasPrice"]
  
  ethDesc = "> ```Slow:       "+ethSafe+"\n> Avarage:    "+ethPropose+"\n> Fast:       "+ethFast+"```\n"
  polySafe = polyGas["SafeGasPrice"]
  polyPropose = polyGas["ProposeGasPrice"]
  polyFast = polyGas["FastGasPrice"]
  
  polyDesc = "> ```Slow:       "+polySafe+"\n> Avarage:    "+polyPropose+"\n> Fast:       "+polyFast+"```\n"
  
  gas = discord.Embed(title=":fuelpump: Gas Price", color=0x01b04b)
  gas.add_field(name='Ethereum Gas', value=ethDesc, inline=False)
  gas.add_field(name='Polygon Gas', value=polyDesc, inline=False)
  gas.set_footer(text="\npowered by etherscan and polygonscan")
  
  return gas
                        
                          
@client.event
async def on_message(message):
  if message.author == client.user:
    return
  
  if message.content.lower() == "!gas":
    ethGas = getEthGas()
    polyGas =getPolyGas()
    gas = msgMaker(ethGas,polyGas)
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
