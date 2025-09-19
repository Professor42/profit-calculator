@bot.command(name='fee')
async def calculate_fee(ctx, price):
    try:
        sell_price = float(price)
        
        embed = discord.Embed(
            title="Platform Fee Calculator",
            description=f"Selling price: **${sell_price:.2f}** | Final payouts after all fees below:",
            color=0xFFBB5C
        )
        
        # Define specific order: top row then bottom row
        platform_order = ['ebay', 'mercari', 'amazon_fba', 'amazon_fbm', 'stockx', 'goat']
        
        for i, platform in enumerate(platform_order):
            result = calculator.calculate_fees(platform, sell_price)
            
            if result:
                fee_breakdown = "\n".join([f"• {fee}: ${amount:.2f}" for fee, amount in result['fees'].items()])
                
                embed.add_field(
                    name=f"**__{result['platform']}__: ${result['net_payout']:.2f}**",
                    value=f"{fee_breakdown}\n**Total Fees: ${result['total_fees']:.2f}**",
                    inline=True
                )
                
                # Add empty field after 2nd and 4th platforms to create row breaks
                if i == 1 or i == 3:
                    embed.add_field(name="\u200b", value="\u200b", inline=True)
        
        embed.set_footer(text="Amounts shown are final payouts after all fees | Use $compare [price] for rankings")
        await ctx.send(embed=embed)
        
    except ValueError:
        await ctx.send("Please enter a valid price. Example: `$fee 350`")
    except Exception as e:
        await ctx.send("Error calculating fees. Please try again.")
