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
                'referral_fee': 0.15,        # 15% average
                'fba_fee': 3.50,             # Average FBA fee
                'storage_fee': 2.00,         # Monthly storage
                'shipping': 0.00,            # Amazon handles
                'packaging': 0.00
            },
            'amazon_fbm': {
                'name': 'Amazon FBM',
                'referral_fee': 0.15,        # 15% average
                'shipping': 8.00,            # Self-ship average
                'packaging': 3.00,
                'payment_processing': 0.00    # Included in referral
            }
        }
    
    def calculate_fees(self, platform, sell_price):
        try:
            sell_price = float(sell_price)
            platform_data = self.platforms.get(platform.lower())
            
            if not platform_data:
                return None
            
            fees = {}
            total_fees = 0
            
            if platform == 'ebay':
                ebay_fee = sell_price * platform_data['final_value_fee']
                paypal_fee = (sell_price * platform_data['paypal_fee']) + platform_data['paypal_fixed']
                shipping = platform_data['shipping']
                packaging = platform_data['packaging']
                
                fees = {
                    'eBay Final Value Fee': ebay_fee,
                    'PayPal Fee': paypal_fee,
                    'Shipping': shipping,
                    'Packaging': packaging
                }
                total_fees = ebay_fee + paypal_fee + shipping + packaging
                
            elif platform == 'stockx':
                transaction_fee = sell_price * platform_data['transaction_fee']
                payment_fee = sell_price * platform_data['payment_fee']
                shipping = platform_data['shipping']
                
                fees = {
                    'Transaction Fee (9.5%)': transaction_fee,
                    'Payment Processing (3%)': payment_fee,
                    'Shipping': shipping
                }
                total_fees = transaction_fee + payment_fee + shipping
                
            elif platform == 'goat':
                commission = sell_price * platform_data['commission']
                payment_fee = (sell_price * platform_data['payment_fee']) + platform_data['payment_fixed']
                shipping = platform_data['shipping']
                
                fees = {
                    'Commission (9.5%)': commission,
                    'Payment Fee': payment_fee,
                    'Shipping': shipping
                }
                total_fees = commission + payment_fee + shipping
                
            elif platform == 'mercari':
                selling_fee = sell_price * platform_data['selling_fee']
                payment_fee = (sell_price * platform_data['payment_fee']) + platform_data['payment_fixed']
                shipping = platform_data['shipping']
                packaging = platform_data['packaging']
                
                fees = {
                    'Selling Fee (10%)': selling_fee,
                    'Payment Fee': payment_fee,
                    'Shipping': shipping,
                    'Packaging': packaging
                }
                total_fees = selling_fee + payment_fee + shipping + packaging
                
            elif platform == 'amazon_fba':
                referral_fee = sell_price * platform_data['referral_fee']
                fba_fee = platform_data['fba_fee']
                storage_fee = platform_data['storage_fee']
                
                fees = {
                    'Referral Fee (15%)': referral_fee,
                    'FBA Fulfillment Fee': fba_fee,
                    'Monthly Storage Fee': storage_fee
                }
                total_fees = referral_fee + fba_fee + storage_fee
                
            elif platform == 'amazon_fbm':
                referral_fee = sell_price * platform_data['referral_fee']
                shipping = platform_data['shipping']
                packaging = platform_data['packaging']
                
                fees = {
                    'Referral Fee (15%)': referral_fee,
                    'Shipping Cost': shipping,
                    'Packaging': packaging
                }
                total_fees = referral_fee + shipping + packaging
            
            net_payout = sell_price - total_fees
            
            return {
                'platform': platform_data['name'],
                'sell_price': sell_price,
                'fees': fees,
                'total_fees': total_fees,
                'net_payout': net_payout,
                'payout_percentage': (net_payout / sell_price) * 100
            }
            
        except Exception as e:
            return None

calculator = FeeCalculator()

@bot.event
async def on_ready():
    print(f'{bot.user} is now online!')

@bot.command(name='fee')
async def calculate_fee(ctx, price):
    try:
        sell_price = float(price)
        
        embed = discord.Embed(
            title="Fee Calculator Results",
            description=f"Selling price: **${sell_price:.2f}**",
            color=0x41F3A6
        )
        
        platforms = ['ebay', 'stockx', 'goat', 'mercari', 'amazon_fba', 'amazon_fbm']
        
        for platform in platforms:
            result = calculator.calculate_fees(platform, sell_price)
            
            if result:
                fee_breakdown = "\n".join([f"• {fee}: ${amount:.2f}" for fee, amount in result['fees'].items()])
                
                embed.add_field(
                    name=f"{result['platform']} - **${result['net_payout']:.2f}** ({result['payout_percentage']:.1f}%)",
                    value=f"{fee_breakdown}\n**Total Fees: ${result['total_fees']:.2f}**",
                    inline=False
                )
        
        embed.set_footer(text="Use $compare [price] for side-by-side comparison")
        await ctx.send(embed=embed)
        
    except ValueError:
        await ctx.send("Please enter a valid price. Example: `$fee 350`")
    except Exception as e:
        await ctx.send("Error calculating fees. Please try again.")

