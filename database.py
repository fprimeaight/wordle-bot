from replit import db 
import game

def get_users():
  return db.keys()
  
def checkUser(user_id):
  if str(user_id) in db.keys():
    return True
  else:
    return False

def createUser(user_id):
  wordle_answer = game.answer()
  challenge_word = game.answer()
  attempts = 0
  output = ''
  totalGames = 0
  wins = 0
  totalGuesses = 0
  exp = 0
  streak = 0 
  keyboard = game.Keyboard().default_keyboard
  isPlaying = True
  db[str(user_id)] = [wordle_answer,attempts,output,totalGames,wins,totalGuesses,exp,challenge_word,streak,keyboard,isPlaying]

def get_answer(user_id):
  return db[str(user_id)][0]

def reset_answer(user_id): 
  db[str(user_id)][0] = game.answer()

def get_attempts(user_id):
  return db[str(user_id)][1]

def set_attempts(user_id,tries):
  db[str(user_id)][1] = tries

def get_output(user_id):
  return db[str(user_id)][2]

def set_output(user_id,string):
  db[str(user_id)][2] += string

def reset_output(user_id):
  db[str(user_id)][2] = ''

def get_challenge_word(user_id):
  return db[str(user_id)][7]

def reset_challenge_word(user_id):
  db[str(user_id)][7] = game.answer()

def set_keyboard(user_id,new_keyboard):
  db[str(user_id)][9] = new_keyboard
  
def get_keyboard(user_id):
  return db[str(user_id)][9]

def reset_keyboard(user_id):
  db[str(user_id)][9] = game.Keyboard().default_keyboard

def set_totalGames(user_id,new_totalGames):
  db[str(user_id)][3] = new_totalGames

def get_totalGames(user_id):
  return db[str(user_id)][3]

def set_wins(user_id,new_wins):
  db[str(user_id)][4] = new_wins

def get_wins(user_id):
  return db[str(user_id)][4]

def set_totalGuesses(user_id,guess):
  db[str(user_id)][5] = guess

def get_totalGuesses(user_id):
  return db[str(user_id)][5]

def gain_exp(user_id,new_exp):
  db[str(user_id)][6] += int(new_exp)
  
def get_exp(user_id):
  return int(db[str(user_id)][6])

def set_streak(user_id,new_streak):
  db[str(user_id)][8] = new_streak
  
def get_streak(user_id):
  return db[str(user_id)][8]

def set_isPlaying(user_id,value):
  db[str(user_id)][10] = value
  
def get_isPlaying(user_id):
  return db[str(user_id)][10]