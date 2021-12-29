import random

rounds = 2
numberOfPlayers = 3
word = ""
builtWord = ""
wordSolved = False
playerCash = [0] * numberOfPlayers
wheel = (100, 150, 200, 250, 300, 350, 400, 450, 500, 550, 600, 650, 700, 750, 800, 850, 900, "Lose a Turn", "Bankrupt")
global consonants, vowels
consonants = ('B', 'C', 'D', 'F', 'G', 'H', 'J', 'K', 'L', 'M', 'N', 'P', 'Q', 'R', 'S', 'T', 'V', 'W', 'X', 'Y', 'Z')
vowels = ('A', 'E', 'I', 'O', 'U')
#Path for words.txt file
userDefinedPath = "C:\\Users\\Qwerty\\Desktop\\words.csv"

def generateWord(userDefinedPath):
    f = open(userDefinedPath)
    words = f.read()
    words = words.split("\n")
    word = random.choice(words)
    word = word.upper()
    return word

def attemptSolve(word):
    word = str(word).strip().upper()
    isCorrect = False
    userInput = input("Input your guess: ")
    userInput = str(userInput).strip().upper()
    if userInput == word:
        isCorrect = True
    return isCorrect

def validateGuess(word, builtWord, userInput):
    word = str(word).strip().upper()
    userInput = str(userInput).strip().upper()
    listWord = list(builtWord.replace(" ", ""))
    foundMatch = False
    for i in range(len(listWord)):
        if listWord[i] == "_" and word[i] == userInput:
            listWord[i] = userInput
            foundMatch = True
    return foundMatch

def buildWord(word, builtWord, userInput):
    word = str(word).strip().upper()
    userInput = str(userInput).strip().upper()
    listWord = list(builtWord.replace(" ", ""))
    for i in range(len(listWord)):
        if listWord[i] == "_" and word[i] == userInput:
            listWord[i] = userInput
    return " ".join(listWord)

def checkTypeOfLetterLeft(word, builtWord):
    vowelsLeft = False
    consonantsLeft = False
    builtWord = str(builtWord).replace(" ", "")
    for i in range(len(builtWord)):
        if builtWord[i] == "_":
            if str(word[i]).upper() in consonants:
                consonantsLeft = True
            elif str(word[i]).upper() in vowels:
                vowelsLeft = True
    return (vowelsLeft, consonantsLeft)

def guessVowel(word, builtWord):
    playerCash[i] -= 250
    inputValid = False
    while inputValid == False:
        userInput = input("Guess a vowel: ")
        userInput = str(userInput).strip().upper()[:1]
        if userInput in vowels:
            inputValid = True
            if validateGuess(word, builtWord, userInput) == True:
                builtWord = buildWord(word, builtWord, userInput)
                print("Your guess was found in the word.")
                print("Word solved to this point: " + str(" ".join(builtWord)) + "\n")
            else:
                print("Your guess wasn't in the word.")
                guessAVowel = False   
        else:
            print(str(userInput) + " isn't a vowel. Try again.")
    return builtWord

