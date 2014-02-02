#BUG: On Mac, if the game exits for any reason it leaves a pygame Dock icon which must be force-quit.
# Potential Enhancements: High score board, Opening splash screen, Instructions, Count Down before start,
# Adjustable screen size (at least the option to go full screen) - silight
import pygame, random, sys
from easygui import * # I know it increases the prereqs by I think this will help give the game a little extra polish. - silight
pygame.init()

width,height = (800,600) #this is short for width=800 and height=600
screen = pygame.display.set_mode((width,height)) #sets up the window

def spawn_word():
    global words
    wordStr = random.choice(words).strip()
    return TypingGameWord(wordStr)

def intro(): # Introduction to the game. Gives instructions on how to play - silight
    msg = """
                            Welcome to WORD BLASTER!
    
    The war against the Nation of Grammar Nazis is going badly. They have developed a new weapon that is haveing devestating effects on the population of Facebookia. This is a bomb that can only be shot down through spelling the word on the bomb correctly. Needless to say, the Grammar Nazis are winning. 
    
    You have been recruited to fight against this final assault on the free speaking Facebookian nation. With latest in l337 LZeR technology at your fingertips you are supposed to destroy the bombs before the free-speaking, language butchering people of Facebookia are destroyed forever. 
    
    Also, the Grammar Nazis kidnapped your dog. So, screw them. 
    
    Finger to home keys, when you are ready hit okay.
    """
    title = "WORDBLASTER"
    msgbox(msg, title)
    mainLoop()

def mainLoop():#the main loop 
    global running, speed, wordfile, words, currentword, extra_words, score
    while running: 
        clock.tick(20)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False #stops the program
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False #stops the program
                else:
                    if currentword.checkLetter(event.unicode): #event.unicode is the letter the user typed
                        speed += 3
                        score += 1
                        if len(extra_words) > 0:
                            lowestwordindex = 0
                            for i in range(len(extra_words)):
                                if extra_words[i].rect.bottom > extra_words[lowestwordindex].rect.bottom:
                                    lowestwordindex = i
                            currentword = extra_words.pop(lowestwordindex)
                            
                        else:
                            currentword = spawn_word()
        currentword.update()
        for i in extra_words:
            i.update()

        score_surf = score_font.render("SCORE:"+str(score), True, (0,255,0))
        
        screen.fill((0,0,0)) #clears the screen
        screen.blit(background,(0,0))
        screen.blit(score_surf,(0,530))
        for i in extra_words:
            screen.blit(i.image, i.rect)
        pygame.draw.line(screen,(0,255,0),(width/2, height),(currentword.rect.left+7, currentword.rect.bottom),14)
        screen.blit(currentword.image, currentword.rect) #draw the word
        pygame.display.flip() #apply the changes
 
class TypingGameWord(pygame.sprite.Sprite):
    "Represents a word that the user will have to type"
    
    def __init__(self, word):
        global width
        pygame.sprite.Sprite.__init__(self) #initialize it as a pygame sprite
        self.font = pygame.font.Font("font.ttf",40) #make the font we'll write the word in
        self.originalWord = word
        self.word = word
        self.image = self.font.render(self.word, True, (255,255,255))
        self.rect = self.image.get_rect()
        self.rect.bottom = 0 #start the word just above the screen
        self.rect.centerx = random.randint(self.rect.width/2,width-self.rect.width/2)
        
    def checkLetter(self, letter):
        "Checks a letter that the player typed.  Returns true if the word is empty, otherwise false."
        if letter == self.word[0]:
            self.word = self.word[1:]
            self.updateSurface()
        return self.word == ""
    
    def updateSurface(self):
        "Updates self.image to match the text of the word."
        self.image = self.font.render(self.word, True, (255,255,255))
        right = self.rect.right
        bottom = self.rect.bottom
        self.rect = self.image.get_rect()
        self.rect.right = right
        self.rect.bottom = bottom

    def update(self):
        global height
        "Called every frame to update the state of the word."
        global speed, running,score, extra_words, currentword, losestmt
        speedCoefficient = len(self.originalWord)
        if speedCoefficient < len(currentword.originalWord):
            speedCoefficient = len(currentword.originalWord)
        if speedCoefficient < 5:
            speedCoefficient = 5
        old_top = self.rect.top
        self.rect.top += speed / speedCoefficient
        if old_top < height/4 and self.rect.top >= height/4:
            extra_words.append(spawn_word())
        if self.rect.bottom >= height:
            msg = """
            Congratulations, you scored %s
                
              Did you want to play again?
                """ % score # Congratz instead of 'you lose' to leave on a positive note. - silight
            title = "Game Over"
            choice = ynbox(msg, title)
            if choice == 1: # reset the game. Object is still detected at the bottom of the screen.  - silight
                speed = 0
                score = 0
                score_surf = score_font.render("SCORE:"+str(score), True, (0,255,0))
                screen.fill((0,0,0)) #clears the screen
                screen.blit(background,(0,0))
                screen.blit(score_surf,(0,530))
                pygame.display.flip()
                intro()
            else:
                running = False # Exits game - silight


running = True
speed = 10
wordfile = open('words.txt', 'r')
words = wordfile.readlines()
currentword = spawn_word()
extra_words = []
wordfile.close()
score = 0

score_font = pygame.font.Font("score_font.TTF",60)

background = pygame.image.load("background.png").convert()

clock = pygame.time.Clock()
# The Game Starts Here - silight
intro()
mainLoop()       
pygame.quit() #fix the program breaking in IDLE
sys.exit()
