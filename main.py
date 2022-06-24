import discord
import os
from replit import db 
import random
from server import keep_alive

intents = discord.Intents.all()
client = discord.Client(intents=intents)

emojiDict = {
             'GA':'<:wordle_green_a:981408163217682472>',
             'GB':'<:wordle_green_b:981408499558936616>',
             'GC':'<:wordle_green_c:981409544863354901>',
             'GD':'<:wordle_green_d:981409583597781012>',
             'GE':'<:wordle_green_e:981410275087507477>',
             'GF':'<:wordle_green_f:981414626732429312>',
             'GG':'<:wordle_green_g:981414670177017887>',
             'GH':'<:wordle_green_h:981414716704444416>',
             'GI':'<:wordle_green_i:981414758366470184>',
             'GJ':'<:wordle_green_j:981414790230605865>',
             'GK':'<:wordle_green_k:981414823080378398>',
             'GL':'<:wordle_green_l:981414843573743656>',
             'GM':'<:wordle_green_m:981414863723188304>',
             'GN':'<:wordle_green_n:981414891451719722>',
             'GO':'<:wordle_green_o:981414916026146878>',
             'GP':'<:wordle_green_p:981414945885405184>',
             'GQ':'<:wordle_green_q:981414966949199892>',
             'GR':'<:wordle_green_r:981415001921306635>',
             'GS':'<:wordle_green_s:981415043520430110>',
             'GT':'<:wordle_green_t:981415066584895521>',
             'GU':'<:wordle_green_u:981415083391479840>',
             'GV':'<:wordle_green_v:981415115133976587>',
             'GW':'<:wordle_green_w:981415135874797648>',
             'GX':'<:wordle_green_x:981415168028327946>',
             'GY':'<:wordle_green_y:981415186370002975>',
             'GZ':'<:wordle_green_z:981415202786541629>',
             'YA':'<:wordle_yellow_a:981428810736082964>',
             'YB':'<:wordle_yellow_b:981428841299992576>',
             'YC':'<:wordle_yellow_c:981428862544134184>',
             'YD':'<:wordle_yellow_d:981428886992748605>',
             'YE':'<:wordle_yellow_e:981428911785271316>',
             'YF':'<:wordle_yellow_f:981428934233194516>',
             'YG':'<:wordle_yellow_g:981428958396571678>',
             'YH':'<:wordle_yellow_h:981428986754252871>',
             'YI':'<:wordle_yellow_i:981429014147260416>',
             'YJ':'<:wordle_yellow_j:981429041389240330>',
             'YK':'<:wordle_yellow_k:981429064076255242>',
             'YL':'<:wordle_yellow_l:981429094220701726>',
             'YM':'<:wordle_yellow_m:981429118371508335>',
             'YN':'<:wordle_yellow_n:981429141758967839>',
             'YO':'<:wordle_yellow_o:981429169198104646>',
             'YP':'<:wordle_yellow_p:981429197731921951>',
             'YQ':'<:wordle_yellow_q:981429225582104596>',
             'YR':'<:wordle_yellow_r:981429257748242482>',
             'YS':'<:wordle_yellow_s:981429285690679386>',
             'YT':'<:wordle_yellow_t:981429318322372699>',
             'YU':'<:wordle_yellow_u:981429344129908776>',
             'YV':'<:wordle_yellow_v:981429370021363712>',
             'YW':'<:wordle_yellow_w:981429393664659497>',
             'YX':'<:wordle_yellow_x:981429421896499280>',
             'YY':'<:wordle_yellow_y:981431940769017856>',
             'YZ':'<:wordle_yellow_z:981431962185125928>',
             'RA':'<:wordle_black_a:981439626763968533>',
             'RB':'<:wordle_black_b:981439655490756698>',
             'RC':'<:wordle_black_c:981439673333350420>',
             'RD':'<:wordle_black_d:981439695290523678>',
             'RE':'<:wordle_black_e:981439714697576508>',
             'RF':'<:wordle_black_f:981439733844545537>',
             'RG':'<:wordle_black_g:981439752286920717>',
             'RH':'<:wordle_black_h:981439772675428362>',
             'RI':'<:wordle_black_i:981439801481895967>',
             'RJ':'<:wordle_black_j:981439820515668038>',
             'RK':'<:wordle_black_k:981439844553203722>',
             'RL':'<:wordle_black_l:981439865205960754>',
             'RM':'<:wordle_black_m:981439884713689120>',
             'RN':'<:wordle_black_n:981439908956766228>',
             'RO':'<:wordle_black_o:981439926262460446>',
             'RP':'<:wordle_black_p:981439942246957086>',
             'RQ':'<:wordle_black_q:981439966624251904>',
             'RR':'<:wordle_black_r:981439988312965190>',
             'RS':'<:wordle_black_s:981440009833967676>',
             'RT':'<:wordle_black_t:981440040272011264>',
             'RU':'<:wordle_black_u:981440063785275442>',
             'RV':'<:wordle_black_v:981440093690675220>',
             'RW':'<:wordle_black_w:981440116822245396>',
             'RX':'<:wordle_black_x:981440134216028200>',
             'RY':'<:wordle_black_y:981440195540971550>',
             'RZ':'<:wordle_black_z:981440219322662933>',
             'BA':'<:wordle_grey_a:981830054596198421>',
             'BB':'<:wordle_grey_b:981830129296740353>',
             'BC':'<:wordle_grey_c:981830160502386718>',
             'BD':'<:wordle_grey_d:981830213824565288>',
             'BE':'<:wordle_grey_e:981830236222160906>',
             'BF':'<:wordle_grey_f:981830259278241792>',
             'BG':'<:wordle_grey_g:981830290165071912>',
             'BH':'<:wordle_grey_h:981830320519262228>',
             'BI':'<:wordle_grey_i:981830346398113822>',
             'BJ':'<:wordle_grey_j:981830375825375272>',
             'BK':'<:wordle_grey_k:981830437007671317>',
             'BL':'<:wordle_grey_l:981830509627863071>',
             'BM':'<:wordle_grey_m:981830526325362688>',
             'BN':'<:wordle_grey_n:981830551646384149>',
             'BO':'<:wordle_grey_o:981830593031581707>',
             'BP':'<:wordle_grey_p:981830716990042162>',
             'BQ':'<:wordle_grey_q:981830742071992392>',
             'BR':'<:wordle_grey_r:981830768156348436>',
             'BS':'<:wordle_grey_s:981830798728638464>',
             'BT':'<:wordle_grey_t:981830829560979466>',
             'BU':'<:wordle_grey_u:981830855792160828>',
             'BV':'<:wordle_grey_v:981830882748948510>',
             'BW':'<:wordle_grey_w:981830953892728832>',
             'BX':'<:wordle_grey_x:981830993637953626>',
             'BY':'<:wordle_grey_y:981831019684581386>',
             'BZ':'<:wordle_grey_z:981831048369422386>'
            }

