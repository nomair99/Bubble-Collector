import pygame, sys
from pygame.locals import *
import random
import sqlite3
import tkinter
from tkinter import *
from tkinter import messagebox

conn = sqlite3.connect('leaderboard.db')
cursor = conn.cursor()
#sqlite 3 uses connect() and cursor() to create a connection to the database
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users(username VARCHAR PRIMARY KEY,
                                     highestscore INTEGER          )
                ''')

#a new table in the database is created using SQL commands


#constants are defined at the start of the program
FPS = 60 #frames per second
WINDOWWIDTH = 720
WINDOWHEIGHT = 540
BUBBLERADIUS = 18 #radius of each bubble


BLACK = (  0,   0,   0)
WHITE = (255, 255, 255)
RED   = (255,   0,   0)
GREEN = (  0, 255,   0)
BLUE  = (  0,   0, 255)
YELLOW = (255, 255, 0)
PINK = (255,192,203)
MENU1 = (211,211,211)
MENU2 = (119,136,153)

#colours are stored as tuples in python so I declared the ones I needed

COLOURLIST = [RED, GREEN, BLUE, YELLOW, PINK] #a list of colour tuples which will be used later in the program

class Player(pygame.sprite.Sprite): #The is the class for the player object
    def __init__(self): #This method initialises the class

        pygame.sprite.Sprite.__init__(self)  #a bulit in data type in pygame, sprite is used for game objects
        playerImage = pygame.image.load('player.png') #player image is loaded
        self.image = playerImage #image is initalised as player image
        self.rect = playerImage.get_rect() #rect is a pygame object used for storing rectangular surfaces, useful for movement and collisions
        self.rect.centerx = WINDOWWIDTH/2 #starting x coordinate of the player is defined
        self.rect.bottom = WINDOWHEIGHT #starting coordinate of the player's bottom is defined
        self.speed = 10 #player speed
        self.colourneeded = getColour(COLOURLIST) #calls the getColour subroutine to get and initial value of the colour needed by the player

    def draw(self):
        #this method draws the player 
        DISPLAYSURF.blit(self.image, self.rect) #player is drawn on the game screen
        pygame.draw.circle(DISPLAYSURF, (self.colourneeded), (self.rect.centerx, self.rect.centery + 20), 15)
        #a circle is drawn presenting the colour of bubble required


class Bubble(pygame.sprite.Sprite):
    #class for the bubble object
    def __init__(self,colour):
        #this method initialises the class
        pygame.sprite.Sprite.__init__(self) #sprite is used once again to declare bubble
        self.colour = colour #colour of the bubble is initialised
        self.radius = BUBBLERADIUS
        self.speed = 7 #speed the bubble moves at is declared
        self.rect = pygame.Rect(0,0,28,28) #just like player rect is used once again
        self.rect.centerx = random.randint(BUBBLERADIUS, WINDOWWIDTH-BUBBLERADIUS) #a random value is generated for the x coordinate
        self.rect.centery = random.randint(-WINDOWHEIGHT, -25) # a random value is generated for the y coordinate
        self.speedmodifier = 1 #used to modify the speed as the game progresses
        
    def draw (self):
        #this method draws the bubble on the game screen
        pygame.draw.circle(DISPLAYSURF, (self.colour), (self.rect.centerx, self.rect.centery), self.radius)
        
    def update(self):
        #this method is used for bubble movement
        self.rect.y = self.rect.y + ((self.speed)*(self.speedmodifier))
        #y coordinate of the bubble is incremented by speed times its modifier each time

class Button1(pygame.sprite.Sprite):
    #class for menu buttons
    def __init__(self, y, text):
        #this method initialises the class
        pygame.sprite.Sprite.__init__(self)#declared as sprite
        self.width = 200
        self.height = 50
        self.rect = pygame.Rect(0,0,self.width,self.height)#a rect is created for button
        self.rect.centerx = WINDOWWIDTH/2
        self.rect.centery = y#self.rect.centery is set to parameter y
        self.colour = MENU1
        self.text = text#text inside the button

    def draw(self):
        pygame.draw.rect(DISPLAYSURF, self.colour, (self.rect.left, self.rect.top, self.width, self.height))
        #button rectangle is drawn
        text = basicfont.render(self.text, True, BLACK)
        textrect = text.get_rect()
        textrect.centerx = self.rect.centerx
        textrect.centery = self.rect.centery
        DISPLAYSURF.blit(text, textrect)
        #text inside button is drawn

class Healthpickup(pygame.sprite.Sprite):
    #class for the health pickup object
    def __init__(self):
        #this method inititalises the class
        pygame.sprite.Sprite.__init__(self)#declared as a sprite
        healthimage = pygame.image.load('health.png')#image for the object
        self.image = healthimage
        self.speed = 10#speed it falls at
        self.rect = healthimage.get_rect()
        self.rect.centerx = random.randint(25, WINDOWWIDTH-25)
        self.rect.centery = -50
        #rect is declared and given coordinates

    def draw(self):
        DISPLAYSURF.blit(self.image, self.rect)
        #the image is drawn on the display

    def update(self):
        self.rect.y += self.speed
        #object falls by incrementing the y value of its rect
    
class Scoreboost(pygame.sprite.Sprite):
    #class for the score boost pickup object
    def __init__(self):
        #this method inititalises the class
        pygame.sprite.Sprite.__init__(self)#declared as a sprite
        scoreboostimage = pygame.image.load('x2.png')#image for the object
        self.image = scoreboostimage
        self.speed = 10#speed it falls at
        self.rect = scoreboostimage.get_rect()
        self.rect.centerx = random.randint(35, WINDOWWIDTH-25)
        self.rect.centery = -50
        #rect is declared and given coordinates

    def draw(self):
        DISPLAYSURF.blit(self.image, self.rect)
        #the image is drawn on the display

    def update(self):
        self.rect.y += self.speed
        #object falls by incrementing the y value of its rect

class Enemy(pygame.sprite.Sprite):
    #class for the enemy object
    def __init__(self,x):
        #this method inititalises the class
        pygame.sprite.Sprite.__init__(self)#declared as a sprite
        enemyimage = pygame.image.load('Enemy.png')#image for the object
        self.image = enemyimage
        self.speed = 15#speed it falls at
        self.rect = enemyimage.get_rect()
        self.rect.centerx = x
        self.rect.centery = 0
        #rect is declared and given coordinates

    def draw(self):
        DISPLAYSURF.blit(self.image, self.rect)
        #the image is drawn on the display

    def update(self):
        self.rect.y += self.speed
        #object falls by incrementing the y value of its rect



def getBubblePosition():
    x = random.randint(BUBBLERADIUS, WINDOWWIDTH-BUBBLERADIUS)
    y = random.randint(-WINDOWHEIGHT, -25)
    
    return x,y
    #this subroutine generates random coordinates for the bubbles when needed

def getColour(COLOURLIST):
    random.shuffle(COLOURLIST)
    colour = COLOURLIST[0]
    return colour
    #shuffles the colour list to genrate a random colour for the bubble


def displayScore():
    scoretext = basicfont.render("Score: " + str(score) ,True, BLACK)
    scoretextrect = scoretext.get_rect()
    scoretextrect.left = WINDOWWIDTH - 100
    scoretextrect.top = 10
    #the score text along with its rect surface on the display and coordinates is defined
    livestext = basicfont.render("Lives: " + str(lives) ,True, BLACK)
    livestextrect = scoretext.get_rect()
    livestextrect.left =  10
    livestextrect.top = 10
    #the number of lives text along with its rect surface on the display and coordinates is defined
    return scoretext, scoretextrect, livestext, livestextrect
    #both texts along with their rect items are returned



def Rungame():
    global score, lives

    player = Player()#player object  is instantiated
    bubbleList = pygame.sprite.Group() #a group of sprites that will be used to add bubbles is created
    spawnRate = 5#number of bubbles in each spawn
    score = 0 #user's score
    lives = 10 #number of lives remaining
    scoreMutiplier = 1#controls the score
    healthList = pygame.sprite.Group()#list of health pickup objects
    scoreboostList = pygame.sprite.Group()#list of score boost pickup objects
    spawnpickup = pygame.USEREVENT + 1#event that spawns pickups
    timeatcollision = 0#time elapsed when score boost collides with the player
    pygame.time.set_timer(spawnpickup, random.randrange(15000,30000))#adds the userevent to the event queue every given time interval
    spawnenemy = pygame.USEREVENT + 2#event that spawns enemy
    pygame.time.set_timer(spawnenemy, random.randrange(30000,60000))##adds the userevent to the event queue every given time interval 
    enemyList = pygame.sprite.Group()#sprite group for enemy objects
    popsound = pygame.mixer.Sound('pop.wav')#sound effect
    music = pygame.mixer.Sound('backgroundmusic.wav')#background music
    
    for i in range(0, spawnRate):   
        colour = getColour(COLOURLIST)
        bubble = Bubble(colour)
        bubbleList.add(bubble)
        #loop used to instantiate and add bubbles to the sprite group
           
    while True: #the main game loop
        keyPressed = pygame.key.get_pressed()#gets key pressed by the user
        DISPLAYSURF.blit(background, [0, 0])#Background image is drawn on the game screen
        player.draw()#draw method in the class Player is called for the object player        
        
        if keyPressed[K_RIGHT] and player.rect.right < WINDOWWIDTH:
            #checks if the right arrow key is pressed and player's right coordinate is less than the right most window coordinate
            player.rect.x += player.speed
            #increases the value of player's x coordinate by it's speed hence moving it to the right

        if keyPressed[K_LEFT] and player.rect.left > 0:
            #checks if the left arrow key is pressed and player's left coordinate is less than 0 (the left most window coordinate)
            player.rect.x -= (player.speed)
            #decreases the value of player's x coordinate by it's speed hence moving it to the left

        addBubble = False
                
        for bubble in bubbleList:
            bubble.draw()
            bubble.update()
            #draw() and update() is called for every object inside the group
            if pygame.sprite.collide_rect(bubble, player):#detects a collision btween the player and bubble
                popsound.play()#pop sound effect is played
                if bubble.colour == player.colourneeded:
                    score += 10*scoreMultiplier
                    player.colourneeded = getColour(COLOURLIST)
                    #points are awarded and player.colourneeded is randomised if a bubble of right colour is collected
                    if score%100 == 0:
                        addBubble = True
                        #value of addBubble boolean is set to True if score is a multiple of 100
                    if addBubble == True:
                        colour = getColour(COLOURLIST)
                        newbubble = Bubble(colour)
                        bubbleList.add(newbubble)
                        addBubble = False
                        #if addBubble is true a newBubble is added to the list, addBubble is set to False
                else:
                    lives -= 1
                    #a life is lost if a bubble of wrong colour is collected
                bubble.rect.centerx, bubble.rect.centery = getBubblePosition()
                bubble.colour = getColour(COLOURLIST)                
                   
                
            if bubble.rect.top > WINDOWHEIGHT:
                bubble.rect.centerx, bubble.rect.centery = getBubblePosition()
                bubble.colour = getColour(COLOURLIST)
                #colour and coordinates of the bubble are randomised if it reaches the bottom of the screen
                
        for health in healthList:
            health.draw()
            health.update()
            if pygame.sprite.collide_rect(health, player):
                popsound.play()
                lives += 1
                health.kill()
                health.rect.y = -500
            if health.rect.top > WINDOWWIDTH:
                health.kill()                
        #goes through every health pickup item in the sprite group to detect collsions and award an extra live

        for scoreboost in scoreboostList:
            scoreboost.draw()
            scoreboost.update()
            if pygame.sprite.collide_rect(scoreboost, player):
                popsound.play()
                timeatcollision = pygame.time.get_ticks()
                scoreboost.kill()
                scoreboost.rect.y = - 500
            if scoreboost.rect.top > WINDOWHEIGHT :
                scoreboost.kill()
            #goes through every score boost pickup item in the sprite group to detect collsions and activate score boost
            
        currenttime = pygame.time.get_ticks()
        if currenttime - timeatcollision < 30000 and timeatcollision > 0:
            scoreMultiplier = 2
        else:
            scoreMultiplier = 1
        #decides the value of scoreMultiplier depending on time passed since collsion

        for enemy in enemyList:
            enemy.draw()
            enemy.update()
            if pygame.sprite.collide_rect(enemy, player):
                popsound.play()
                lives = 0
        #goes through every enemy item in the sprite group

    
        if lives <= 0:
                Endscreen()
                #checks if lives is less than or equal to 0 and calls Endscreen() if that is the case
            
        if score > 10:
            
            for bubble in bubbleList:
                bubble.speedmodifier = score/500 + 1
                #speed modifier is adjusted depending on the score
                
        for event in pygame.event.get():#get all the events from the event queue
            if event.type == QUIT:
                pygame.quit()
                sys.exit()#exits if the event is quit
            if event.type == spawnpickup:
                pickuptype = random.randint(1,2)
                if pickuptype == 1:
                    health = Healthpickup()
                    healthList.add(health)
                elif pickuptype ==2:
                    scoreboost = Scoreboost()
                    scoreboostList.add(scoreboost)
                #if the event spawnpickup is in the event queue a pickup object is instantiated and added to a sprite group
            if event.type == spawnenemy:
                enemy = Enemy(player.rect.centerx)
                enemyList.add(enemy)
            #if the event spawnenemy is in the event queue an enemy object is intantiated and added to a sprite group
                
        if not(pygame.mixer.get_busy()):
            music.play()#background music is played if the pygame mixer isn't playing anything
                
        scoretext, scoretextrect, livestext, livestextrect = displayScore()      
        DISPLAYSURF.blit(scoretext, scoretextrect)
        DISPLAYSURF.blit(livestext, livestextrect)
        pygame.display.update()
        CLOCK.tick(FPS)
        
def Endscreen():
    endtext = basicfont.render("You scored " + str(score) + " Please select one of the options below" ,True, BLACK)
    endtextrect = endtext.get_rect()
    endtextrect.centerx = WINDOWWIDTH/2
    endtextrect.centery = WINDOWHEIGHT/2
    #the text displayed after the game ends is declared
    buttonList2 = pygame.sprite.Group()
    menuButton = Button1(400, "MENU")
    restartButton = Button1(500, "RESTART")
    buttonList2.add(menuButton, restartButton)
    #a new sprite group is created to add 2 buttons for going back to the menu or restarting the game
    
    cursor.execute('''SELECT highestscore FROM users WHERE username = ? ''',
                         (username,))
    highestscore = cursor.fetchone()
    #highestscore is assigned to the highestscore field for the active user
    if score > highestscore[0]:
                      cursor.execute('''UPDATE users SET highestscore = ? WHERE username = ? ''',
                                      (score, username))
                      conn.commit()
    #highestscore is modified if the user acheive more than they previously did
    
         
    while True:
        DISPLAYSURF.fill(WHITE)
        #display is filled white
        DISPLAYSURF.blit(endtext, endtextrect)
        #text is drawn on the display
        mousePosition = pygame.mouse.get_pos()
        #a variable is used to get mouse position
        mouseClick = pygame.mouse.get_pressed()
        #a variable is used to get current status of mouse buttons
        
        for button in buttonList2:
            
            button.draw()
            #all buttons are drawn
            if button.rect.left < mousePosition[0] < button.rect.right and button.rect.top < mousePosition[1] < button.rect.bottom:
                button.colour = MENU2
                #button colour is changed if mouse points on it
                if mouseClick[0] == 1:
                    if button.text == "MENU":
                        main()
                    if button.text == "RESTART":
                        Rungame()
                    #actions are perfromed if one of the menu button is pressed depending on the button pressed                    
            else:
                button.colour = MENU1
                
        for event in pygame.event.get():#get all the events from the event queue
            if event.type == QUIT:
                pygame.quit()
                sys.exit()#exits if the event is quit
        pygame.display.update()
        CLOCK.tick(FPS)

def Login():
    #this subroutine is used for logging users in
    global username#username is made global as it would be needed in other parts of the program
    invalidlist = []
    invalid = " !@#$%^&*()+=[]{}\|;:'></? "
    for i in range(0, len(invalid)):
                   invalidlist.append( invalid[i])
    invalidlist.append('"')
    #a list of invalid characters is created
    root = Tk()
    root.title("Please sign in")
    root.geometry("250x50")
    Label(root, text="Username").grid(row=0)
    entry1 = Entry(root)
    entry1.grid(row=0, column=1)
    Button(root, text='Enter', command=root.quit).grid(row=1, column=1, sticky=W, pady=4)
    root.mainloop()
    #a log in window is created
    try:
        username = entry1.get()
    except:
        main()
    #username is assigned to the value in the entry box if not possible main() is called

    for i in range(0,len(username)):
               while username[i] in invalidlist:
                    messagebox.showinfo("Error", "Invalid characters entered")
                    root.destroy()
                    main()
                                  
    #username is checked for invalid characters 
    while len(username) < 5 or len(username) > 20:
        messagebox.showinfo("Error", "Username must be between 5 and 20 letters long")
        root.destroy()
        main()
    #a length check is done on the username
    try:
        cursor.execute('''INSERT INTO users VALUES(?,?)''',(username, 0))
        conn.commit()
        messagebox.showinfo("Successful", "Welcome to Bubble Collector")
    except sqlite3.IntegrityError:
        messagebox.showinfo("Successful", "Welcome Back")        
    #username is added to the database unless it already exists there
    root.destroy()
    Rungame()
    #window is closed and Rungame() is called to start a new game

def Help():
    backButton = Button1(500, 'BACK')
    helpbackground = pygame.image.load("help.png")#the background image for the help section
    while True:
        DISPLAYSURF.blit(helpbackground, [0,0])
        mousePosition = pygame.mouse.get_pos()
        #a variable is used to get mouse position
        mouseClick = pygame.mouse.get_pressed()
        #a variable is used to get current status of mouse buttons
        backButton.draw()
        if backButton.rect.left < mousePosition[0] < backButton.rect.right and backButton.rect.top < mousePosition[1] < backButton.rect.bottom:
            backButton.colour = MENU2
            #button colour is changed if mouse points on it
            if mouseClick[0] == 1:
                main()#actions are perfromed if one of the menu button is pressed depending on the button pressed           
        else:
            backButton.colour = MENU1

        for event in pygame.event.get():#get all the events from the event queue
            if event.type == QUIT:
                pygame.quit()
                sys.exit()#exits if the event is quit
        pygame.display.update()
        CLOCK.tick(FPS)
        

def Leaderboard():
    leaderboardfont = pygame.font.SysFont('Arial', 35)
    cursor.execute('''SELECT* FROM users ORDER BY highestscore desc''')#data is obtained from the database table in descending order
    scores = cursor.fetchmany(10)#10 of those values are fetched
    if len(scores) < 10:
        x = len(scores)
    else:
        x = 10 #x is set to 10 or the number of items if less than 10
    DISPLAYSURF.blit(background, [0, 0])#background image is drawn on the display
    backButton = Button1(515, 'BACK')#a backButton is instantiated
    for i in range(0, x):
            leaderboardtext = leaderboardfont.render(str(i+1) + ".        " + scores[i][0] ,True, BLACK)
            leaderboardtextrect = leaderboardtext.get_rect()
            leaderboardtextrect.x = 10
            leaderboardtextrect.centery = i*50 + 20
            DISPLAYSURF.blit(leaderboardtext,leaderboardtextrect)
            leaderboardtext2 = leaderboardfont.render(str(scores[i][1]) ,True, BLACK)
            leaderboardtext2rect = leaderboardtext.get_rect()
            leaderboardtext2rect.x = 500
            leaderboardtext2rect.centery = i*50 + 20
            DISPLAYSURF.blit(leaderboardtext2,leaderboardtext2rect)
            #the leaderboard text is drawn on the screen using a for loop depending on the value of x
    while True:
             mousePosition = pygame.mouse.get_pos()
             #a variable is used to get mouse position
             mouseClick = pygame.mouse.get_pressed()
             #a variable is used to get current status of mouse buttons
             backButton.draw()
             if backButton.rect.left < mousePosition[0] < backButton.rect.right and backButton.rect.top < mousePosition[1] < backButton.rect.bottom:
                backButton.colour = MENU2
                #button colour is changed if mouse points on it
                if mouseClick[0] == 1:
                    main()#actions are perfromed if one of the menu button is pressed depending on the button pressed           
             else:
                backButton.colour = MENU1
             for event in pygame.event.get():#get all the events from the event queue
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()#exits if the event is quit
             pygame.display.update()
             CLOCK.tick(FPS)
                
def main():
    global DISPLAYSURF, DISPLAYRECT, CLOCK, basicfont, background
    #some variables are made global as they are needed throughout the program
    pygame.init()#pygame is initialised
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT ))
    #the pygame display window is declared as DISPLAYSURF, width and height are set as the constant defined at the start
    pygame.display.set_caption('Bubble Collector')#display window caption is set
    DISPLAYRECT = DISPLAYSURF.get_rect()#just like the objects display also has a rect item which is defined
    background = pygame.image.load("background.png")#the background image
    basicfont = pygame.font.SysFont('Arial', 25)#font used for displaying text
    CLOCK = pygame.time.Clock()#gameclock    
    
    buttonList = pygame.sprite.Group()#a sprite group to hold buttons is declared
    playButton = Button1(175, "PLAY")
    leaderboardButton = Button1(250, "LEADERBOARD")
    helpButton = Button1(325, "HELP")
    quitButton = Button1(400, "QUIT")
    #all the buttons needed for the menu are instantiated
    buttonList.add(playButton, leaderboardButton, helpButton, quitButton)
    #buttons are added to the sprite group
    while True:
        DISPLAYSURF.blit(background, [0, 0])
        #background is drawn on the screen
        mousePosition = pygame.mouse.get_pos()
        #a variable is used to get mouse position
        mouseClick = pygame.mouse.get_pressed()
        #a variable is used to get current status of mouse buttons
        for button in buttonList:
            button.draw()
            #all buttons are drawn
            if button.rect.left < mousePosition[0] < button.rect.right and button.rect.top < mousePosition[1] < button.rect.bottom:
                button.colour = MENU2
                #button colour is changed if mouse points on it
                if mouseClick[0] == 1:
                    if button.text == "PLAY":
                        Login()
                    if button.text == "LEADERBOARD":
                        Leaderboard()
                    if button.text == "HELP":
                        Help()
                    if button.text == "QUIT":
                        pygame.quit()
                        sys.exit()
                        #actions are perfromed if one of the menu button is pressed depending on the button pressed           
            else:
                button.colour = MENU1
            
        
        for event in pygame.event.get():#get all the events from the event queue
            if event.type == QUIT:
                pygame.quit()
                sys.exit()#exits if the event is quit
        pygame.display.update()
        CLOCK.tick(FPS)

if __name__ == '__main__':
    main()



