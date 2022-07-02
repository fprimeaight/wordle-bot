import discord
import game
import os
import discord_components
import database
from discord.ext import commands
# from server import keep_alive
import time

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)
discord_components.DiscordComponents(bot)

@bot.event
async def on_ready():
  print("Logged in as {0.user}".format(bot))
  activity = discord.Game(name="!testcmd")
  await bot.change_presence(status = discord.Status.online, activity = activity)
      
@bot.event
async def on_message(message):
  if message.author.id != bot.user.id and database.checkUser(message.author.id) == True:
    if len(message.content.split()) == 1 and database.get_isPlaying(str(message.author.id)) == True and message.content != '!testcmd':
      user_id = message.author.id
      user_word = message.content.upper()
      user_game = game.Wordle(database.get_answer(user_id))
      attempts = database.get_attempts(user_id)
      exp_gain = 0

      if len(user_word) == 5 and user_game.checkWordExists(user_word) == True:
        database.set_keyboard(user_id,game.Keyboard.newKeyboardState(database.get_keyboard(user_id),user_game.checkWord(user_word)))
        database.set_output(user_id,user_game.emojiDisplay(user_game.checkWord(user_word)) + '\n')
        output = database.get_output(user_id)

        # give extra exp for using challenge word
        if user_word == database.get_challenge_word(user_id):
          database.gain_exp(user_id,100)
          database.reset_challenge_word(user_id)
          await message.channel.send(f'You gained 100 EXP for using the word {user_word}!')
            
  
        embed = discord.Embed(title = "Playing Wordle...", description = f'Enter a 5 letter word! You have {5-attempts} attempts left!\nUse the word {database.get_challenge_word(user_id)} for bonus EXP!\n\n{output}', color=0x5865F2)
        embed.add_field(name = "Keyboard", value = f'Letters Used:\n{game.Keyboard.newKeyboardDisplay(database.get_keyboard(user_id))}', inline = False)
        await message.reply(embed=embed)

        #incrementing attempt counter by 1
        database.set_attempts(user_id,database.get_attempts(user_id) + 1)
        database.set_totalGuesses(user_id,database.get_totalGuesses(user_id) + 1)
        
        if user_word == database.get_answer(user_id):
          if database.get_attempts(user_id) == 0:
            exp_gain = int(15000 * (-1/(database.get_streak(user_id)+2)+1.5))
            await message.reply(f'💸 JACKPOT!!! 💸')
          else:
            exp_gain = int(4000/(2**(database.get_attempts(user_id)-1)) * (-1/(database.get_streak(user_id)+2)+1.5))

          database.gain_exp(user_id,exp_gain)
          database.set_streak(user_id,database.get_streak(user_id) + 1)
          await message.reply(f'You WON in {database.get_attempts(user_id)} attempts! 🎉🥳🎉\nYou won {exp_gain} EXP!\nYour win streak is now {database.get_streak(user_id)}!')
          
          database.set_totalGames(user_id,database.get_totalGames(user_id) + 1)
          database.set_wins(user_id,database.get_wins(user_id) + 1)
          database.reset_keyboard(user_id)
          database.reset_answer(user_id)
          database.set_attempts(user_id,0)
          database.reset_output(user_id)
          database.set_isPlaying(user_id,False)

        elif attempts >= 5:
          print(attempts)
          if database.get_exp(user_id) < 600:
            database.gain_exp(user_id,-database.get_exp(user_id))
          else:
            database.gain_exp(user_id,-600)
            
          database.set_streak(user_id,0)
          await message.reply(f'You LOST! 😔 Word is {database.get_answer(user_id)}!\nYou lost 600 EXP!\nYour win streak is now {database.get_streak(user_id)}!')
          
          database.set_totalGames(user_id,database.get_totalGames(user_id) + 1)
          database.reset_keyboard(user_id)
          database.reset_answer(user_id)
          database.set_attempts(user_id,0)
          database.reset_output(user_id)
          
        
      elif len(user_word) != 5:
        await message.reply('Word MUST have 5 letters!')
      else:
        await message.reply('Word you entered is not a valid word!')
        
    await bot.process_commands(message)
      
@bot.command()
async def testcmd(ctx):
  # create embed
  start_time = time.time()
  if database.checkUser(ctx.author) == True:
    database.set_isPlaying(ctx.author.id,False)
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
    await ctx.reply(play_wordle(ctx.author))

  elif interaction.custom_id == 'stats':
    # when 'Stats' button is pressed
    if str(ctx.author.id) not in database.get_users():
      await interaction.send(f'<@{ctx.author.id}> Play a game first to view your stats!', ephemeral = False)
    else:
      await ctx.reply(embed=get_stats(ctx.author))
  
  elif interaction.custom_id == 'leaderboard':
    # when 'Leaderboard' button is pressed
    server = message.guild
    await ctx.reply(embed=get_server_leaderboard(ctx.author,server))
  
  else:
    # when 'Help' button is pressed
    await ctx.reply(embed=help())

def play_wordle(user):
  # function to start a wordle game
  user_id = user.id
  
  if database.checkUser(user_id) == False:
    database.createUser(user_id)
    
  database.set_isPlaying(user_id,True)

  return f'Enter a word!'
  
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
  start_time = time.time()
  
  leaderboard_size = 5 
  leaderboard = {}
  all_users = database.get_users()
  user_id = user.id
  
  leaderboard_usernames = ''
  leaderboard_exp = ''
  leaderboard_wins = ''
  
  for member in server.members:
    memberID = str(member.id)
    if memberID in all_users:
      leaderboard[database.get_exp(memberID)] = memberID

  sorted_leaderboard = sorted(leaderboard.items(), key=lambda x: x[0], reverse=True)

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
  
  embed = discord.Embed(title = "🏆 Leaderboard", description='Top people in the server!',color=0x5865F2)
  embed.add_field(name = "User", value = f'{leaderboard_usernames}', inline = True)
  embed.add_field(name = "EXP", value = f'{leaderboard_exp}', inline = True)
  embed.add_field(name = "Wins", value = f'{leaderboard_wins}', inline = True)
  embed.set_footer(text = f'Runtime: {(time.time()-start_time):.2e} seconds')
  return embed
  
# keep_alive()
def help(user):
  start_time = time.time()
  embed = discord.Embed(title = "Help ❓", description='Placeholder Text',color=0x5865F2)
  embed.set_footer(text = f'Runtime: {(time.time()-start_time):.2e} seconds')
  return embed
  
# keep_alive()
bot.run(os.environ['TOKEN'])