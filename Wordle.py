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