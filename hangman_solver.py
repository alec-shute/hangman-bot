import string

#Loads the dictionary that will be used for the game
file_path = "words_alpha.txt"
with open(file_path, 'r') as file:
    unsorted_words = [line.strip() for line in file.readlines()]

#partition words based on length
words = dict([(i,[word for word in unsorted_words if len(word) == i]) for i in range(1,32)])

#A letter frequency analysis function

def freq(lst, letters = None):
    if letters == None:
        letters = list(string.ascii_lowercase)
    return dict([(letter, len([word for word in lst if letter in word])/len(lst)*100) for letter in letters]) 

#finds the letter in a list of letters which is most likely to be contained in another list of words. Ties are decided at random
def max_freq(lst, letters =None):
    return max(freq(lst, letters), key=freq(lst).get)

def missing_letter(letter,lst):
    return [word for word in lst if letter not in word]

"""word candidate pruner function based on letter positions (i.e. a crossword solver)
takes as input the length of the word and string 'hints' of the form '_t_d_w__' for example,
and a list of candidate words (default all words of length i).
outputs updated list of candidates based on hints."""

def crossword(hints, cands=None):
    i=len(hints)
    if cands ==None:
        cands = words[i]
    for j in range(0,i):
        if hints[j] != '_':
            cands = [word for word in cands if word[j]==hints[j]]
    return cands

#And now for the hangman game!

def play_hangman():

    try:
        i = int(input("Welcome to hangman! Pick your word and I'll try to guess it. Start by telling me how many letters your word has: "))

    except ValueError:
        print("Please enter a valid number.")
        i = int(input("Welcome to hangman! Pick your word and I'll try to guess it. Start by telling me how many letters your word has: "))
    

    letters = list(string.ascii_lowercase)
    cands = words[i]
    guess_counter = 0
    lives_counter = 0
    
    while True:
        guess_counter +=1
        if not cands:
            print("Good game! Unfortunately the word you were thinking of isn't in my database")
            return 
        
        guess = max_freq(cands, letters)
        letters.remove(guess)
        
        if guess_counter == 1:
            clue = input("Cool! I found {} words of length {} in my database. \n \
            Let's start narrowing it down. My first guess is {}. \n \
            Rules: If my guess is not in your word, type 'No'.\n \
            If my guess is in your word, type all instances of that letter and everywhere else, use underscores, for example '_a__a___'  \n".format(len(cands),i, guess))
            if clue == 'No':
                lives_counter +=1
                cands = missing_letter(guess, cands)
            else:
                cands = crossword(clue, cands)
        
        elif len(cands) == 1:
            verdict = input("I think your word is '{}'. Am I right? (Type 'Yes' or 'No') \n".format(cands[0]))
            if verdict == "Yes":
                print("Good game! It cost me {} lives to find your word '{}'.".format(lives_counter, cands[0]))
                return
            else:
                print("Good game! Unfortunately the word you were thinking of isn't in my database")
                return
                
        else:
            clue = input("{} candidates remaining. My next guess is {}. \n".format(len(cands), guess))
        
            if clue == 'No':
                lives_counter +=1
                cands = missing_letter(guess, cands)
        
            elif "_" not in clue and clue in cands:
                print("Good game! It cost me {} lives to find your word '{}'.".format(lives_counter, clue))
                return

#Some test cases for the functions

#print(unsorted_words[0:100])
#freqs(words[7],['a','c','e'])  
#max_freq(words[8],['f','j','z'])
#max_freq(['ab','hg','rf','er','bv','ac','az'])
#crossword('__l___s_d')

play_hangman()
