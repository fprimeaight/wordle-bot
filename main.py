import discord
import game
import os
import random
import discord_components
import database
from discord.ext import commands
from server import keep_alive
import time

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)
discord_components.DiscordComponents(bot)

@bot.event
async def on_ready():
  print("Logged in as {0.user}".format(bot))
  activity = discord.Game(name="!testcmd")
  await bot.change_presence(status = discord.Status.online, activity = activity)
      

@bot.command()
async def testcmd(ctx):
  # create embed
  start_time = time.time()
  embed = discord.Embed(title = "📝 Menu", description='Choose an option below!',color=0x5865F2)
  embed.set_footer(text = f'Runtime: {(time.time()-start_time):.2e} seconds')
  
  button1 = discord_components.Button(label='Play', style = '1', emoji='▶️', custom_id='play')
  button2 = discord_components.Button(label='Stats',style = '1', emoji = '📈', custom_id='stats')
  button3 = discord_components.Button(label='Leaderboard', style = '1', emoji='🏆', custom_id='leaderboard')
  button4 = discord_components.Button(label='Help', style = '1', emoji='❓', custom_id='help')
  
  menu = [button1,button2,button3,button4]

  # shows menu to user
  message = await ctx.reply(embed=embed, components=[menu])

  # ensure that user who pressed the button is the user who called the original command
  interaction = await bot.wait_for('button_click')

  while interaction.author != ctx.author:
    interaction = await bot.wait_for('button_click')

  # disable buttons and update menu look after a button is pressed
  for button in menu:
    if button.custom_id == interaction.custom_id:
      button.style = 3
    button.disabled = True
    
  await message.edit(embed=embed, components=[menu])

  if interaction.custom_id == 'play':
    # when 'Play button is pressed'

    await ctx.reply('run function1')

  elif interaction.custom_id == 'stats':
    # when 'Stats' button is pressed
    if str(ctx.author.id) not in database.get_users():
      await interaction.send(f'<@{ctx.author.id}> Play a game first to view your stats!', ephemeral = False)
    else:
      await ctx.reply(embed=get_stats(ctx.author))
  
  elif interaction.custom_id == 'leaderboard':
    # when 'Leaderboard' button is pressed
    server = message.guild
    leaderboard = get_server_leaderboard(ctx.author,server)
    await ctx.reply(embed=leaderboard)
  
  else:
    # when 'Help' button is pressed
    await ctx.reply(embed=help())

def get_stats(user):
  # function to return an embed of the user's stats
  start_time = time.time()
  user_id = user.id
  embed = discord.Embed(title = 'Statistics 📈', description=f'Reviewing statistics of {user}...',color = 0x5865F2)
  embed.add_field(name = "Total Games Played", value ="{:,}".format(database.get_totalGames(user_id)), inline = False)
  embed.add_field(name = "Total Wins", value = "{:,}".format(database.get_wins(user_id)), inline = False)
  embed.add_field(name = "Total EXP", value = f'{"{:,}".format(database.get_exp(user_id))}', inline = False)
  embed.add_field(name = "Streak", value = f'{"{:,}".format(database.get_streak(user_id))} `(+{round((-1/(database.get_streak(user_id)+2)+0.5)*100,2)}% EXP Bonus)`', inline = False)
  embed.add_field(name = "Average Guesses", value = round(database.get_totalGuesses(user_id)/database.get_totalGames(user_id),2), inline = False)
  embed.set_thumbnail(url=user.avatar_url)
  embed.set_footer(text = f'Runtime: {(time.time()-start_time):.2e} seconds')
  return embed


