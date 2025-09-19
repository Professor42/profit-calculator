@bot.command(name='fee')
async def calculate_fee(ctx, price):
    try:
        sell_price = float(price)
        
        embed = discord.Embed(
            title="Platform Fee Calculator",
            description=f"Selling price: **${sell_price:.2f}** | Final payouts after all fees below:",
            color=0xFFBB5C
        )
        
        platforms = ['ebay', 'mercari', 'amazon_fba', 'amazon_fbm', 'stockx', 'goat']
        
        for i, platform in enumerate(platforms):
            result = calculator.calculate_fees(platform, sell_price)
            
            if result:
                fee_breakdown = "\n".join([f"• {fee}: ${amount:.2f}" for fee, amount in result['fees'].items()])
                
                embed.add_field(
                    name=f"**__{result['platform']}__: ${result['net_payout']:.2f}**",
                    value=f"{fee_breakdown}\n**Total Fees: ${result['total_fees']:.2f}**",
                    inline=True
                )
        
        embed.set_footer(text="Amounts shown are final payouts after all fees | Use $compare [price] for rankings")
        await ctx.send(embed=embed)
        
    except ValueError:
        await ctx.send("Please enter a valid price. Example: `$fee 350`")
    except Exception as e:
        await ctx.send(f"Error calculating fees: {e}")
