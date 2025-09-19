@bot.command(name='fee')
async def calculate_fee(ctx, price):
    try:
        sell_price = float(price)
        
        embed = discord.Embed(
            title="Platform Fee Calculator",
            description=f"Selling price: **${sell_price:.2f}** | Final payouts after all fees below:",
            color=0xFFBB5C  # Orange color
        )
        
        platforms = ['ebay', 'stockx', 'goat', 'mercari', 'amazon_fba', 'amazon_fbm']
        results = []
        
        # Calculate all platforms
        for platform in platforms:
            result = calculator.calculate_fees(platform, sell_price)
            if result:
                results.append(result)
        
        # Sort by best payout for better organization
        results.sort(key=lambda x: x['net_payout'], reverse=True)
        
        # Create 4 quadrants (2x2 grid) with inline=True
        for i, result in enumerate(results):
            fee_breakdown = "\n".join([f"• {fee}: ${amount:.2f}" for fee, amount in result['fees'].items()])
            
            embed.add_field(
                name=f"{result['platform']}: ${result['net_payout']:.2f}",
                value=f"{fee_breakdown}\n**Total Fees: ${result['total_fees']:.2f}**",
                inline=True  # This creates the grid layout
            )
            
            # Add empty field every 2 platforms to force new row
            if i == 1 or i == 3:  # After 2nd and 4th platform
                embed.add_field(name="\u200b", value="\u200b", inline=True)
        
        embed.set_footer(text="Amounts shown are final payouts after all fees | Use $compare [price] for rankings")
        await ctx.send(embed=embed)
        
    except ValueError:
        await ctx.send("Please enter a valid price. Example: `$fee 350`")
    except Exception as e:
        await ctx.send("Error calculating fees. Please try again.")