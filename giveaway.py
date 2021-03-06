import discord
import random

@client.command(pass_context = True)
async def giveaway(ctx):
    if ctx.message.author.server_permissions.manage_server:
        if ctx.message.author.bot:
            await client.say("Bots can't use commands.")
            return
        """Create a giveaway throught an interactive setup!"""
        await client.say(":tada: WooHoo!!!! We will create your giveaway :tada:")
        await asyncio.sleep(1)
        await ctx.bot.say("What channel will the Giveaway be help in?\n"
                        "\n"
                        "`Ex. Do a channel in your server. ('general' not #general)`")
        channel_name = await client.wait_for_message(author = ctx.message.author)
        g_channel = discord.utils.get(ctx.message.server.channels, name = channel_name.content)
    
        #Check if the channel even exists!
        if not g_channel:
            await client.say(":x: | Channel Not Found! | Start Over!")
        if g_channel:
            await client.say(":white_check_mark: | Channel Found And Selected!")
            await asyncio.sleep(1)
            await client.say("How long will the Giveaway Be?\n"
                            "\n"
                            "Ex. 5 Minutes, say 5m, 1 Hour, say 1h ,etc. (Please only use Whole Numbers!")
            duration = await client.wait_for_message(author = ctx.message.author)
            await asyncio.sleep(1)
            await client.say(":tada: Giveaway set to end {} after the start".format(duration.content))
            await asyncio.sleep(1)
            await client.say("How many winner will be selected?\n"
                              "\n"
                              "`Pick a Number 1 (More Winners Coming Soon!)`")
            msg = await client.wait_for_message(author = ctx.message.author)
            g_winners = int(msg.content)
            await asyncio.sleep(1)
            await client.say(":tada: {} Winner(s) will be Chosen".format(g_winners))
            await asyncio.sleep(1)
            await client.say("What are you giving away?\n"
                            "\n"
                            "`This Will Become The Title Of The Giveaway`\n"
                            "`Ex. If I'm Giving away Free Steam Keys I Would say Free Steam Keys`")
            g_prize = await ctx.bot.wait_for_message(author = ctx.message.author)
            await asyncio.sleep(1)
            await client.say("Giving away {}".format(g_prize.content))
            await asyncio.sleep(1)
            await client.say(":tada: Almost Done Please Confirm Below")
            await asyncio.sleep(1)
            await client.say("You are Giving away `{}` with `{}` Winners, that will Last `{}`?\n"
                            "\n"
                            "`If This Is Correct Say Yes. If Not Say No (You Will Have To Start Over)`".format(g_prize.content, g_winners, duration.content))
            response = await client.wait_for_message(author = ctx.message.author, channel = ctx.message.channel)
            response = response.content.lower()

            duration = duration.content

            unit = duration[-1]
            if unit == 's':
                time = int(duration[:-1])
                longunit = 'seconds'
            elif unit == 'm':
                time = int(duration[:-1]) * 60
                longunit = 'minutes'
            elif unit == 'h':
                time = int(duration[:-1]) * 60 * 60
                longunit = 'hours'
            else:
                return

            yesres = 'yes'
            nores = 'no'
            if response.lower() == nores.lower():
                await asyncio.sleep(1)
                await client.say(":x: | Giveaway Canceled, Please Restart The Setup")
            if response.lower() == yesres.lower():
                await client.say(":tada: Giveaway Started! :tada:")

                color = ''.join([random.choice('0123456789ABCDEF') for x in range(6)])
                color = int(color, 16)
                embed=discord.Embed(title=":tada: __**Giveaway: {}**__ :tada:".format(g_prize.content), colour = discord.Colour(value=color), timestamp = datetime.datetime.utcnow())
                embed.add_field(name = "Prize: ",value = "{}".format(g_prize.content))
                embed.add_field(name = "Winners: ", value = "{} Winner(s)".format(g_winners))
                embed.add_field(name = "Time: ", value = "{}".format(duration), inline = True)
                embed.set_footer(text = "Add The Reaction to join! Started @ ")
                give_away = await client.send_message(g_channel, embed = embed)
                ga_message = await client.add_reaction(give_away, "\U0001f389")
                await asyncio.sleep(time)#Sleep for the duration

                ga_message = await client.get_message(give_away.channel, give_away.id)
                ga_users=[]
                for user in await client.get_reaction_users(ga_message.reactions[0]):
                    ga_users.append(user.mention)
                ga_client = ctx.message.server.get_member('500854299455127563') #Put your bot id here for this to pull it.
                ga_users.remove(ga_client.mention)
                if len(ga_users) == 0:
                    error = discord.Embed(title=":warning: Error!",description="The giveaway ended with no participants, could not chose a winner",color=0xff0000)
                    await client.say(embed=error)
                else:
                    winner_list=[]
                    for loop in range(g_winners):
                        winner = random.choice(ga_users)
                        ga_users.remove(winner)
                        winner_list.append(winner)
                        msg = ""
            
                color = ''.join([random.choice('0123456789ABCDEF') for x in range(6)])#Winning Embed
                color = int(color, 16)
                embed=discord.Embed(title=":tada: __**Giveaway Ended!**__ :tada:", colour = discord.Colour(value=color), timestamp = datetime.datetime.utcnow())
                embed.add_field(name = "Winners: ", value = "{} Winner(s)".format(g_winners))
                embed.add_field(name = "Winner(s): ", value = ",\n".join(winner_list))
                embed.add_field(name = "Prize: ", value = "{}".format(g_prize.content))
                embed.set_footer(text = "Better Luck Next Time! Ended @ ")
                await client.edit_message(give_away, embed = embed)
                for winner in winner_list:
                    msg += ", " + winner
                await client.send_message(g_channel, ":tada: " + ", ".join(winner_list) + " won **{}**".format(g_prize.content))
    else:
        embed = discord.Embed(color=0xff0200)
        author = ctx.message.author
        embed.set_author(icon_url=author.avatar_url, name="Uh Oh.")
        embed.add_field(name=":x: Error", value="You are missing some permissions there bud. ```Permissions: Manage Server```", inline=False)
        await client.say(embed=embed)
