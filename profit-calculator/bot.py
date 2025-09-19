@bot.command(name='fee')
async def calculate_fee(ctx, price):
    try:
        sell_price = float(price)
        
        embed = discord.Embed(
            title="Platform Fee Calculator",
            description=f"Selling price: **${sell_price:.2f}** | Final payouts after all fees below:",
            color=0xFFBB5C
        )
        
        platforms = ['ebay', 'stockx', 'goat', 'mercari', 'amazon_fba', 'amazon_fbm']
        results = []
        
        for platform in platforms:
            result = calculator.calculate_fees(platform, sell_price)
            if result:
                results.append(result)
        
        # Sort by best payout
        results.sort(key=lambda x: x['net_payout'], reverse=True)
        
        # Reorder to put eBay, Mercari, Amazon FBA, Amazon FBM in top row
        # StockX, GOAT in bottom row
        platform_order = []
        for result in results:
            if result['platform'] in ['eBay', 'Mercari', 'Amazon FBA', 'Amazon FBM']:
                platform_order.append(result)
        
        for result in results:
            if result['platform'] in ['StockX', 'GOAT']:
                platform_order.append(result)
        
        # Add fields in the correct order
        for i, result in enumerate(platform_order):
            fee_breakdown = "\n".join([f"• {fee}: ${amount:.2f}" for fee, amount in result['fees'].items()])
            
            embed.add_field(
                name=f"**__{result['platform']}__: ${result['net_payout']:.2f}**",
                value=f"{fee_breakdown}\n**Total Fees: ${result['total_fees']:.2f}**",
                inline=True
            )
            
            # Add spacing after every 2 fields to create rows
            if i == 1 or i == 3:
                embed.add_field(name="\u200b", value="\u200b", inline=True)
        
        embed.set_footer(text="Amounts shown are final payouts after all fees | Use $compare [price] for rankings")
        await ctx.send(embed=embed)
        
    except ValueError:
        await ctx.send("Please enter a valid price. Example: `$fee 350`")
    except Exception as e:
        await ctx.send("Error calculating fees. Please try again.")
