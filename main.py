import pygame
import numpy as np
import pygame_widgets
from pygame_widgets.slider import Slider

print("Witaj w curringu w pythonie!!!")
print("Kliknij d aby wypuścić krążek")
print("Kliknij r aby zrestartowac")
print("Do zobaczenia na pytońskim boisku")

h=80
l=200
m=1
g=10
f=0.2

gapY=1

white=(255,255,255)
black=(0,0,0)
red=(255,0,0)
orange=(255,140,0)
yellow=(255,255,0)

run=True

class plansza:
    def __init__(self,width,height,krazekWidth,krazekHeight,spawnProcetion,redWidth,orangeWidth,yellowWidth):
        self.windowWidth=width
        self.windowHeight=height
        self.krazekWidth=krazekWidth
        self.krazekHeight=krazekHeight
        self.spawnProcetion=spawnProcetion
        self.screen=pygame.display.set_mode((width,height))
        self.kat=np.arctan((h + gapY) / l)
        self.excist=False

        self.redBorder=[]
        self.redWidth=redWidth
        self.orangeBorder = []
        self.orangeWidth=orangeWidth
        self.yellowBorder = []
        self.yellowWidth=yellowWidth

        self.Krazki=[]
        self.currentKrazek=-1

        self.punkty=0

    def generujPlansze(self):
        center = np.random.randint(l + self.spawnProcetion + self.redWidth + self.orangeWidth + self.yellowWidth + self.krazekWidth,self.windowWidth - self.redWidth - self.orangeWidth - self.yellowWidth - self.krazekWidth)
        self.redBorder = [center - self.redWidth - self.krazekWidth, center + self.redWidth + self.krazekWidth]
        self.orangeBorder = [self.redBorder[0]-self.orangeWidth, self.redBorder[1]+self.orangeWidth]
        self.yellowBorder = [self.orangeBorder[0] - self.yellowWidth, self.orangeBorder[1] + self.yellowWidth]

    def obliczKat(self):
        self.kat=np.arctan((h + gapY) / l)
    def Punkty(self):
        pygame.draw.rect(self.screen, black, (self.windowWidth - 50, 0, 50, 30))
        text = font.render(str(self.punkty), True, white, black)
        textRect = text.get_rect()
        textRect.center = (self.windowWidth - 40, 20)
        self.screen.blit(text, textRect)

    def Plansza(self):
        pygame.draw.line(self.screen, yellow, (self.yellowBorder[0], self.windowHeight - 1), (self.yellowBorder[1], self.windowHeight - 1), 2)
        pygame.draw.line(self.screen, orange, (self.orangeBorder[0], self.windowHeight - 1), (self.orangeBorder[1], self.windowHeight - 1), 2)
        pygame.draw.line(self.screen, red, (self.redBorder[0], self.windowHeight - 1), (self.redBorder[1], self.windowHeight - 1), 2)

    def Update(self):
        self.Krazki[self.currentKrazek].y=self.windowHeight-h

    def Kolizje(self):
        for i in range (self.currentKrazek+1):
            for j in range (self.currentKrazek+1):
                if i==j:
                    break
                if self.Krazki[i].x+self.Krazki[i].width>=self.Krazki[j].x and self.Krazki[i].x - 1<=self.Krazki[j].x+self.Krazki[j].width:
                    vf=self.Krazki[i].v/(self.Krazki[i].m+self.Krazki[j].m)
                    self.Krazki[i].v=vf
                    self.Krazki[j].v=vf
    def Rysuj(self):
        self.screen.fill(black)
        self.obliczKat()
        if self.excist:
            self.Kolizje()
        pygame.draw.polygon(self.screen, white,
                            [(0, self.windowHeight - gapY), (0 + l, self.windowHeight - gapY), (0, self.windowHeight - h - gapY)], 1)
        self.Punkty()
        self.Plansza()
        for i in range (self.currentKrazek+1):
            self.Krazki[i].ruchKrazek(self.windowHeight, self.kat)
            self.Krazki[i].rysujKrazek(self.screen,self.windowHeight,self.kat)

        pygame.display.update()

    def start(self):
        self.excist=False
        self.currentKrazek=-1
        self.punkty=0
        self.Krazki = []
        self.generujPlansze()
        for i in range (3):
            self.Krazki.append(krazek(0,self.windowHeight-h,self.krazekWidth,self.krazekHeight,white))

    def sprawdz(self):
        for i in range (3):
            self.punkty+=self.Krazki[i].sprawdzKrazek(self.redBorder,self.orangeBorder,self.yellowBorder)
class krazek:
    def __init__(self,x,y,width,height,color):
        self.width=width
        self.height=height
        self.x=x
        self.y=y
        self.color=color
        self.m=m
        self.v=0
    def rysujKrazek(self,screen,windowHeight,kat):
        if self.y >= windowHeight - 2:
            pygame.draw.rect(screen, white, (self.x, self.y - self.height, self.width, self.height))
        else:
            pygame.draw.polygon(screen, white, [(self.x, self.y - gapY), (self.x+self.height*np.sin(kat), self.y - self.height - gapY), (
                self.x + self.width * np.cos(kat)+self.height*np.sin(kat), self.y + self.width * np.sin(kat) - self.height - gapY), (
                                                    self.x + self.width * np.cos(kat),
                                                    self.y + self.width * np.sin(kat) - gapY)])

    def sprawdzKrazek(self,redBorder,orangeBorder,yellowBorder):
        punkt=0
        if((self.x>=redBorder[0] and self.x+1<=redBorder[1]) or (self.x+self.width>=redBorder[0] and self.x+self.width-1<=redBorder[1])):
            print("czerwone!")
            punkt=3
        elif((self.x>=orangeBorder[0] and self.x+1<=orangeBorder[1]) or (self.x+self.width>=orangeBorder[0] and self.x+self.width-1<=orangeBorder[1])):
            print("pomaranczowe!")
            punkt=2
        elif((self.x>=yellowBorder[0] and self.x+1<=yellowBorder[1]) or (self.x+self.width>=yellowBorder[0] and self.x+self.width-1<=yellowBorder[1])):
            print("zolte!")
            punkt=1
        return punkt
    def ruchKrazek(self,windowHeight,kat):
        if (self.y >= windowHeight - 2):
            self.v -= (f * m * g) / m
            if not self.v < 0:
                self.y = windowHeight - 2
                self.x += self.v
        else:
            self.v += (m * g * np.sin(kat) - (f * m * g)) / m
            self.x = self.x + self.v * np.cos(kat)
            self.y = self.y + self.v * np.sin(kat)
pygame.init()

font=pygame.font.Font('freesansbold.ttf',16)

gameboard = plansza(800,600,30,15,100,15,30,60)

slider = Slider(gameboard.screen, 20, 20, 100, 20, min=45, max=160, step=5, initial=80)
gameboard.start()
legal=True
while run:
    events=pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            run=False
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_d:
            gameboard.currentKrazek += 1
            gameboard.excist=True
            if not gameboard.currentKrazek == 3:
                gameboard.Update()
            if gameboard.currentKrazek > 2:
                if legal:
                    gameboard.sprawdz()
                    legal=False
                gameboard.currentKrazek -= 1

        elif event.type == pygame.KEYDOWN and event.key == pygame.K_r:
            gameboard.start()
    gameboard.Rysuj()
    if(not legal):
        pygame.time.delay(3000)
        gameboard.start()
        legal=True
    h=int(slider.getValue())
    gameboard.obliczKat()
    pygame_widgets.update(events)
    pygame.display.update()
    pygame.time.delay(100)
pygame.quit()