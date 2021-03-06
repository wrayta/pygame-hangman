import sys, os, pygame, random

"""-----------------------------------------------------------------"""
def resourcePath(relative):
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, relative)
    return os.path.join(relative)
"""-----------------------------------------------------------------"""

"""-----------------------------------------------------------------"""
def setupHangmanGlobals():   

    global g_tries #how many tries the player gets to guess the word
    g_tries = 7 

    global g_dictWord #select random word ALSO needed for 'game over'
    g_dictWord = list(random.choice(g_lines))  

    global g_guessedWord #word the player sees
    g_guessedWord = []
    for i in range(0, len(g_dictWord)):
        g_guessedWord.append('*') 

    global g_guessesList #the incorrect guesses
    g_guessesList = [] 

    global g_numOfBadGuesses #counter for num of incorrect guesses
    g_numOfBadGuesses = 0 
"""-----------------------------------------------------------------"""

"""-----------------------------------------------------------------"""
def preGameSetup():
    
    global g_width
    g_width = 800

    global g_height
    g_height = 600

    size = (g_width, g_height)
    
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

    global g_stageString
    g_stageString = {"welcome" : "welcomeStage", "gameSetup" : "gameSetupStage", "hangman" : "hangmanStage", "gameWon" : "gameWonStage",
                     "gameOver" : "gameOverStage", "playAgain" : "playAgainStage",}
    
    global g_stagePointer
    g_stagePointer = g_stageString["welcome"]

    global g_stageSelect
    g_stageSelect= {"welcomeStage" : welcomeStage, "gameSetupStage" : gameSetupStage, "hangmanStage" : hangmanStage, "gameWonStage" : gameWonStage,
                    "gameOverStage" : gameOverStage, "playAgainStage" : playAgainStage,}

    global g_setupGameGlobalsFlag
    g_setupGameGlobalsFlag = True
"""-----------------------------------------------------------------"""

"""-----------------------------------------------------------------"""
def loadResources():
    
    filename = "Master_Word_List.txt"
    myWordFile = resourcePath(os.path.join('data', filename))

    global g_lines #a list of all the possible hangman words

    g_lines = open(myWordFile).readlines()

    g_lines = [word.lower().rstrip("\n") for word in g_lines]

    start = "start.png"
    startFile = pygame.image.load(os.path.join('data', start))

    try1 = "try1.png"
    try1File = pygame.image.load(os.path.join('data', try1))

    try2 = "try2.png"
    try2File = pygame.image.load(os.path.join('data', try2))

    try3 = "try3.png"
    try3File = pygame.image.load(os.path.join('data', try3))

    try4 = "try4.png"
    try4File = pygame.image.load(os.path.join('data', try4))

    try5 = "try5.png"
    try5File = pygame.image.load(os.path.join('data', try5))

    try6 = "try6.png"
    try6File = pygame.image.load(os.path.join('data', try6))

    try7 = "try7.png"
    try7File = pygame.image.load(os.path.join('data', try7))

    global g_hangmanDrawings
    g_hangmanDrawings = [startFile, try1File, try2File, try3File, try4File, try5File, try6File, try7File]
"""-----------------------------------------------------------------"""

"""-----------------------------------------------------------------"""
def gameSetupStage(event):
    global g_stagePointer
    global g_setupGameGlobalsFlag

    if g_setupGameGlobalsFlag: #only want this to happen at start of every game
        setupHangmanGlobals()

    g_setupGameGlobalsFlag = False

    g_screen.blit(g_screenText["word selected"]("A random word has been selected...", 1, g_black),(100,100))
    g_screen.blit(g_screenText["enter"]("Press SPACE to continue...", 1, g_black),(100,150))

    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_SPACE:
            g_stagePointer = g_stageString["hangman"]

"""-----------------------------------------------------------------"""

"""-----------------------------------------------------------------"""
def welcomeStage(event):
    global g_stagePointer

    g_screen.blit(g_screenText["greeting"]("Hello, and welcome to 'Python Hangman'!", 1, g_black),(100,100))
        
    g_screen.blit(g_screenText["enter"]("Press ENTER to continue...", 1, g_black),(100,150))

    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_RETURN:
            g_stagePointer = g_stageString["gameSetup"]
"""-----------------------------------------------------------------"""