class Wordle:
    def __init__(self,answer):
        self.answer = answer
        self.dictionary = {}
        for letter in answer:
            if letter not in self.dictionary:
                self.dictionary[letter] = 1
            else:
                self.dictionary[letter] += 1
    
    #Note: checkWord returns an array
    def checkWord(self,word):
        checkWordDictionary = self.dictionary
        output = ['']*5
        
        #check for correct letters at correct position
        i = 0
        for letter in word:
            if letter == self.answer[i]:
                output[i] = 'G' + str(letter)
                checkWordDictionary[letter] -= 1
            i += 1
        
        #check for correct letters at incorrect position
        i = 0
        for letter in word:
            if letter in self.answer and letter != self.answer[i] and checkWordDictionary[letter] > 0:
                output[i] = 'Y' + str(letter)
                checkWordDictionary[letter] -= 1
            i += 1
        
        #fill in remaining wrong letters
        i = 0
        for letter in output:
            if letter == '':
                output[i] = 'R' + str(word[i])
            i += 1

        #reset dictionary to initial values
        self.resetDict()
        
        return output
    
    def checkWin(self,word):
        if word == self.answer:
            return True
   
    def getAns(self):
        return self.answer
    
    def getDict(self):
        return self.dictionary
    
    def resetDict(self):
        self.dictionary = {}
        for letter in self.answer:
            if letter not in self.dictionary:
                self.dictionary[letter] = 1
            else:
                self.dictionary[letter] += 1

def checkUser(user_id):
  if str(user_id) in db.keys():
    return True
  else:
    return False

def checkWordExists(word):
  checklist = []
  f = open('wordle-allowed-guesses.txt','r')
  for line in f:
    checklist.append(line.strip().upper())
  f.close()
  
  if word in checklist:
    return True
  else:
    return False

