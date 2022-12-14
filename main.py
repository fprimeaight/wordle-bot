import discord
from discord.ext import commands

import os
import time

import game
import database
from emote_dictionary import emojiDict
from server import keep_alive

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print("Logged in as {0.user}".format(bot))
    try:
        synced = await bot.tree.sync()
        print(f'Synced {len(synced)}')
    except Exception:
        print(Exception)
    activity = discord.Game(name="Play Wordle with this bot!")
    await bot.change_presence(status=discord.Status.online, activity=activity)

@bot.tree.command(name="play",description="Enter a 5 letter word to guess!")
async def play(interaction: discord.Interaction, word: str):
    if database.checkUser(interaction.user.id) == False:
        database.createUser(interaction.user.id)
    
    if interaction.user.id:
        await interaction.response.send_message(embed=get_loading_message())
        await interaction.edit_original_response(embed=play_wordle(interaction.user,word))
    else:
        await interaction.response.send_message('Error')
    
@bot.tree.command(name="stats",description='Request for your Wordle statistics!')
async def stats(interaction: discord.Interaction):
    if database.checkUser(interaction.user.id) == False:
        database.createUser(interaction.user.id)
    
    await interaction.response.send_message(embed=get_stats(interaction.user))

@bot.tree.command(name="leaderboard",description='Request for server leaderboard!')
async def leaderboard(interaction: discord.Interaction):
    if database.checkUser(interaction.user.id) == False:
        database.createUser(interaction.user.id)
    
    await interaction.response.send_message(embed=get_server_leaderboard(interaction.user,interaction.guild))

@bot.tree.command(name="help",description='Provides instructions on how to play Wordle and use this bot!')
async def help(interaction: discord.Interaction):
    if database.checkUser(interaction.user.id) == False:
        database.createUser(interaction.user.id)

    embed = discord.Embed(title="Help ❓",
                          description='What do you need help with?',
                          color=0x5865F2)

    view = help_menu()
    await interaction.response.send_message(embed=embed,view=view,ephemeral=True)


def get_loading_message():
    header_text = 'Playing Wordle...'
    embed_colour = 0x5865F2
    embed = discord.Embed(title=header_text,
                          description='Loading...',
                          color=embed_colour)
    return embed


