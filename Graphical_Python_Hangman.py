import sys, pygame, random
"""-----------------------------------------------------------------"""
def setupHangmanGlobals():   

    global g_TRIES #how many tries the player gets to guess the word
    g_TRIES = 6 

    global g_DICT_WORD #select random word ALSO needed for 'game over'
    g_DICT_WORD = list(random.choice(LINES))  

    global g_GUESSED_WORD #word the player sees
    g_GUESSED_WORD = []
    for i in range(0, len(g_DICT_WORD)):
        g_GUESSED_WORD.append('*') 

    global g_GUESSES_LIST #the incorrect guesses
    g_GUESSES_LIST = [] 

    global g_NUM_OF_BAD_GUESSES #counter for num of incorrect guesses
    g_NUM_OF_BAD_GUESSES = 0 
"""-----------------------------------------------------------------"""

"""-----------------------------------------------------------------"""
def preGameSetup():

    pygame.init()
    pygame.font.init()

    loadWords()

    size = (800, 600)
    
    global g_white #color definition for "white"
    g_white = (255, 255, 255)

    global g_black #color definition for "black"
    g_black = (0, 0, 0)

    global g_screen #screen that will have things rendered to it
    g_screen = pygame.display.set_mode(size)

    pygame.display.set_caption("Hangman")

    global g_comicSansFont #main font for the screen text
    g_comicSansFont = pygame.font.SysFont("Comic Sans MS", 30)

    global g_screenText #helper that renders certain text to the screen when needed
    g_screenText = {"greeting" :  g_comicSansFont.render, "enter" : g_comicSansFont.render, "word selected" : g_comicSansFont.render, 
                    "word to guess" : g_comicSansFont.render, "wrong letters" : g_comicSansFont.render, "guess letter" : g_comicSansFont.render,
                    "win message" : g_comicSansFont.render, "lose message" : g_comicSansFont.render, "play again" : g_comicSansFont.render,}
"""-----------------------------------------------------------------"""

"""-----------------------------------------------------------------"""
def setFlags(firstTime):
    global g_welcomeFlag #puts player at welcomeStage()
    global g_playFlag #puts player at gameSetupStage()

    if firstTime:
        g_welcomeFlag = True
        g_playFlag = False

    else:
        g_welcomeFlag = False
        g_playFlag = True
    
    global g_setupGameGlobalsFlag #only done once during gameSetupStage() to initialize all the hangman global variables
    g_setupGameGlobalsFlag = True

    global g_hangmanFlag #puts player at hangmanStage()
    g_hangmanFlag = False

    global g_playAgainFlag
    g_playAgainFlag = False
"""-----------------------------------------------------------------"""

"""-----------------------------------------------------------------"""
def loadWords():

    global LINES #a list of all the possible hangman words

    LINES = open("Master_Word_List.txt").readlines()

    LINES = [word.lower().rstrip("\n") for word in LINES]
"""-----------------------------------------------------------------"""

"""-----------------------------------------------------------------"""
def gameSetupStage(event):
    global g_playFlag
    global g_hangmanFlag
    global g_setupGameGlobalsFlag

    if g_setupGameGlobalsFlag: #only want this to happen at start of every game
        setupHangmanGlobals()

    g_setupGameGlobalsFlag = False

    g_screen.blit(g_screenText["word selected"]("A random word has been selected...", 1, g_black),(100,100))
    g_screen.blit(g_screenText["enter"]("Press SPACE to continue...", 1, g_black),(100,150))

    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_SPACE:
            print("Inside 2nd event")
            g_playFlag = False
            g_hangmanFlag = True

"""-----------------------------------------------------------------"""

"""-----------------------------------------------------------------"""
def welcomeStage(currentTime, event):
    global g_playFlag
    global g_welcomeFlag

    if currentTime <= 5000:
        g_screen.blit(g_screenText["greeting"]("Hello, and welcome to 'Python Hangman'!", 1, g_black),(100,100))
        
    else:
        g_screen.blit(g_screenText["enter"]("Press ENTER to continue...", 1, g_black),(100,100))

    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_RETURN:
            print("Inside event")
            g_welcomeFlag = False
            g_playFlag = True
"""-----------------------------------------------------------------"""

"""-----------------------------------------------------------------"""
def hangmanStage(event):

    printGuessedWord()
    printWrongGuesses() 
    #printHangman() **Uncomment this 

    if g_GUESSED_WORD == g_DICT_WORD:
        clearScreen()
        #printGuessedWord() **not sure if I'll keep
        #printWrongGuesses() **not sure if I'll keep
        doGameWon(event)
        #deleted "play = "
        #break   
    elif g_NUM_OF_BAD_GUESSES == g_TRIES:
        clearScreen()
        printGuessedWord()
        printWrongGuesses()
        doGameOver(event)
        #deleted "play = "       
        #break
    else:
        promptForLetter()

        if event.type == pygame.KEYDOWN:

            if event.unicode.isalpha():

                letter = pygame.key.name(event.key)
        
                checkLetter(letter)
"""-----------------------------------------------------------------"""