def deleteAllKeys(): # --> only for testing
  for key in db.keys():
    del db[key]

def answer():
  word_list = []
  
  f = open('wordle-answers-alphabetical.txt','r')
  for line in f:
    word_list.append(line.strip())
  f.close()
  
  chosenWord = random.choice(word_list).upper()

  return chosenWord

def emojiDisplay(array):
  result = ''
  for data in array:
    if data[0] == 'G':
      result += emojiDict.get(data)
    elif data[0] == 'Y':
      result += emojiDict.get(data)
    elif data[0] == 'R':
      result += emojiDict.get(data)
    elif data[0] == 'B':
      result += emojiDict.get(data)
  return result

def newKeyboardState(curr_keyboard,array):
  for data in array:
    found = False
    if data[0] == 'G':
      for row in range(len(curr_keyboard)):
        for key in range(len(curr_keyboard[row])):
          if curr_keyboard[row][key][1] == data[1]:
            curr_keyboard[row][key] = 'G' + curr_keyboard[row][key][1]
            found = True
            break
        if found == True:
          break
    elif data[0] == 'R':
      for row in range(len(curr_keyboard)):
        for key in range(len(curr_keyboard[row])):
          if curr_keyboard[row][key][1] == data[1]:
            if curr_keyboard[row][key][0] == 'B':
              curr_keyboard[row][key] = 'R' + curr_keyboard[row][key][1]
              found = True
            break
        if found == True:
          break
    elif data[0] == 'Y':
      for row in range(len(curr_keyboard)):
        for key in range(len(curr_keyboard[row])):
          if curr_keyboard[row][key][1] == data[1]:
            if curr_keyboard[row][key][0] != 'G' and curr_keyboard[row][key][0] != 'Y':
              curr_keyboard[row][key] = 'Y' + curr_keyboard[row][key][1]
              found = True
            break
        if found == True:
          break
  
  return curr_keyboard

def newKeyboardDisplay(curr_keyboard):
  display = ''
  i = 0
  for row in curr_keyboard:
    if i == 1:
      display += i*7*' ' + emojiDisplay(row) + '\n'
    elif i == 2:
      display += i*12*' ' + emojiDisplay(row) + '\n'
    else:
      display += emojiDisplay(row) + '\n'
    i += 1

  return display

default_keyboard = [
                    ['BQ','BW','BE','BR','BT','BY','BU','BI','BO','BP'],
                    ['BA','BS','BD','BF','BG','BH','BJ','BK','BL'],
                    ['BZ','BX','BC','BV','BB','BN','BM']
                   ]

# def updateDB():
#   for key in db.keys():
#     value = db[key]
#     value[1] = 0
#     value[2] = ''
#     value[9] = default_keyboard
#     if key == '368244543998656512':
#       value[5] = 170
#       value[4] = 34
#       value[3] = 37

# updateDB()

@client.event
async def on_ready():
  print("Logged in as {0.user}".format(client))
  await client.change_presence(activity=discord.Game(name="Type !whelp to view commands!"))
  #deleteAllKeys() #-> for debugging

@client.event

