import discord

@client.command(pass_context = True)
async def suggest(ctx, * ,suggeston):
    embed = discord.Embed(title="Suggestion from: ", description="{0}".format(ctx.message.author), color=0x00ff00)
                       value="{}".format(suggestion), inline=False)
    embed.set_footer(text="Thanks for suggesting!")
    await client.delete_message(ctx.message)
    await client.say(embed=embed)