"""-----------------------------------------------------------------"""
def hangmanStage(event):
    global g_stagePointer

    printHangman() 
    printGuessedWord()
    printWrongGuesses() 

    if g_guessedWord == g_dictWord:
        g_stagePointer = g_stageString["gameWon"]
        #printGuessedWord() **not sure if I'll keep
        #printWrongGuesses() **not sure if I'll keep
  
    elif g_numOfBadGuesses == g_tries:
        g_stagePointer = g_stageString["gameOver"]

    else:
        promptForLetter()

        if event.type == pygame.KEYDOWN:

            if event.unicode.isalpha():

                letter = pygame.key.name(event.key)
        
                checkLetter(letter)
"""-----------------------------------------------------------------"""

"""-----------------------------------------------------------------"""
def main():

    pygame.init()
    pygame.font.init()

    loadResources()
    preGameSetup()   
     
    while 1:
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()

        clearScreen()
        
        g_stageSelect[g_stagePointer](event)

        pygame.display.flip()
    
"""-----------------------------------------------------------------"""

"""-----------------------------------------------------------------"""
def gameWonStage(event):
    global g_stagePointer

    printHangman()

    g_screen.blit(g_screenText["win message"]("CONGRATULATIONS! YOU WON!!!", 1, g_black),(100,50))
    g_screen.blit(g_screenText["win message"]("You correctly guessed '" + ''.join(g_guessedWord) + "'", 1, g_black),(100,100))
    g_screen.blit(g_screenText["enter"]("Press SPACE to continue...", 1, g_black),(100,150))

    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_SPACE:
            g_stagePointer = g_stageString["playAgain"]
"""-----------------------------------------------------------------"""

"""-----------------------------------------------------------------"""
def gameOverStage(event):

    global g_stagePointer

    printHangman() 
    printGuessedWord()
    printWrongGuesses()

    g_screen.blit(g_screenText["lose message"]("Game Over. The word was '" + ''.join(g_dictWord) + "'", 1, g_black),(100,50))
    g_screen.blit(g_screenText["enter"]("Press SPACE to continue...", 1, g_black),(100,100))

    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_SPACE:
            g_stagePointer = g_stageString["playAgain"]
"""-----------------------------------------------------------------"""

"""-----------------------------------------------------------------"""
def playAgainStage(event):
    global g_setupGameGlobalsFlag
    global g_stagePointer

    g_screen.blit(g_screenText["play again"]("Play again? Y/N... ", 1, g_black),(g_width - 750,g_height - 100))

    if event.type == pygame.KEYDOWN:
        if event.unicode.isalpha():
            choice = pygame.key.name(event.key)
    
            if choice == "n" or choice == "N":
                sys.exit()
                #input("Goodbye!")
    
            g_setupGameGlobalsFlag = True
            g_stagePointer = g_stageString["gameSetup"]
"""-----------------------------------------------------------------"""

"""-----------------------------------------------------------------"""
def promptForLetter():

    g_screen.blit(g_screenText["guess letter"]("Please guess a letter: ", 1, g_black),(g_width - 750,g_height - 100))
"""-----------------------------------------------------------------"""

"""-----------------------------------------------------------------"""
def printWrongGuesses():
    
    g_screen.blit(g_screenText["wrong letters"](''.join(g_guessesList), 1, g_black),(g_width - 200,g_height - 100))
"""-----------------------------------------------------------------"""

"""-----------------------------------------------------------------"""
def printGuessedWord():
    text = g_screenText["word to guess"](''.join(g_guessedWord), 1, g_black)
    g_screen.blit(text,[g_width / 2 - text.get_rect().width / 2, 150])
"""-----------------------------------------------------------------"""

"""-----------------------------------------------------------------"""
def printHangman():

    g_screen.blit(g_hangmanDrawings[g_numOfBadGuesses],[g_width / 2 - g_hangmanDrawings[g_numOfBadGuesses].get_rect().width / 2, 
                  g_height / 2 - g_hangmanDrawings[g_numOfBadGuesses].get_rect().height / 2])
    
"""-----------------------------------------------------------------"""
    
"""-----------------------------------------------------------------"""  
def clearScreen():
    g_screen.fill(g_white)
"""-----------------------------------------------------------------"""

"""-----------------------------------------------------------------"""
def addToGuessesList(letter):
    
    g_guessesList.append(letter)
"""-----------------------------------------------------------------"""

"""-----------------------------------------------------------------"""
def checkLetter(letter):

    global g_numOfBadGuesses

    indices = [i for i, x in enumerate(g_dictWord) if x == letter]
    
    if not indices:
        if letter not in g_guessesList:
            addToGuessesList(letter)
            g_numOfBadGuesses += 1

    for index in indices:
        g_guessedWord[index] = letter

"""-----------------------------------------------------------------"""

if __name__ == '__main__': 
    main()