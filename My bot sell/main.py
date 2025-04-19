import os
import discord
from discord.ext import commands
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

# Bot setup with required intents
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)

# Store items for sale
items_for_sale = {}

class Item:
    def __init__(self, name, price, description, image_url):
        self.name = name
        self.price = price
        self.description = description
        self.image_url = image_url

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')

@bot.command(name='add_item')
@commands.has_permissions(administrator=True)
async def add_item(ctx, name: str, price: float, description: str, image_url: str = None):
    """Add an item to the store (Admin only)"""
    items_for_sale[name] = Item(name, price, description, image_url)
    
    embed = discord.Embed(
        title="✅ Item Added Successfully",
        color=discord.Color.green()
    )
    embed.add_field(name="Name", value=name, inline=False)
    embed.add_field(name="Price", value=f"${price:.2f}", inline=True)
    embed.add_field(name="Description", value=description, inline=False)
    
    if image_url:
        embed.set_image(url=image_url)
    
    await ctx.send(embed=embed)

@bot.command(name='list_items')
async def list_items(ctx):
    """List all items available for sale"""
    if not items_for_sale: