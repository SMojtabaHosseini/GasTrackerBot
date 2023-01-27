import discord, os, requests, json


client = discord.Client()

@client.event
async def on_ready():
  print("I'm Live as {0.user}".format(client))

  
def getGas():
  apiKey = os.getenv('API_KEY')
  response = requests.get("https://api.etherscan.io/api?module=gastracker&action=gasoracle&apikey={0}".format(apiKey))
  json_data = json.loads(response.text)
  return json_data['result']
                        
                          
@client.event
async def on_message(message):
  if message.author == client.user:
    return
  
  if message.content == "!gas":
    result= getGas()
    safe = result["SafeGasPrice"]
    propose = result["ProposeGasPrice"]
    fast = result["FastGasPrice"]
    gas = "Safe Gas Price: " + safe + "\nPropose Gas Price: " + propose + "\nFast Gas Price: " + fast

    await message.channel.send(gas)
    
    
    
## get the token bot from .env file and put it in the run method.
client.run(os.getenv('TOKEN'))
