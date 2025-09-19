import discord
from discord.ext import commands
import os

# Bot setup
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='$', intents=intents)

class FeeCalculator:
    def __init__(self):
        self.platforms = {
            'ebay': {
                'name': 'eBay',
                'final_value_fee': 0.1295,
                'paypal_fee': 0.0349,
                'paypal_fixed': 0.49,
                'shipping': 15.00,
                'packaging': 2.00
            },
            'stockx': {
                'name': 'StockX',
                'transaction_fee': 0.095,
                'payment_fee': 0.03,
                'shipping': 13.95,
                'packaging': 0.00
            },
            'goat': {
                'name': 'GOAT',
                'commission': 0.095,
                'payment_fee': 0.029,
                'payment_fixed': 0.30,
                'shipping': 12.00,
                'packaging': 0.00
            },
            'mercari': {
                'name': 'Mercari',
                'selling_fee': 0.10,
                'payment_fee': 0.029,
                'payment_fixed': 0.30,
                'shipping': 11.50,
                'packaging': 2.00
            },
            'amazon_fba': {
                'name': 'Amazon FBA',
