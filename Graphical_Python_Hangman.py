import sys, pygame, random
"""-----------------------------------------------------------------"""
def setupGlobals():   

    global g_TRIES
    g_TRIES = 6 #how many tries the player gets to guess the word

    global g_DICT_WORD
    g_DICT_WORD = list(random.choice(LINES)) #select random word ALSO needed for 'game over' 

    global g_GUESSED_WORD
    g_GUESSED_WORD = []
    for i in range(0, len(g_DICT_WORD)):
        g_GUESSED_WORD.append('*') #word the player sees

    global g_GUESSES_LIST
    g_GUESSES_LIST = [] #the incorrect guesses

    global g_NUM_OF_BAD_GUESSES
    g_NUM_OF_BAD_GUESSES = 0 #counter for num of incorrect guesses
"""-----------------------------------------------------------------"""

"""-----------------------------------------------------------------"""
def preGameSetup():

    pygame.init()
    pygame.font.init()

    #loadWords() **uncomment this

    size = (800, 600)
    
    global g_white
    g_white = (255, 255, 255)

    global g_black
    g_black = (0, 0, 0)

    global g_screen
    g_screen = pygame.display.set_mode(size)

    pygame.display.set_caption("Hangman")

    global g_comicSansFont
    g_comicSansFont = pygame.font.SysFont("Comic Sans MS", 30)

    #greetingString = g_comicSansFont.render("Hello, and welcome to 'Python Hangman'!", 1, g_black)
    #enterString = g_comicSansFont.render("Press ENTER to continue...", 1, g_black)
    
    global g_playFlag
    g_playFlag = False

    global g_screenText
    g_screenText = {"greeting" :  g_comicSansFont.render, "enter" : g_comicSansFont.render, "JUST_A_TEST" : g_comicSansFont.render,}
"""-----------------------------------------------------------------"""

"""-----------------------------------------------------------------"""
def loadWords():

    global LINES #a list of all the possible hangman words

    LINES = open("Master_Word_List.txt").readlines()

    LINES = [word.lower().rstrip("\n") for word in LINES]
"""-----------------------------------------------------------------"""

"""-----------------------------------------------------------------"""
def welcomeStage(currentTime, event):
    global g_playFlag

    if currentTime <= 5000:
        g_screen.blit(g_screenText["greeting"]("Hello, and welcome to 'Python Hangman'!", 1, g_black),(100,100))
        
    else:
        g_screen.blit(g_screenText["enter"]("Press ENTER to continue...", 1, g_black),(100,100))

    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_RETURN:
            g_playFlag = True
"""-----------------------------------------------------------------"""

"""-----------------------------------------------------------------"""
def main():
    
    preGameSetup()    

    #displayWelcome = True

    while 1:
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()

        currentTime = pygame.time.get_ticks()

        clearScreen()

        if not g_playFlag:
            welcomeStage(currentTime, event)

        elif g_playFlag:
            clearScreen()

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
def doGameWon():

    print("\nCONGRATULATIONS! YOU WON!!!")
    print("You correctly guessed " + ''.join(g_GUESSED_WORD))
    play = doPlayAgain()
    return play
"""-----------------------------------------------------------------"""

"""-----------------------------------------------------------------"""
def doGameOver():

    print("\nGame Over. The word was " + ''.join(g_DICT_WORD))
    play = doPlayAgain()
    return play
"""-----------------------------------------------------------------"""

"""-----------------------------------------------------------------"""
def doPlayAgain():

    play = True

    choice = input("Play again? Y/N... ")
    if choice == "n" or choice == "N":
        play = False
        input("Goodbye!")
    
    return play
"""-----------------------------------------------------------------"""

"""-----------------------------------------------------------------"""
def printWrongGuesses():

    print(''.join(g_GUESSES_LIST) + "\n")
"""-----------------------------------------------------------------"""

"""-----------------------------------------------------------------"""
def printGuessedWord():

    print(''.join(g_GUESSED_WORD), end="                    ")
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

    indices = [i for i, x in enumerate(g_DICT_WORD) if x == letter]
    
    if not indices:
        return False

    for index in indices:
        g_GUESSED_WORD[index] = letter

    return True
"""-----------------------------------------------------------------"""

if __name__ == '__main__': 
    main()