def get_server_leaderboard(user,server):
  # function to return an embed of server leaderboard
  leaderboard_size = 5 
  leaderboard = {}
  all_users = database.get_users()
  
  leaderboard_usernames = ''
  leaderboard_exp = ''
  leaderboard_wins = ''
  
  start_time = time.time()
  user_id = user.id
  
  for member in server.members:
    memberID = str(member.id)
    if memberID in all_users:
      leaderboard[database.get_exp(memberID)] = memberID

  sorted_leaderboard = sorted(leaderboard.items(), key=lambda x: x[0], reverse=True)

  index = 0
  while index < leaderboard_size and index < len(sorted_leaderboard):
    # getting user_id of top players
    top_player_id = int(sorted_leaderboard[index][1])
    # print(top_player_id)
    
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
  
  embed = discord.Embed(title = "🏆 Leaderboard", description='Top people in the server!',color=0x5865F2)
  embed.add_field(name = "User", value = f'{leaderboard_usernames}', inline = True)
  embed.add_field(name = "EXP", value = f'{leaderboard_exp}', inline = True)
  embed.add_field(name = "Wins", value = f'{leaderboard_wins}', inline = True)
  embed.set_footer(text = f'Runtime: {(time.time()-start_time):.2e} seconds')
  return embed
  
# keep_alive()
def help():
  start_time = time.time()
  embed = discord.Embed(title = "Help ❓", description='Placeholder Text',color=0x5865F2)
  embed.set_footer(text = f'Runtime: {(time.time()-start_time):.2e} seconds')
  return embed
  
keep_alive()
bot.run(os.environ['TOKEN'])

# @client.event

# async def on_message(message):
#   if message.author == client.user:
#     return
  
#   if message.content.startswith('!w'):
#     user_id = message.author.id
#     if checkUser(user_id) == False:
#       wordle_answer = answer()
#       challenge_word = answer()
#       attempts = 0
#       output = ''
#       totalGames = 0
#       wins = 0
#       totalGuesses = 0
#       exp = 0
#       streak = 0 
#       keyboard = default_keyboard
#       db[str(user_id)] = [wordle_answer,attempts,output,totalGames,wins,totalGuesses,exp,challenge_word,streak,keyboard]
  
#   if message.content.startswith('!wplay'):

#     #print(checkPlaying(user_id)) #--> check for debugging

#     game = Wordle((db[str(user_id)])[0])
#     attempts = (db[str(user_id)])[1]
#     exp_gain = 0
    
#     curr_keyboard = (db[str(user_id)])[9]
#     #print(curr_keyboard)

#     if len(message.content.split()) == 2:
#       word = (message.content.split())[1].upper()
    
#       #--> check if word is 5 letters and is valid

#       if len(word) == 5 and checkWordExists(word) == True:
#         db[str(user_id)][9] = newKeyboardState(curr_keyboard,game.checkWord(word))

#         (db[str(user_id)])[2] += emojiDisplay(game.checkWord(word)) + '\n'
#         output = db[str(user_id)][2]
        
#         #give extra exp for using challenge word
#         if word == (db[str(user_id)])[7]:
#           (db[str(user_id)])[6] += 100
#           (db[str(user_id)])[7] = answer()
#           await message.channel.send(f'You gained an extra 100 EXP for using the word {word}!')
          

#         embedMsg = discord.Embed(title = "Playing Wordle...", description = f'Enter a 5 letter word! You have {5-attempts} attempts left!\nUse the word {(db[str(user_id)])[7]} for bonus EXP!\n\n{output}', color=0x48b400)
#         embedMsg.add_field(name = "Keyboard", value = f'Letters Used:\n{newKeyboardDisplay(curr_keyboard)}', inline = False)
#         await message.reply(embed=embedMsg)

#         #incrementing attempt counter by 1
#         (db[str(user_id)])[1] += 1
#         (db[str(user_id)])[5] += 1
        
#         if game.checkWin(word) == True:
#           if attempts == 0:
#             exp_gain = int(15000 * (-1/(db[str(user_id)][8]+2)+1.5))
#             await message.reply(f'💸 JACKPOT!!! 💸')
#           else:
#             exp_gain = int(4000/(2**(attempts)) * (-1/(db[str(user_id)][8]+2)+1.5))
          
