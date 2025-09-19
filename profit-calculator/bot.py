@bot.command(name='fee')
async def calculate_fee(ctx, price):
    try:
        sell_price = float(price)
        
        # Create two-column layout with fee breakdowns
        output = f"**Fee Calculator**\n${sell_price:.0f} After fees:\n\n"
        
        platforms = ['ebay', 'mercari', 'amazon_fba', 'stockx', 'goat', 'amazon_fbm']
        
        # Process platforms in pairs for two columns
        for i in range(0, len(platforms), 2):
            left_platform = platforms[i]
            right_platform = platforms[i + 1] if i + 1 < len(platforms) else None
            
            # Left column
            left_result = calculator.calculate_fees(left_platform, sell_price)
            if left_result:
                fee_breakdown = []
                for fee_name, fee_amount in left_result['fees'].items():
                    fee_breakdown.append(f"• {fee_name}: ${fee_amount:.2f}")
                
                left_text = f"**{left_result['platform']}** (${left_result['total_fees']:.2f})\n"
                left_text += f"${left_result['net_payout']:.2f}\n"
                left_text += "\n".join(fee_breakdown)
            
            # Right column
            right_text = ""
            if right_platform:
                right_result = calculator.calculate_fees(right_platform, sell_price)
                if right_result:
                    fee_breakdown = []
                    for fee_name, fee_amount in right_result['fees'].items():
                        fee_breakdown.append(f"• {fee_name}: ${fee_amount:.2f}")
                    
                    right_text = f"**{right_result['platform']}** (${right_result['total_fees']:.2f})\n"
                    right_text += f"${right_result['net_payout']:.2f}\n"
                    right_text += "\n".join(fee_breakdown)
            
            # Combine columns with spacing
            if right_text:
                # Split into lines and combine side by side
                left_lines = left_text.split('\n')
                right_lines = right_text.split('\n')
                max_lines = max(len(left_lines), len(right_lines))
                
                for line_idx in range(max_lines):
                    left_line = left_lines[line_idx] if line_idx < len(left_lines) else ""
                    right_line = right_lines[line_idx] if line_idx < len(right_lines) else ""
                    
                    # Pad left column to consistent width
                    left_padded = left_line.ljust(40)
                    output += f"{left_padded} {right_line}\n"
                
                output += "\n"
            else:
                output += left_text + "\n\n"
        
        embed = discord.Embed(
            description=f"```{output}```",
            color=0xFFBB5C
        )
        
        await ctx.send(embed=embed)
        
    except ValueError:
        await ctx.send("Please enter a valid price. Example: `$fee 350`")
    except Exception as e:
        await ctx.send("Error calculating fees. Please try again.")
