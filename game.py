import random
from emote_dictionary import emojiDict

class Wordle:
    def __init__(self,answer):
        self.answer = answer
        self.dictionary = {}
        for letter in answer:
            if letter not in self.dictionary:
                self.dictionary[letter] = 1
            else:
                self.dictionary[letter] += 1
    
    def answer():
      word_list = []
    
      f = open('wordle-answers-alphabetical.txt','r')
      for line in f:
        word_list.append(line.strip())
      f.close()
    
      chosenWord = random.choice(word_list).upper()
  
      return chosenWord
    
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

class Keyboard:
    def __init__(self):
      self.default_keyboard =  [
                                ['BQ','BW','BE','BR','BT','BY','BU','BI','BO','BP'],
                                ['BA','BS','BD','BF','BG','BH','BJ','BK','BL'],
                                ['BZ','BX','BC','BV','BB','BN','BM']
                               ]
      
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
          display += i*7*' ' + Wordle.emojiDisplay(row) + '\n'
        elif i == 2:
          display += i*12*' ' + Wordle.emojiDisplay(row) + '\n'
        else:
          display += Wordle.emojiDisplay(row) + '\n'
        i += 1
    
      return display