import pygame, sys, os, random

#module
cwd=os.path.dirname(os.path.realpath(__file__))
os.chdir(cwd)
cwd=os.path.normpath(os.getcwd() + os.sep + os.pardir)
print(cwd)
os.chdir(cwd+"/others")

#screen
screenW=1200
screenH=900
screen=pygame.display.set_mode((screenW,screenH))
background=pygame.image.load("BG.png")
endGameBackground=pygame.image.load("endGameBG.png")
pygame.mouse.set_visible(False)

#game
status=0
#0-not started 1-playing 2-ended
score=0
highScore=0
time=10
extraTimeTimer=-2000

class Target(pygame.sprite.Sprite):
    def __init__(self,picturePath,posX,posY):
        super().__init__()
        self.image=pygame.image.load(picturePath)
        self.rect=self.image.get_rect()
        self.rect.center=[posX,posY]

class StartButton(pygame.sprite.Sprite):
    def __init__(self,picturePath):
        super().__init__()
        self.image=pygame.image.load(picturePath)
        self.rect=self.image.get_rect()
        self.rect.center=[600,450]

class ReplayButton(pygame.sprite.Sprite):
    def __init__(self,picturePath):
        super().__init__()
        self.image=pygame.image.load(picturePath)
        self.rect=self.image.get_rect()
        self.rect.center=[600,600]

def replay():
    replayButton=ReplayButton("replayButton.png")
    replayButtonGroup.add(replayButton)

def shot():
    newTarget= Target("target.png", random.randrange(150,screenW-150), random.randrange(150,screenH-150))
    targetGroup.add(newTarget)

class Crosshair(pygame.sprite.Sprite):
    def __init__(self,picturepath):
        super().__init__()
        self.image=pygame.image.load(picturepath)
        self.rect=self.image.get_rect()
    def shoot(self):
        #return value 0-no col 1-target col 2-start col 3-replay col
        shootReturn=0
        #targetTest
        col= pygame.sprite.spritecollide(crosshairHitBox,targetGroup,True)
        col=bool(col)
        if col == True:
            shot()
            col=False
            shootReturn=1
        #startTest
        col= pygame.sprite.spritecollide(crosshairHitBox,startButtonGroup,True)
        col=bool(col)
        if col == True:
            col=False
            shootReturn=2
        #replayTest
        col= pygame.sprite.spritecollide(crosshairHitBox,replayButtonGroup,True)
        col=bool(col)
        if col == True:
            col=False
            shootReturn=3
        return shootReturn
    def update(self):
        self.rect.center=pygame.mouse.get_pos()
    
pygame.init()
clock=pygame.time.Clock()
currentTime=0

#crosshair
crosshair=Crosshair("crosshair.png")
crosshairHitBox=Crosshair("crosshairHitBox.png")
crosshairGroup=pygame.sprite.Group()
crosshairGroup.add(crosshair)
crosshairGroup.add(crosshairHitBox)

#targets
targetGroup=pygame.sprite.Group()
newTarget= Target("target.png", random.randrange(100,screenW-100), random.randrange(100,screenH-100))
targetGroup.add(newTarget)

#startButton
startButton=StartButton("startButton.png")
startButtonGroup=pygame.sprite.Group()
startButtonGroup.add(startButton)

#replayButton
replayButtonGroup=pygame.sprite.Group()

#text
font=pygame.font.Font('freesansbold.ttf', 32)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type==pygame.MOUSEBUTTONDOWN:
            shotStatus=crosshair.shoot()
            if shotStatus==2:
                gameStartTime=pygame.time.get_ticks()
                status=1
            if shotStatus==3:
                time=10
                score=0
                gameStartTime=pygame.time.get_ticks()
                status=1
            if shotStatus==1:
                score+=1
                if score%5==0:
                    extraTimeTimer=pygame.time.get_ticks()
                    time+=1
                isItShot=False
    
    pygame.display.flip()
    currentTime=pygame.time.get_ticks()
    screen.blit(background,(0,0))
    startButtonGroup.draw(screen)
    crosshairGroup.draw(screen)
    if status==1:
        gameTime=currentTime-gameStartTime
        targetGroup.draw(screen)
        textSurfaceCountDown=font.render(str(time-int(gameTime/1000)),True,(0, 0, 0))
        screen.blit(textSurfaceCountDown,(585,20))
        textSurfaceScore=font.render(str(score),True,(0, 0, 0))
        screen.blit(textSurfaceScore,(1100,20))
        textSurfaceExtraTime=font.render("+1",True,(0,255,0))
        if (currentTime-extraTimeTimer)<800:
            screen.blit(textSurfaceExtraTime,(610,20))
        crosshairGroup.draw(screen)
        if (time-int(gameTime/1000))==0:
            status=2
            if highScore<score:
                highScore=score
            replay()
    if status==2:
        screen.blit(endGameBackground,(400,150))
        textSurfaceScore=font.render("Score:"+str(score),True,(0, 255, 0))
        screen.blit(textSurfaceScore,(500,250))
        textSurfaceHighscore=font.render("Highscore:"+str(highScore),True,(0, 255, 0))
        screen.blit(textSurfaceHighscore,(500,280))
        replayButtonGroup.draw(screen)
        crosshairGroup.draw(screen)
    crosshairGroup.update()
    clock.tick(60)