async def on_message(message):
  if message.author == client.user:
    return
  
  if message.content.startswith('!w'):
    user_id = message.author.id
    if checkUser(user_id) == False:
      wordle_answer = answer()
      challenge_word = answer()
      attempts = 0
      output = ''
      totalGames = 0
      wins = 0
      totalGuesses = 0
      exp = 0
      streak = 0 
      keyboard = default_keyboard
      db[str(user_id)] = [wordle_answer,attempts,output,totalGames,wins,totalGuesses,exp,challenge_word,streak,keyboard]
  
  if message.content.startswith('!wplay'):

    #print(checkPlaying(user_id)) #--> check for debugging

    game = Wordle((db[str(user_id)])[0])
    attempts = (db[str(user_id)])[1]
    exp_gain = 0
    
    curr_keyboard = (db[str(user_id)])[9]
    #print(curr_keyboard)

    if len(message.content.split()) == 2:
      word = (message.content.split())[1].upper()
    
      #--> check if word is 5 letters and is valid

      if len(word) == 5 and checkWordExists(word) == True:
        db[str(user_id)][9] = newKeyboardState(curr_keyboard,game.checkWord(word))

        (db[str(user_id)])[2] += emojiDisplay(game.checkWord(word)) + '\n'
        output = db[str(user_id)][2]
        
        #give extra exp for using challenge word
        if word == (db[str(user_id)])[7]:
          (db[str(user_id)])[6] += 100
          (db[str(user_id)])[7] = answer()
          await message.channel.send(f'You gained an extra 100 EXP for using the word {word}!')
          

        embedMsg = discord.Embed(title = "Playing Wordle...", description = f'Enter a 5 letter word! You have {5-attempts} attempts left!\nUse the word {(db[str(user_id)])[7]} for bonus EXP!\n\n{output}', color=0x48b400)
        embedMsg.add_field(name = "Keyboard", value = f'Letters Used:\n{newKeyboardDisplay(curr_keyboard)}', inline = False)
        await message.reply(embed=embedMsg)

        #incrementing attempt counter by 1
        (db[str(user_id)])[1] += 1
        (db[str(user_id)])[5] += 1
        
        if game.checkWin(word) == True:
          if attempts == 0:
            exp_gain = int(15000 * (-1/(db[str(user_id)][8]+2)+1.5))
            await message.reply(f'💸 JACKPOT!!! 💸')
          else:
            exp_gain = int(4000/(2**(attempts)) * (-1/(db[str(user_id)][8]+2)+1.5))
          
          (db[str(user_id)])[6] += exp_gain
          db[str(user_id)][8] += 1
          await message.reply(f'You WON in {attempts+1} attempts! 🎉🥳🎉\nYou won {exp_gain} EXP!\nYour win streak is now {db[str(user_id)][8]}!')
          
          #increase total games by 1
          (db[str(user_id)])[3] += 1
          (db[str(user_id)])[4] += 1

          (db[str(user_id)])[9] = default_keyboard
          (db[str(user_id)])[0] = answer()
          (db[str(user_id)])[1] = 0
          (db[str(user_id)])[2] = ''
        
        elif attempts == 5:
          if (db[str(user_id)])[6] < 600:
            (db[str(user_id)])[6] = 0
          else:
            (db[str(user_id)])[6] -= 600
          
          db[str(user_id)][8] = 0
          await message.reply(f'You LOST! 😔 Word is {(db[str(user_id)])[0]}!\nYou lost 600 EXP!\nYour win streak is now {db[str(user_id)][8]}!')

          #increase total games by 1
          (db[str(user_id)])[3] += 1

          (db[str(user_id)])[9] = default_keyboard
          (db[str(user_id)])[0] = answer()
          (db[str(user_id)])[1] = 0
          (db[str(user_id)])[2] = ''
      
      elif len(word) != 5:
        await message.reply('Word MUST have 5 letters!')
      else:
        await message.reply('Word you entered is not a valid word!')
    
  if message.content.startswith('!wstats'):

    totalGames = (db[str(user_id)])[3]
    wins = (db[str(user_id)])[4]
    totalGuesses = (db[str(user_id)])[5]
    exp = int((db[str(user_id)])[6])
    streak = db[str(user_id)][8]
    
    if totalGames != 0: 
      avgGuesses = round(totalGuesses/totalGames,2)
    else:
      avgGuesses = 0

    #getting users profile picture
    pfp = message.author.avatar_url

    userList = db.keys()
    
    serverList = []
    
    server_id = message.guild.id
    server = client.get_guild(server_id)
    
    #implementing server leaderboard
    
    leaderboardSize = 5
    scores = []
    leaderboard = [''] * leaderboardSize
    winexp_list = [''] * leaderboardSize
    avgGuesses_list = [''] * leaderboardSize
    serverUserLeaderboardString = ''
    serverWinsExpLeaderboardString = ''
    serverAvgGuessLeaderboardString = ''
    
    for member in server.members:
      memberID = str(member.id)
      if memberID in userList:
        serverList.append(memberID)
        
    for key in serverList:
      scores.append((key,db[key][6]))
    
    # #array of scores
    # #use index 3,4 and 5 => totalGames,wins,totalGuesses
    scores.sort(key=lambda x:x[1],reverse = True)

    leaderboardPos = scores.index((str(user_id),db[str(user_id)][6])) + 1

    if leaderboardPos > 3:
      leaderboardPos = '#' + str(leaderboardPos)
    elif leaderboardPos == 1:
      leaderboardPos = '🥇 #' + str(leaderboardPos)
    elif leaderboardPos == 2:
      leaderboardPos = '🥈 #' + str(leaderboardPos)
    elif leaderboardPos == 3:
      leaderboardPos = '🥉 #' + str(leaderboardPos)
    
    for i in range(leaderboardSize):
      if len(scores) != 0:
        #print(db.keys())
        
        key = scores[0][0]
        
        username = str(await client.fetch_user(key))
        if len(username) > 17:
          username = username[0:8] + '...' + username[len(username)-5:len(username)+1]
        
        leaderboard[i] = f'{i+1}. {username}\n'
        winexp_list[i] = f' {int(db[key][6])} EXP | {db[key][4]} Wins \n'
        if db[key][3] != 0:
          avgGuesses_list[i] = f' {round((db[key][5]/db[key][3]),2)} \n'
        else:
          avgGuesses_list[i] = ''

        scores.pop(0)
      
      else:    
        break
      
    i = 1
    for data in leaderboard:
      if data == '':
        data = f'{i}. None\n'
      serverUserLeaderboardString += data
      i += 1

    for data in winexp_list:
      if data == '':
        data = f' None \n'
      serverWinsExpLeaderboardString += data

    for data in avgGuesses_list:
      if data == '':
        data = f' None \n'
      serverAvgGuessLeaderboardString += data

    #check latency
    #latency = client.latency
    #await message.channel.send(f'debug={latency*1000}ms')
      
    embedMsg = discord.Embed(title = f"{message.author}'s Wordle Stats 📈", description = f'Total Games: {totalGames}\nTotal Wins: {wins}\nWin Streak: {streak} `(+{round((-1/(streak+2)+0.5)*100,2)}% EXP Bonus)`\nAverage No. Of Guesses: {avgGuesses}\nEXP: {exp}\nLeaderboard Position: {leaderboardPos}', color=0x48b400)
    embedMsg.add_field(name = "Server Leaderboard 🏆", value = f'Top {leaderboardSize} people in the server ranked based on EXP!', inline = False)
    embedMsg.add_field(name = "User", value = f'{serverUserLeaderboardString}', inline = True)
    embedMsg.add_field(name = "EXP | Wins", value = f'`{serverWinsExpLeaderboardString}`', inline = True)
    embedMsg.add_field(name = "Avg. No. of Guesses", value = f'`{serverAvgGuessLeaderboardString}`', inline = True)
    
    embedMsg.set_thumbnail(url=pfp)
    await message.reply(embed=embedMsg)
    

  if message.content.startswith('!whelp'):

    #text to display for how to play wordle
    howToPlayText = 'Guess the WORDLE in six tries.\n\nEach guess must be a valid five-letter word.\nAfter each guess, the color of the tiles will change to show how close your guess was to the word.\n\n<:wordle_green_w:981415135874797648> means that the letter (in this case, the letter W) is in the word and is in the correct spot.\n\n<:wordle_yellow_o:981429169198104646> means that the letter (in this case, the letter O) is in the word but is in the wrong spot.\n\n<:wordle_black_r:981439988312965190> means that the letter (in this case, the letter R) is NOT in the word.'

    embedMsg = discord.Embed(title = "Wordle Help ❓", description = 'Bot has the commands below...\n`!wplay [*insert your word*]` -> To play Wordle\n`!wstats` -> To review your stats\n`!whelp` -> To view all bot commands\n`!wquit` -> To quit out of your Wordle Game', color=0x48b400)
    embedMsg.add_field(name = "How to play Wordle: ", value = howToPlayText, inline = False)
    await message.reply(embed=embedMsg)
    
  elif message.content.startswith('!wquit'):
    if (db[str(user_id)])[1] == 0:
      await message.reply('You are currently not playing in a Wordle game!')
    else:
      (db[str(user_id)])[1] = 0
      (db[str(user_id)])[2] = ''
      #increase total games by 1
      #(db[str(user_id)])[3] += 1

      if (db[str(user_id)])[6] < 600:
        (db[str(user_id)])[6] = 0
      else:
        (db[str(user_id)])[6] -= 600
      
      db[str(user_id)][8] = 0
      
      await message.reply(f'Quitted out of wordle game! Word is {db[str(user_id)][0]}!\nYou lost 600 EXP!\nYour win streak is now 0!')

      (db[str(user_id)])[0] = answer()
      
keep_alive()
client.run(os.environ['TOKEN'])