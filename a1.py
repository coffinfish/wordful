# This python program solves the problem of wanting to play wordle more than once a day, you get to play as many times as you want (And, without wifi!). 
# Thus, the name of this game is called: Wordful.
# You can play as many times as you want, and at the end it will tell you the total # of games you played, your winrate, and your guess distribution.
# While playing, it also replicates the real wordle and it will show you the list of letters that you have gotten in the right position, letters that are in the wrong position, or letters that aren't in the word.

# Important Note: words.txt should be in the same folder as a1.py because this code cannot run without it. "words.txt" is a txt file with every 5 letter word.
# Cindy H
# ID: 501184805


#Custom Class of text colors
# ATTENTION!: In Python IDLE, instead of outputting colour it will output "\033[xxm" (where x is the responding ANSI value). In Spyder, there will be no colour or any "\033m[xxm". This works best in Visual Studio Code.
class wordleUI():
    # if I use this reset it will reset the font colour and style.
    reset = "\033[0m"
    # This returns the string in bright green
    def correctPos(string = ""):
        return (f"\033[1;32m{string}")
    # This returns the string in gray
    def empty(string = ""):
        return (f"\033[0;37m{string}")
    # This returns the string in light gray
    def usedLetter(string = ""):
        return (f"\033[1;90m{string}")
    # This returns the string in yellow
    def incorrectpos(string = ""):
        return (f"\033[1;33m{string}")
    # This returns the string in magenta
    def text(string = ""):
        return (f"\033[0;4;35m{string}")
    # This returns the string in turquoise
    def title(string = ""):
        return(f"\033[1;36m{string}")
    # This returns the string in bright red
    def error(string = ""):
        return (f"\033[1;31m{string}")
    # This returns the string in bright green
    def winner(string = ""):
        return(f"\033[1;32m{string}")
    

# Importing choice from random because I only need to use that one function:
from random import choice

# This function will check if the player input is valid or not. In order for the player input to be valid, it must be a 5 letter word. So, if it is in the words.txt, it is a valid guess.
def isValid(playerInput = ""):
    #Default return value is False
    result = False
    # This opens up the text file called "words.txt", it will join the two lines together. The first line consists of words that are used as the answer, while the second line consists of acceptable answers. By combining the two, I can get the full list of acceptable inputs.
    with open('words.txt') as f:
        # " ".join will join the two lines (there are only two lines in word.txt) using a " ". The line.strip("\n") gets rid of the newline character between end of line 1 and start of line 2. Then, since all the words are separated by one space, split(" ") puts it into a list with " " as the separator.
        listOfWords = " ".join(line.strip("\n") for line in f).split(" ")
    # If the playerinput is in the list of words, then the result is valid and it changes it to true. If not, then result will stay False.
    if (playerInput in listOfWords):
        result = True
    # Return the result
    return(result)

# This function will check the input of the player, and returns a list of the correct letters in the right places + correct letters in the wrong places.
def checkWord(correctWord, playerWord):
    # This turns the playerWord and the correctWord into their own lists
    pwList = [c for c in playerWord]
    cwList = [c for c in correctWord]
    # For each index in pwList
    for i in range(len(pwList)):
        # First, we check for correct character in the correct position
        if pwList[i] == cwList[i]:
            # If it is, then in pwList, update that character to become green
            pwList[i] = wordleUI.correctPos(pwList[i])
            # In cwList, replace it with an empty string so another check is not done.
            # I do this because, for example, if the correct word was "balls" and the person guessed "aware", this will cause both "a"s in "aware" to be checked against the one "a" in "balls", when we really only want to check one since the correct word only has one "a"
            cwList[i] = ""
    # For each index in pwList, after all the correct letters have been checked.
    for i in range(len(pwList)):
        # I do this check because I want to make sure it doesn't have the \033[92m in front of it (which means its a correct letter so no need to update it)
        if ("a" <= pwList[i] <= "z"):
            # If that character from pwList is in cwList, it has to be in the wrong position.
            if pwList[i] in cwList:
                # I change cwList first because once I update pwList[i] to become yellow, I can no longer find it in cwList using .index.
                cwList[cwList.index(pwList[i])] = ""
                # Make the character yellow.
                pwList[i] = wordleUI.incorrectpos(pwList[i])
            # Else, make it gray 
            else:
                pwList[i] = wordleUI.usedLetter(pwList[i])
    # Return the updated list in the end
    return pwList

# This creates the letter list that I will use to display the used letters and unused letters
def createLetterList():
    # Creating a list of letters based on the qwerty layout, with each list within the list being a separate row on the keyboard.
    listOfLetters = [["q","w","e","r","t","y","u","i","o","p"],["a","s","d","f","g","h","j","k","l"],["z","x","c","v","b","n","m"]]
    # Accesses each element in listOfLetters and makes it light gray.
    for r in range(len(listOfLetters)):
        for c in range(len(listOfLetters[r])):
            listOfLetters[r][c] = wordleUI.empty(listOfLetters[r][c])
    # Returning the final list at the end.
    return listOfLetters

