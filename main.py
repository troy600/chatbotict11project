from chatterbot.trainers import ChatterBotCorpusTrainer
from chatterbot import ChatBot
from craiyon import Craiyon, craiyon_utils
import discord
from discord.ext import commands
from io import BytesIO
import base64
import random
import socket
import requests
import asyncio
import os



intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(intents = intents, command_prefix="!")



chatbot = ChatBot('Testing')
'''
trainer = ChatterBotCorpusTrainer(chatbot)

# Train the chatbot based on the english corpus
trainer.train("chatterbot.corpus.english")
'''

import yt_dlp

# Create a yt-dlp instance
ydl_opts = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
}
#ydl = yt_dlp.YoutubeDL(ydl_opts)

'''@bot.command()
async def convert(ctx, url):
    with ydl:
        info = ydl.extract_info(url, download=False)
        url2 = info['formats'][0]['url']
        await ctx.send(f"Converting {url} to MP3... This may take a moment.")
        await ctx.send(url2)
'''

generator = Craiyon() # Initialize Craiyon() class

generator = Craiyon() # Initialize Craiyon() class

# Create command
@bot.command()
async def genimage(ctx, *, prompt: str):
    await ctx.send(f"Generating prompt \"{prompt}\"...")    
    generated_images = await generator.async_generate(prompt) # Generate images
    b64_list = await craiyon_utils.async_encode_base64(generated_images.images) # Download images from https://img.craiyon.com and store them as b64 bytestring object
    
    images1 = []
    for index, image in enumerate(b64_list): # Loop through b64_list, keeping track of the index
        img_bytes = BytesIO(base64.b64decode(image)) # Decode the image and store it as a bytes object
        image = discord.File(img_bytes)
        image.filename = f"result{index}.webp"
        images1.append(image) # Add the image to the images1 list
        
    await ctx.reply(files=images1)

@bot.command()
async def message(ctx, msg):
    if msg == bot.user:
        return
    
    await ctx.send(chatbot.get_response(msg))
   
    if msg == '69':
        response = "nice"
        await ctx.send(response)



@bot.command()
async def ageguess(ctx, age):
    await ctx.send("guessing your age")
    await ctx.send(f"your age is {age}")



@bot.command()
async def binary_to_ip(binary_str):
    try:
        if not all(bit in '01' for bit in binary_str):
            raise ValueError("Invalid binary number")

        binary_str = binary_str.zfill(32)

        segments = [binary_str[i:i+8] for i in range(0, 32, 8)]

        decimal_segments = [str(int(segment, 2)) for segment in segments]

        ip_address = ".".join(decimal_segments)

        return ip_address
    except ValueError as e:
        return str(e)

@bot.command()
async def binarytoip(ctx, bin1, bin2, bin3, bin4):
    try:
        if len(bin1) == len(bin2) == len(bin3) == len(bin4) == 8:
            ip_address = ".".join(str(int(bin_str, 2)) for bin_str in [bin1, bin2, bin3, bin4])
            await ctx.send(f'tsu ip address converted is: {ip_address}')
        else:
            await ctx.send('Invalid binary strings. Each binary string should be 8 characters long.')
    except ValueError:
        await ctx.send('Invalid binary strings. lol.')

@bot.command()
async def iptobinary(ctx, ip_address):
    try:
        socket.inet_pton(socket.AF_INET, ip_address)
        
        binary_ip = ".".join(format(int(octet), "08b") for octet in ip_address.split("."))
        await ctx.send(f'Binary IP Address: {binary_ip}')
    except socket.error:
        await ctx.send("Invalid IP address. are you du..? be specific lol")


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')

@bot.command()
async def ping(ctx, website):
    try:
        response = requests.get(website)
        if response.status_code == 200:
            await ctx.send(f'Ping successful. {website} is online!')
        else:
            await ctx.send(f'Ping failed. {website} returned status code {response.status_code}')
    except Exception as e:
        await ctx.send(f'Ping failed. Error: {str(e)}')

'''@bot.command()
async def ping(ctx, website):
    try:
        response = requests.get(website)
        if response.status_code == 200:
            await ctx.send(f'Ping successful. {website} is online!')
        else:
            await ctx.send(f'Ping failed. {website} returned status code {response.status_code}')
    except Exception as e:
        await ctx.send(f'Ping failed. Error: {str(e)}')
'''

@bot.command()
async def convert(ctx, link):

    await ctx.send(f'Converting {link} to MP3...')

        # Download the YouTube video as MP3
    ydl_opts = {
        'format': '140',
        'extractaudio': True,
        'audioformat': 'mp3',
        'outtmpl': 'downloads/%(title)s.%(ext)s',
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(link, download=False)
        video_url = info['url']
        title = info['title']

        os.makedirs('downloads', exist_ok=True)
        filename = f'downloads/{title}.m4a'
        ydl.download([link])
            
        await ctx.send(f'Uploading {title} as MP3...')
        
        # Send the MP3 file
        await ctx.send(file=discord.File(filename))

        # Delete the downloaded file
        os.remove(filename)
        await ctx.send(f'{title} MP3 file sent and removed from the server.')



bot.run("YourTokenHere")