#           (db[str(user_id)])[6] += exp_gain
#           db[str(user_id)][8] += 1
#           await message.reply(f'You WON in {attempts+1} attempts! 🎉🥳🎉\nYou won {exp_gain} EXP!\nYour win streak is now {db[str(user_id)][8]}!')
          
#           #increase total games by 1
#           (db[str(user_id)])[3] += 1
#           (db[str(user_id)])[4] += 1

#           (db[str(user_id)])[9] = default_keyboard
#           (db[str(user_id)])[0] = answer()
#           (db[str(user_id)])[1] = 0
#           (db[str(user_id)])[2] = ''
        
#         elif attempts == 5:
#           if (db[str(user_id)])[6] < 600:
#             (db[str(user_id)])[6] = 0
#           else:
#             (db[str(user_id)])[6] -= 600
          
#           db[str(user_id)][8] = 0
#           await message.reply(f'You LOST! 😔 Word is {(db[str(user_id)])[0]}!\nYou lost 600 EXP!\nYour win streak is now {db[str(user_id)][8]}!')

#           #increase total games by 1
#           (db[str(user_id)])[3] += 1

#           (db[str(user_id)])[9] = default_keyboard
#           (db[str(user_id)])[0] = answer()
#           (db[str(user_id)])[1] = 0
#           (db[str(user_id)])[2] = ''
      
#       elif len(word) != 5:
#         await message.reply('Word MUST have 5 letters!')
#       else:
#         await message.reply('Word you entered is not a valid word!')
    
#   if message.content.startswith('!wstats'):

#     totalGames = (db[str(user_id)])[3]
#     wins = (db[str(user_id)])[4]
#     totalGuesses = (db[str(user_id)])[5]
#     exp = int((db[str(user_id)])[6])
#     streak = db[str(user_id)][8]
    
#     if totalGames != 0: 
#       avgGuesses = round(totalGuesses/totalGames,2)
#     else:
#       avgGuesses = 0

#     #getting users profile picture
#     pfp = message.author.avatar_url

#     userList = db.keys()
    
#     serverList = []
    
#     server_id = message.guild.id
#     server = client.get_guild(server_id)
    
#     #implementing server leaderboard
    
#     leaderboardSize = 5
#     scores = []
#     leaderboard = [''] * leaderboardSize
#     winexp_list = [''] * leaderboardSize
#     avgGuesses_list = [''] * leaderboardSize
#     serverUserLeaderboardString = ''
#     serverWinsExpLeaderboardString = ''
#     serverAvgGuessLeaderboardString = ''
    
#     for member in server.members:
#       memberID = str(member.id)
#       if memberID in userList:
#         serverList.append(memberID)
        
#     for key in serverList:
#       scores.append((key,db[key][6]))
    
#     # #array of scores
#     # #use index 3,4 and 5 => totalGames,wins,totalGuesses
#     scores.sort(key=lambda x:x[1],reverse = True)

#     leaderboardPos = scores.index((str(user_id),db[str(user_id)][6])) + 1

#     if leaderboardPos > 3:
#       leaderboardPos = '#' + str(leaderboardPos)
#     elif leaderboardPos == 1:
#       leaderboardPos = '🥇 #' + str(leaderboardPos)
#     elif leaderboardPos == 2:
#       leaderboardPos = '🥈 #' + str(leaderboardPos)
#     elif leaderboardPos == 3:
#       leaderboardPos = '🥉 #' + str(leaderboardPos)
    
#     for i in range(leaderboardSize):
#       if len(scores) != 0:
#         #print(db.keys())
        
#         key = scores[0][0]
        
#         username = str(await client.fetch_user(key))
#         if len(username) > 17:
#           username = username[0:8] + '...' + username[len(username)-5:len(username)+1]
        