"""-----------------------------------------------------------------"""
def main():
    
    preGameSetup()    
    setFlags(True)

    while 1:
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()

        currentTime = pygame.time.get_ticks()

        clearScreen()

        if g_welcomeFlag: #welcome screen
            welcomeStage(currentTime, event)

        elif g_playFlag: #setup game screen
            clearScreen()
            gameSetupStage(event)

        elif g_hangmanFlag: #main game screen
            clearScreen()
            hangmanStage(event)

        elif g_playAgainFlag: #play again screen
            clearScreen()
            playAgainStage(event)
            
        pygame.display.flip()
    """
    loadWords() #only do this once at application's start

    play = True
    while play:

        clearScreen()

        print("Hello, and welcome to 'Python Hangman'!")
        input("Press ENTER to continue...")

        clearScreen()

        setupGlobals()

        print("A random word has been selected...")
        input("Press ENTER to continue...")
        
        global g_NUM_OF_BAD_GUESSES

        while True: 

            clearScreen()
            printGuessedWord()
            printWrongGuesses()
            printHangman()

            letter = input("\nplease guess a letter: ")
            
            if not checkLetter(letter):
                addToGuessesList(letter)
                g_NUM_OF_BAD_GUESSES += 1 

            if g_GUESSED_WORD == g_DICT_WORD:
                clearScreen()
                printGuessedWord()
                printWrongGuesses()
                printHangman()
                play = doGameWon()
                break   
            elif g_NUM_OF_BAD_GUESSES == g_TRIES:
                clearScreen()
                printGuessedWord()
                printWrongGuesses()
                printHangman()
                play = doGameOver()       
                break     
"""
"""-----------------------------------------------------------------"""

"""-----------------------------------------------------------------"""
def doGameWon(event):

    global g_playAgainFlag
    global g_hangmanFlag

    g_screen.blit(g_screenText["win message"]("CONGRATULATIONS! YOU WON!!!", 1, g_black),(100,100))
    g_screen.blit(g_screenText["win message"]("You correctly guessed '" + ''.join(g_GUESSED_WORD) + "'", 1, g_black),(100,150))
    g_screen.blit(g_screenText["enter"]("Press SPACE to continue...", 1, g_black),(100,250))
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_SPACE:
            g_playAgainFlag = True
            g_hangmanFlag = False
"""-----------------------------------------------------------------"""

"""-----------------------------------------------------------------"""
def doGameOver(event):

    global g_playAgainFlag
    global g_hangmanFlag

    g_screen.blit(g_screenText["lose message"]("Game Over. The word was '" + ''.join(g_DICT_WORD) + "'", 1, g_black),(100,100))
    g_screen.blit(g_screenText["enter"]("Press SPACE to continue...", 1, g_black),(100,150))
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_SPACE:
            g_playAgainFlag = True
            g_hangmanFlag = False
"""-----------------------------------------------------------------"""

"""-----------------------------------------------------------------"""
def playAgainStage(event):

    g_screen.blit(g_screenText["play again"]("Play again? Y/N... ", 1, g_black),(50,500))

    if event.type == pygame.KEYDOWN:
        if event.unicode.isalpha():
            choice = pygame.key.name(event.key)
    
            if choice == "n" or choice == "N":
                sys.exit()
                #input("Goodbye!")
    
            setFlags(False)
"""-----------------------------------------------------------------"""

"""-----------------------------------------------------------------"""
def promptForLetter():

    g_screen.blit(g_screenText["guess letter"]("Please guess a letter: ", 1, g_black),(50,500))
"""-----------------------------------------------------------------"""

"""-----------------------------------------------------------------"""
def printWrongGuesses():

    g_screen.blit(g_screenText["wrong letters"](''.join(g_GUESSES_LIST), 1, g_black),(375,500))
"""-----------------------------------------------------------------"""

"""-----------------------------------------------------------------"""
def printGuessedWord():

    g_screen.blit(g_screenText["word to guess"](''.join(g_GUESSED_WORD), 1, g_black),(375,200))
"""-----------------------------------------------------------------"""

"""-----------------------------------------------------------------"""
def printHangman():
    board = [[[], [], []],
           [[], [], []],
           [[], [], []]]

    if g_NUM_OF_BAD_GUESSES > 0:
        board[0][1] = '0'

    if g_NUM_OF_BAD_GUESSES > 1:
        board[1][1] = '|'

    if g_NUM_OF_BAD_GUESSES > 2:
        board[2][0] = '/'

    if g_NUM_OF_BAD_GUESSES > 3:
        board[2][2] = '\\'

    if g_NUM_OF_BAD_GUESSES > 4:
        board[1][0] = '-'

    if g_NUM_OF_BAD_GUESSES > 5:
        board[1][2] = '-'

    for cell in board:
        print(cell)
    
"""-----------------------------------------------------------------"""
    
"""-----------------------------------------------------------------"""  
def clearScreen():
    g_screen.fill(g_white)
"""-----------------------------------------------------------------"""

"""-----------------------------------------------------------------"""
def addToGuessesList(letter):
    
    g_GUESSES_LIST.append(letter)
"""-----------------------------------------------------------------"""

"""-----------------------------------------------------------------"""
def checkLetter(letter):

    global g_NUM_OF_BAD_GUESSES

    indices = [i for i, x in enumerate(g_DICT_WORD) if x == letter]
    
    if not indices:
        if letter not in g_GUESSES_LIST:
            addToGuessesList(letter)
            g_NUM_OF_BAD_GUESSES += 1

    for index in indices:
        g_GUESSED_WORD[index] = letter

"""-----------------------------------------------------------------"""

if __name__ == '__main__': 
    main()