def play_wordle(user,word):
    # function to play a wordle game
    try:
        # get relevant values
        user_id = user.id
        user_word = word.upper()
        user_game = game.Wordle(database.get_answer(user_id))
        attempts = database.get_attempts(user_id)
        exp_gain = 0
        header_text = 'Playing Wordle...'
        secondary_text = ''
        embed_colour = 0x5865F2
        
        database.set_isPlaying(user_id, True)

        if len(user_word) == 5 and user_game.checkWordExists(user_word) == True:
            database.set_keyboard(user_id,game.Keyboard.newKeyboardState(database.get_keyboard(user_id),user_game.checkWord(user_word)))
            database.set_output(user_id,user_game.emojiDisplay(user_game.checkWord(user_word)) + '\n')
            output = database.get_output(user_id)

            # give extra exp for using challenge word
            if user_word == database.get_challenge_word(user_id):
                database.gain_exp(user_id, 100)
                database.reset_challenge_word(user_id)
                secondary_text += f'You gained 100 EXP for using the word {user_word}!\n'

            # incrementing attempt counter by 1
            database.set_attempts(user_id,database.get_attempts(user_id) + 1)
            database.set_totalGuesses(user_id,database.get_totalGuesses(user_id) + 1)

            # displays the empty rows/squares left
            blank_rows = ''
            for i in range(5 - attempts):
                blank_rows += emojiDict['Blank'] * 5 + '\n'

            # update embed description text
            secondary_text += f'Enter a 5 letter word!\nYou have {5-attempts} attempts left!\nUse the word {database.get_challenge_word(user_id)} for bonus EXP!\n\n{output + blank_rows}'

            if user_word == database.get_answer(user_id):
                header_text = 'You WON! 🏆'
                embed_colour = 0x7BBA43

                if database.get_attempts(user_id) == 0:
                    exp_gain = int(15000 * (-1 /(database.get_streak(user_id) + 2) + 1.5))
                    header_text = '💸 JACKPOT!!! 💸'
                else:
                    exp_gain = int(4000 /(2**(database.get_attempts(user_id) - 1)) * (-1 /(database.get_streak(user_id) + 2) + 1.5))

                    database.gain_exp(user_id, exp_gain)
                    database.set_streak(user_id,database.get_streak(user_id) + 1)

                    secondary_text = f'You WON in {database.get_attempts(user_id)} attempts!\nYou won {exp_gain} EXP!\nYour win streak is now {database.get_streak(user_id)}!\n\n{output + blank_rows}'

                    embed = discord.Embed(title=header_text,
                                          description=secondary_text,
                                          color=embed_colour)
                    embed.add_field(name="Keyboard",
                                    value=f'Letters Used:\n{game.Keyboard.newKeyboardDisplay(database.get_keyboard(user_id))}',
                                    inline=False)

                    database.set_totalGames(user_id,database.get_totalGames(user_id) + 1)
                    database.set_wins(user_id,database.get_wins(user_id) + 1)
                    database.reset_keyboard(user_id)
                    database.reset_answer(user_id)
                    database.set_attempts(user_id, 0)
                    database.reset_output(user_id)
                    database.set_isPlaying(user_id, False)
                
                return embed

            elif attempts >= 5:
                header_text = 'You LOST! 💀'
                embed_colour = 0xDA5252
                secondary_text = f'Word is {database.get_answer(user_id)}!\nYou lost 600 EXP!\nYour win streak is now 0!\n\n{output + blank_rows}'

                embed = discord.Embed(title=header_text,
                                      description=secondary_text,
                                      color=embed_colour)
                
                embed.add_field(name="Keyboard",
                                value=f'Letters Used:\n{game.Keyboard.newKeyboardDisplay(database.get_keyboard(user_id))}',
                                inline=False)
                
                if database.get_exp(user_id) < 600:
                    database.gain_exp(user_id,-database.get_exp(user_id))
                else:
                    database.gain_exp(user_id, -600)

                database.set_streak(user_id, 0)

                database.set_totalGames(user_id,database.get_totalGames(user_id) + 1)
                database.reset_keyboard(user_id)
                database.reset_answer(user_id)
                database.set_attempts(user_id, 0)
                database.reset_output(user_id)
                database.set_isPlaying(user_id, False)
                
                return embed
                
            else:
                embed = discord.Embed(title=header_text,
                                      description=secondary_text,
                                      color=embed_colour)
                
                embed.add_field(name="Keyboard",
                                value=f'Letters Used:\n{game.Keyboard.newKeyboardDisplay(database.get_keyboard(user_id))}',
                                inline=False)
                return embed

        elif len(user_word) != 5:
            embed = discord.Embed(title=header_text,
                                  description='Word MUST have 5 letters!',
                                  color=0xDA5252)
            return embed

        else:
            embed = discord.Embed(
                title=header_text,
                description='Word you entered is NOT a valid word!',
                color=0xDA5252)
            return embed

    except:
        # Disables user's game is an error is present
        database.set_isPlaying(str(user.id),False)
        print('exception reached')