#         leaderboard[i] = f'{i+1}. {username}\n'
#         winexp_list[i] = f' {int(db[key][6])} EXP | {db[key][4]} Wins \n'
#         if db[key][3] != 0:
#           avgGuesses_list[i] = f' {round((db[key][5]/db[key][3]),2)} \n'
#         else:
#           avgGuesses_list[i] = ''

#         scores.pop(0)
      
#       else:    
#         break
      
#     i = 1
#     for data in leaderboard:
#       if data == '':
#         data = f'{i}. None\n'
#       serverUserLeaderboardString += data
#       i += 1

#     for data in winexp_list:
#       if data == '':
#         data = f' None \n'
#       serverWinsExpLeaderboardString += data

#     for data in avgGuesses_list:
#       if data == '':
#         data = f' None \n'
#       serverAvgGuessLeaderboardString += data

#     #check latency
#     #latency = client.latency
#     #await message.channel.send(f'debug={latency*1000}ms')
      
#     embedMsg = discord.Embed(title = f"{message.author}'s Wordle Stats 📈", description = f'Total Games: {totalGames}\nTotal Wins: {wins}\nWin Streak: {streak} `(+{round((-1/(streak+2)+0.5)*100,2)}% EXP Bonus)`\nAverage No. Of Guesses: {avgGuesses}\nEXP: {exp}\nLeaderboard Position: {leaderboardPos}', color=0x48b400)
#     embedMsg.add_field(name = "Server Leaderboard 🏆", value = f'Top {leaderboardSize} people in the server ranked based on EXP!', inline = False)
#     embedMsg.add_field(name = "User", value = f'{serverUserLeaderboardString}', inline = True)
#     embedMsg.add_field(name = "EXP | Wins", value = f'`{serverWinsExpLeaderboardString}`', inline = True)
#     embedMsg.add_field(name = "Avg. No. of Guesses", value = f'`{serverAvgGuessLeaderboardString}`', inline = True)
    
#     embedMsg.set_thumbnail(url=pfp)
#     await message.reply(embed=embedMsg)
    

#   if message.content.startswith('!whelp'):

#     #text to display for how to play wordle
#     howToPlayText = 'Guess the WORDLE in six tries.\n\nEach guess must be a valid five-letter word.\nAfter each guess, the color of the tiles will change to show how close your guess was to the word.\n\n<:wordle_green_w:981415135874797648> means that the letter (in this case, the letter W) is in the word and is in the correct spot.\n\n<:wordle_yellow_o:981429169198104646> means that the letter (in this case, the letter O) is in the word but is in the wrong spot.\n\n<:wordle_black_r:981439988312965190> means that the letter (in this case, the letter R) is NOT in the word.'

#     embedMsg = discord.Embed(title = "Wordle Help ❓", description = 'Bot has the commands below...\n`!wplay [*insert your word*]` -> To play Wordle\n`!wstats` -> To review your stats\n`!whelp` -> To view all bot commands\n`!wquit` -> To quit out of your Wordle Game', color=0x48b400)
#     embedMsg.add_field(name = "How to play Wordle: ", value = howToPlayText, inline = False)
#     await message.reply(embed=embedMsg)
    
#   elif message.content.startswith('!wquit'):
#     if (db[str(user_id)])[1] == 0:
#       await message.reply('You are currently not playing in a Wordle game!')
#     else:
#       (db[str(user_id)])[1] = 0
#       (db[str(user_id)])[2] = ''

#       if (db[str(user_id)])[6] < 600:
#         (db[str(user_id)])[6] = 0
#       else:
#         (db[str(user_id)])[6] -= 600
      
#       db[str(user_id)][8] = 0
      
#       await message.reply(f'Quitted out of wordle game! Word is {db[str(user_id)][0]}!\nYou lost 600 EXP!\nYour win streak is now 0!')

#       (db[str(user_id)])[0] = answer()
      
# keep_alive()
# client.run(os.environ['TOKEN'])