@bot.command(name='compare')
async def compare_platforms(ctx, price):
    try:
        sell_price = float(price)
        
        platforms = ['ebay', 'stockx', 'goat', 'mercari', 'amazon_fba', 'amazon_fbm']
        results = []
        
        for platform in platforms:
            result = calculator.calculate_fees(platform, sell_price)
            if result:
                results.append(result)
        
        results.sort(key=lambda x: x['net_payout'], reverse=True)
        
        embed = discord.Embed(
            title="Platform Comparison",
            description=f"Selling **${sell_price:.2f}** - Ranked by best payout",
            color=0x41F3A6
        )
        
        for i, result in enumerate(results, 1):
            if i == 1:
                emoji = "🥇"
            elif i == 2:
                emoji = "🥈"
            elif i == 3:
                emoji = "🥉"
            else:
                emoji = f"{i}."
            
            embed.add_field(
                name=f"{emoji} {result['platform']}",
                value=f"**${result['net_payout']:.2f}** ({result['payout_percentage']:.1f}%)\nFees: ${result['total_fees']:.2f}",
                inline=True
            )
        
        if len(results) > 1:
            best_payout = results[0]['net_payout']
            difference_text = "\n".join([
                f"• {result['platform']}: ${best_payout - result['net_payout']:.2f} less"
                for result in results[1:3]  # Show top 3 differences
            ])
            
            embed.add_field(
                name="Payout Differences from Best",
                value=difference_text,
                inline=False
            )
        
        await ctx.send(embed=embed)
        
    except ValueError:
        await ctx.send("Please enter a valid price. Example: `$compare 350`")
    except Exception as e:
        await ctx.send("Error comparing platforms. Please try again.")

@bot.command(name='profit')
async def calculate_profit(ctx, buy_price, sell_price, platform="ebay"):
    try:
        buy_price = float(buy_price)
        sell_price = float(sell_price)
        
        result = calculator.calculate_fees(platform.lower(), sell_price)
        
        if not result:
            await ctx.send("Invalid platform. Use: ebay, stockx, goat, mercari, amazon_fba, amazon_fbm")
            return
        
        gross_profit = sell_price - buy_price
        net_profit = result['net_payout'] - buy_price
        profit_margin = (net_profit / buy_price) * 100 if buy_price > 0 else 0
        
        embed = discord.Embed(
            title=f"Profit Analysis - {result['platform']}",
            color=0x00ff00 if net_profit > 0 else 0xff0000
        )
        
        embed.add_field(
            name="Investment",
            value=f"**Buy Price:** ${buy_price:.2f}\n**Sell Price:** ${sell_price:.2f}",
            inline=True
        )
        
        embed.add_field(
            name="Returns",
            value=f"**Gross Profit:** ${gross_profit:.2f}\n**Net Profit:** ${net_profit:.2f}",
            inline=True
        )
        
        embed.add_field(
            name="Metrics",
            value=f"**Profit Margin:** {profit_margin:.1f}%\n**Total Fees:** ${result['total_fees']:.2f}",
            inline=True
        )
        
        fee_breakdown = "\n".join([f"• {fee}: ${amount:.2f}" for fee, amount in result['fees'].items()])
        embed.add_field(
            name="Fee Breakdown",
            value=fee_breakdown,
            inline=False
        )
        
        if net_profit > 0:
            embed.add_field(
                name="Assessment",
                value=f"**Profitable deal!** You'll make ${net_profit:.2f} profit ({profit_margin:.1f}% margin)",
                inline=False
            )
        else:
            embed.add_field(
                name="Assessment",
                value=f"**Losing deal.** You'll lose ${abs(net_profit):.2f}",
                inline=False
            )
        
        await ctx.send(embed=embed)
        
    except ValueError:
        await ctx.send("Please enter valid numbers. Example: `$profit 200 350 ebay`")
    except Exception as e:
        await ctx.send("Error calculating profit. Please try again.")

@bot.command(name='help_fees')
async def help_command(ctx):
    embed = discord.Embed(
        title="Fee Calculator Commands",
        description="Calculate selling fees across multiple platforms",
        color=0x0099ff
    )
    
    embed.add_field(
        name="Basic Commands",
        value="""
        `$fee 350` - Calculate fees for all platforms
        `$compare 350` - Compare platforms side-by-side
        `$profit 200 350 ebay` - Calculate profit for specific platform
        """,
        inline=False
    )
    
    embed.add_field(
        name="Supported Platforms",
        value="""
        • **eBay** - 12.95% + PayPal fees + shipping
        • **StockX** - 9.5% + 3% payment + $13.95 shipping
        • **GOAT** - 9.5% + 2.9% payment + $12 shipping  
        • **Mercari** - 10% + 2.9% payment + shipping
        • **Amazon FBA** - 15% referral + $3.50 FBA + storage
        • **Amazon FBM** - 15% referral + self-ship costs
        """,
        inline=False
    )
    
    embed.add_field(
        name="Examples",
        value="""
        `$fee 500` - See what you'd get selling $500 item
        `$compare 750` - Find best platform for $750 sale
        `$profit 300 500 amazon_fba` - Amazon FBA profit analysis
        """,
        inline=False
    )
    
    await ctx.send(embed=embed)

# Run the bot
if __name__ == "__main__":
    TOKEN = os.environ.get('DISCORD_TOKEN')
    bot.run(TOKEN)