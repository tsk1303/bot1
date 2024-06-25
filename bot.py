import discord
import requests
from discord.ext import commands

# Replace 'your-bot-token' with your bot's token
TOKEN = 'MTI1NTE4NjQ5ODAzOTMyMDU3Ng.GQTXtP.s4UO-wu3OyvqkFmMW6PiI9qo3yWnAAPyijG8H4'

# List of websites to search
websites = [
    'https://fitgirl-repacks.site/?s={}'
    # Add more websites as needed
]

intents = discord.Intents.default()
intents.message_content = True  # Enable the message content intent

bot = commands.Bot(command_prefix='!', intents=intents)

def search_website(query):
    results = []
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    for website in websites:
        search_url = website.format(query)
        
        response = requests.get(search_url, headers=headers)
        
        # Debugging: Print the search URL and response status code
        print(f"Searching {website} for '{query}'")
        print(f"URL: {search_url}")
        print(f"Status Code: {response.status_code}")

        if response.status_code == 200:
            results.append(search_url)
        else:
            results.append(f'Error fetching results from {website}')
    
    return results

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if message.content.startswith('!'):
        query = message.content[1:]  # Remove the '!' from the message content
        results = search_website(query)
        if not results:
            response_message = 'No results found.'
        else:
            response_message = '\n'.join(results)
        
        if not response_message.strip():
            response_message = 'No results found or there was an error fetching the results.'

        await message.channel.send(response_message)

bot.run(TOKEN)