def get_stats(user):
    # function to return an embed of the user's stats
    start_time = time.time()
    user_id = user.id
    embed = discord.Embed(title='Statistics 📈',
                          description=f'Reviewing statistics of {user}...',
                          color=0x5865F2)
    embed.add_field(name="Total Games Played",
                    value="{:,}".format(database.get_totalGames(user_id)),
                    inline=False)
    
    embed.add_field(name="Total Wins",
                    value="{:,}".format(database.get_wins(user_id)),
                    inline=False)
    
    embed.add_field(name="Total EXP",
                    value=f'{"{:,}".format(database.get_exp(user_id))}',
                    inline=False)
    
    embed.add_field(
        name="Streak",
        value=
        f'{"{:,}".format(database.get_streak(user_id))} `(+{round((-1/(database.get_streak(user_id)+2)+0.5)*100,2)}% EXP Bonus)`',
        inline=False)
    
    embed.add_field(name="Average Guesses",
                    value=round(
                        database.get_totalGuesses(user_id) /
                        database.get_totalGames(user_id), 2),
                    inline=False)
    
    embed.set_thumbnail(url=user.avatar)
    embed.set_footer(text=f'Runtime: {(time.time()-start_time):.2e} seconds')
    return embed


def get_server_leaderboard(user, server):
    # function to return an embed of server leaderboard
    start_time = time.time()

    leaderboard_size = 5
    leaderboard = {}
    all_users = database.get_users()

    leaderboard_usernames = ''
    leaderboard_exp = ''
    leaderboard_wins = ''

    for member in server.members:
        memberID = str(member.id)
        if memberID in all_users:
            leaderboard[database.get_exp(memberID)] = memberID

    sorted_leaderboard = sorted(leaderboard.items(),
                                key=lambda x: x[0],
                                reverse=True)

    index = 0
    while index < leaderboard_size and index < len(sorted_leaderboard):
        # getting user_id of top players
        top_player_id = int(sorted_leaderboard[index][1])

        # getting usernames of top players
        username = str(bot.get_user(top_player_id))

        if len(username) > 17:
            username = f'{username[0:8]}...{username[len(username)-5:len(username)+1]}'
        leaderboard_usernames += f'{index + 1}. {username}\n'

        # getting EXP of top players
        leaderboard_exp += f'{"{:,}".format(database.get_exp(top_player_id))}\n'

        # getting wins of top players
        leaderboard_wins += f'{"{:,}".format(database.get_wins(top_player_id))}\n'

        index += 1

    embed = discord.Embed(title="🏆 Leaderboard",
                          description='Top people in the server!',
                          color=0x5865F2)
    
    embed.add_field(name="User", value=f'{leaderboard_usernames}', inline=True)
    embed.add_field(name="EXP", value=f'{leaderboard_exp}', inline=True)
    embed.add_field(name="Wins", value=f'{leaderboard_wins}', inline=True)
    embed.set_footer(text=f'Runtime: {(time.time()-start_time):.2e} seconds')
    return embed


class help_menu(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.value = None

    @discord.ui.button(label='Commands',style=discord.ButtonStyle.blurple,emoji="🤖")
    async def menu1(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.edit_message(embed=get_cmd_list())

    @discord.ui.button(label='How to Play',style=discord.ButtonStyle.green,emoji="📜")
    async def menu2(self, interaction: discord.Interaction, button: discord.ui.Button):  
        await interaction.response.edit_message(embed=get_help())
    
    
def get_help():
    start_time = time.time()
    description_text = ''

    f = open('menu.txt', 'r')

    for line in f:
        description_text += line

    embed = discord.Embed(title="Help ❓",
                          color=0x5865F2)
    embed.add_field(name='How to play',value=description_text)
    embed.set_footer(text=f'Runtime: {(time.time()-start_time):.2e} seconds')
    return embed


def get_cmd_list():
    start_time = time.time()
    description_text = '''
                        /play [word] -> Starts a wordle game / Enter in your guessed word!\n 
                        /stats -> Shows all the related statistics of all your past Wordle games!\n
                        /leaderboard -> Shows the top people in the server!\n
                        /help -> Gives information about bot commands or help on how to play Wordle!'''
    
    embed = discord.Embed(title="Help ❓",
                          color=0x5865F2)

    embed.add_field(name='Commands',value=description_text)
    
    embed.set_footer(text=f'Runtime: {(time.time()-start_time):.2e} seconds')
    return embed
    

keep_alive()
bot.run(os.environ['TOKEN'])