# This function updates the letter list to display the correct colour, it takes in pwList, which is the list of the playerword already coloured from checkWord(), and the listOfLetters.
def updateLetterList(pwList, listOfLetters):
    # The two for statements will access each element in listOfLetters
    for r in range(len(listOfLetters)):
        for c in range(len(listOfLetters[r])):
            # For each string in the pwList
            for char in pwList:
                # If the last character in the string from pwList (remember, it has \033[xxm in front) is equal to the last character in listOfLetters.
                # and if the string from listOfLetters apart from the last character (so, the "\033[xxm" part) is not equal to wordleUI.correctPos() (which will return just the string that makes the string green, since the default value is an empty string)
                # I do the second check because if there are two of the same letter and one is in the right spot while the other one isn't, I still want the keyboard to display green and not yellow.
                if (char[-1:] == listOfLetters[r][c][-1:]) and (listOfLetters[r][c][:-1] != wordleUI.correctPos()):
                    # updating that position by taking the colour from the pwList, and the letter from listOfLetters.
                    listOfLetters[r][c] = char[:len(char)-1] + listOfLetters[r][c][-1:]
    # Because I update the index itself and lists are mutable, I do not need to return the listOfLetters. 
    
def isCorrect(correctWord, playerWord):
    # Checks if the word is corect, returns True if it is and False if it isn't. I put it in a function so the one-line if wouldn't be confusing to read.
    return True if playerWord == correctWord else False

# This function will choose a random word from the words.txt
def chooseWord():
    myFile = open("words.txt", "r")
    # I only need to read the first line, because those are the words that are actually used as the answer in wordle. All words in the second line are just acceptable guesses.
    listOfWords = myFile.readline().split(" ")
    # return a random word from the listOfWords using random.choice, but since I only imported choice, I do not need to put random in front.
    return (choice(listOfWords))

# This function will print out the Rounds & the letterList
def printRound(listOfAllRounds, listOfLetters):
    for eachRound in listOfAllRounds:
        print(" ".join(eachRound))
    print()
    for eachRow in listOfLetters:
        print(" ".join(eachRow))

# This function will run in main
def main():
    # Initiating statistic variables
    play = "y"
    wins = 0
    losses = 0
    numOfGuesses = {
        "1":0,
        "2":0,
        "3":0,
        "4":0,
        "5":0,
        "6":0
    }
    print(wordleUI.title('Welcome to Wordful')+"\n"+wordleUI.title('The Wordle that you can play more than once!'))
    
    # Will keep playing the game while play == "y"
    while (play == "y"):
        # Declaring game variables
        correctWord = chooseWord()
        listOfAllRounds = [[wordleUI.usedLetter("_") for i in range(5)] for i in range(6)]
        listOfLetters = createLetterList()
        roundNum = 0
        
        # Will keep looping until 6 rounds have been played.
        while (roundNum < 6):
            printRound(listOfAllRounds, listOfLetters)
            
            # Getting the player word
            while True:
                # Keep getting an input until isValid returns true, which means the guess is valid, and breaks out of the loop
                playerWord = input(f"{wordleUI.text('Guess:')} {roundNum+1}:{wordleUI.reset} ").strip().lower()
                if (isValid(playerWord) == True):
                    break
                else:
                    print(wordleUI.error("Invalid Word, please try again"))
            # updating the listOfAllRounds at the index roundNum to the list returned from checkWord()
            listOfAllRounds[roundNum] = checkWord(correctWord, playerWord)
            # updating letterList (this shows the keyboard), no need to assign it to a variable because the list is mutable and I update the index itself.
            updateLetterList(listOfAllRounds[roundNum], listOfLetters)
            # If the playerword == correctword, break out of the loop.
            if isCorrect(correctWord, playerWord):
                break
            # update roundNum at the end of everything
            roundNum +=1
        # When the round loop is broken, it means current game is over, check whether roundNum is < 6, if it is, it means the player guessed the word within 6 tries (because roundNum starts at 0)
        if (roundNum < 6):
            # print You won, and add 1 to wins.
            print(wordleUI.winner("You won!")+wordleUI.reset)
            wins += 1
            # updates the dictionary value using the key
            numOfGuesses[str(roundNum+1)] += 1
        else:
            # the player loss, add one to losses.
            print(wordleUI.error("You lost!")+wordleUI.reset)
            losses +=1
        # Print out the final result of all the rounds, and print out the correct word as well.
        print(wordleUI.title("\nFinal Result:")+wordleUI.reset)
        printRound(listOfAllRounds, listOfLetters)
        print(wordleUI.title("The word was:"), correctWord)
        # Ask if the user wants to play again, if they type 'y', then the play loop continues. 
        while True:
            play = input(wordleUI.text("Play Again? (y/n)")+wordleUI.reset)
            if (play == "y" or play == "n"):
                break
            else:
                print(wordleUI.error("Please type 'y' for to continue playing or 'n' to quit."))
    
    # Printing the statistics
    print(wordleUI.title("\n\nStatistics:")+wordleUI.reset)
    winrate = round(wins/(wins + losses)*100,2)
    print(f"{wordleUI.text('Total Games:')}{wordleUI.reset} {wins+losses}\n{wordleUI.text('Winrate:')}{wordleUI.reset} {winrate}%")
    print(wordleUI.text("Guess Distribution:")+wordleUI.reset)
    for key,value in numOfGuesses.items():
        print(f"\t{key}: {value}")
if __name__ == "__main__":
    # calling main()
    main()