from replit import db 
import game

def checkUser(user_id):
  if str(user_id) in db.keys():
    return True
  else:
    return False

def createUser(user_id):
  wordle_answer = game.Wordle.answer()
  challenge_word = game.Wordle.answer()
  attempts = 0
  output = ''
  totalGames = 0
  wins = 0
  totalGuesses = 0
  exp = 0
  streak = 0 
  keyboard = game.Keyboard.default_keyboard
  db[str(user_id)] = [wordle_answer,attempts,output,totalGames,wins,totalGuesses,exp,challenge_word,streak,keyboard]

def get_answer(user_id):
  return db[str(user_id)][0]

def reset_answer(user_id): 
  db[str(user_id)][0] = game.Wordle.answer()

def get_attempts(user_id):
  return db[str(user_id)][0]

def reset_attempts(user_id):
  db[str(user_id)][1] = 0

def get_output(user_id):
  return db[str(user_id)][2]

def reset_output(user_id):
  db[str(user_id)][2] = ''

def get_challenge_word(user_id):
  return db[str(user_id)][7]

def reset_challenge_word(user_id):
  db[str(user_id)][7] = game.Wordle.answer()

def get_keyboard(user_id):
  return db[str(user_id)][9]

def reset_keyboard(user_id):
  db[str(user_id)][9] = game.Keyboard.default_keyboard