for r  in range(rounds):
    # Initialize round
    print("\nRound " + str(r + 1))
    word = generateWord(userDefinedPath)
    builtWord = "_" * len(word)
    print("\nFor ease of debugging, the word is " + str(word))
    while wordSolved == False:
        # i-th player's turn
        for i in range(numberOfPlayers):
            #Check if word is solved to skip succeeding player turns when a previous player has solved it
            if wordSolved == False:
                print("Word solved to this point: " + str(" ".join(builtWord)) + "\n")
                print("Player " + str(i + 1) + "'s turn:")
                spin = wheel[random.randrange(0, len(wheel))]
                print("Player " + str(i + 1) + "'s spin = " + str(spin))
                # Bankrupt and turn over
                if spin == "Bankrupt":
                    playerCash[i] = 0
                    print("You lose all your money.")
                # Spun 'lose a turn' and turn is now over
                elif spin == "Lose a Turn":
                    print("You lost your turn.")
                # All other spins
                else:
                    userInput = input("Would you like to solve (S) or guess a letter (L)? ")
                    userInput = userInput.strip().upper()[:1]
                    # Player attempts to solve
                    if userInput == "S":
                        if attemptSolve(word):
                            #This player solved the word and the round is over
                            print ("You guessed the word correctly. You add " + str(spin) + " to your cash total.")
                            playerCash[i] += spin
                            print("Player " + str(i + 1) + "'s cash total is now $" + str(playerCash[i]))
                            wordSolved = True
                        else:
                            print("Your guess was wrong. No cash rewarded.")
                    #Take all other input as a decision to guess a letter
                    else:
                        # Check if there's any consonants left to guess. If not, only ask for vowels. 
                        if checkTypeOfLetterLeft(word, builtWord) == (True, False):
                            print("There are only vowels left.")
                            if playerCash[i] >= 250:
                                userInput = input("Would you like to buy a vowel for $250? (Y/N) ")
                                userInput = str(userInput).strip().upper()[:1]
                                if userInput == "Y":
                                    temp = guessVowel(word, builtWord)
                                    # if the word you built with the vowel guess completes the word, it is solved
                                    if str(word).upper() == str(temp.replace(" ", "").upper()):
                                        print("Word is solved.")
                                        wordSolved = True
                                        guessAVowel = False
                                    # Else if the word after the vowel guess is the same as it was before, then the guess was wrong
                                    elif builtWord == temp:
                                        print("Your guess wasn't in the word.")  
                                        guessAVowel = False
                            else:
                                print("You don't have enough cash to buy a vowel.")
                        else:
                            # Guess a consonant
                            inputValid = False
                            while inputValid == False:
                                userInput = input("Guess a consonant: ")
                                userInput = str(userInput).strip().upper()[:1]
                                if userInput in consonants:
                                    inputValid = True
                                    if validateGuess(word, builtWord, userInput):
                                        builtWord = buildWord(word, builtWord, userInput)
                                        playerCash[i] += spin
                                        print("Your guess was found in the word.")
                                        print("Word solved to this point: " + str(" ".join(builtWord)) + "\n")
                                        print("You add " + str(spin) + " to your cash total.")
                                        print("Player " + str(i + 1) + "'s cash total is $" + str(playerCash[i]))
                                        #print("word = " + str(word) + ", builtword = " + str(builtWord.replace(" ", "")))
                                        if str(word).upper() == str(builtWord.replace(" ", "").upper()):
                                            print("Word is solved.")
                                            wordSolved = True
                                            break
                                        # Guess a vowel. If there are no vowels to guess, turn off vowel guessing.
                                        if checkTypeOfLetterLeft(word, builtWord) == (False, True):
                                            guessAVowel = False
                                        else:
                                            guessAVowel = True
                                        while guessAVowel:
                                            if playerCash[i] >= 250:
                                                userInput = input("Would you like to buy a vowel for $250? (Y/N) ")
                                                userInput = str(userInput).strip().upper()[:1]
                                                if userInput == "Y":
                                                    temp = guessVowel(word, builtWord)
                                                    # if the word you built with the vowel guess completes the word, it is solved
                                                    if str(word).upper() == str(temp.replace(" ", "").upper()):
                                                        print("Word is solved.")
                                                        wordSolved = True
                                                        guessAVowel = False
                                                    # Else if the word after the vowel guess is the same as it was before, then the guess was wrong
                                                    elif builtWord == temp:
                                                        guessAVowel = False
                                                        break
                                                    else:
                                                        builtWord = temp
                                                    # Check to see if there's vowels left after this instance of vowel guessing. If not, then disallow future vowel guessing this turn.
                                                    if checkTypeOfLetterLeft(word, builtWord) == (False, True):
                                                        guessAVowel = False
                                                        print("There are no vowels left.")
                                                else:
                                                    guessAVowel = False
                                            else:
                                                guessAVowel = False
                                                print("You don't have enough money to buy a vowel.")
                                    else:
                                        print("Your guess wasn't in the word. You get no money.")       
                                else:
                                    print(str(userInput) + " isn't a consonant. Try again.")
                    print("Turn over.\n")
        print("Player cash totals so far:")
        for i in range(numberOfPlayers):
            print("Player " + str(i  + 1) + ": " + str(playerCash[i]))
    print("Round " + str(r + 1) + " over\n")
    # For the next round
    wordSolved = False

#Final round
# Get index with largest value for playeCash
print("\nFinal round.\n")
word = generateWord(userDefinedPath)
print("\nFor ease of debugging, the word is " + str(word))
builtWord = "_" * len(word)
finalRoundGuessList = []
for i in range(len(playerCash)):
    highest = 0
    if playerCash[i] > playerCash[highest]:
        highest = i
print("Player " + str(highest + 1) + " has the highest cash value and will advance to the final round.")
print("Adding R-S-T-L-N-E to word: ")
builtWord = buildWord(word, builtWord, "R")
builtWord = buildWord(word, builtWord, "S")
builtWord = buildWord(word, builtWord, "T")
builtWord = buildWord(word, builtWord, "L")
builtWord = buildWord(word, builtWord, "N")
builtWord = buildWord(word, builtWord, "E")
print("Word solved to this point: " + str(" ".join(builtWord)) + "\n")

print("Player " + str(highest + 1) + ", choose three consonants: ")
for i in range(3):
    inputValid = False
    while inputValid == False:
        userInput = input("Input value for consonant " + str(i + 1) + ": ")
        print("user input = " + str(userInput))
        if str(userInput).strip().upper()[:1] in consonants:
            inputValid = True
        else:
            print("That's not a consonant. Try again.")
            inputValid = False
    finalRoundGuessList.append(str(userInput).strip().upper()[:1])
print("Player " + str(highest + 1) + ", choose one vowel: ")
inputValid = False
while inputValid == False:
    userInput = input("Input value for vowel " + str(i + 1) + ": ")
    if str(userInput).strip().upper()[:1] in vowels:
        inputValid = True
    else:
        print("That's not a vowel. Try again.")
        inputValid = False
       
finalRoundGuessList.append(str(userInput).strip().upper()[:1])
# Build word with supplied guesses
for i in range(len(finalRoundGuessList)):
    builtWord = buildWord(word, builtWord, finalRoundGuessList[i])
print("Word solved to this point: " + str(" ".join(builtWord)) + "\n")
if attemptSolve(word):
    print ("You guessed the word correctly. You won the final round and get a whole dollar as compensation. You add $1 to your cash total.")
    playerCash[highest] += 1
    print("Player " + str(highest + 1) + "'s cash total is now $" + str(playerCash[highest]))
else:
    print("Your guess was wrong. No cash rewarded.")
print("Overal total for cash per player: ")
for i in range(len(playerCash)):
    print("Player " + str(i + 1) + " $" + str(playerCash[i]))
print("Game over")

