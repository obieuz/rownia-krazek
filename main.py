import pygame
import numpy as np
import pygame_widgets
from pygame_widgets.slider import Slider

#TODO
#- additional, zrobic 3 krazki które beda mialy kolizje i taka gre jak to z lodem

print("Witaj w curringu w pythonie!!!")
print("Kliknij d aby wypuścić krążek")
print("Kliknij g aby wygenerowac nowa tarcze")
print("Do zobaczenia na pytońskim boisku")

h=50
l=200
m=1
g=10
f=0.2

windowWidth=800
windowHeight=600
screen=pygame.display.set_mode((windowWidth,windowHeight))
gapY=1

krazekWidth=30
krazekHeight=10

redLength=5
orangeLength=30
yellowLength=60
redBorder=[]
orangeBorder=[]
yellowBorder=[]
spawnProcetion=100

white=(255,255,255)
black=(0,0,0)
red=(255,0,0)
orange=(255,140,0)
yellow=(255,255,0)

run=True
kat=np.arctan((h+gapY)/l)

def generujPlansze():
    center = np.random.randint(l + spawnProcetion + redLength + orangeLength + yellowLength + krazekWidth,
                               windowWidth - redLength - orangeLength - yellowLength - krazekWidth)
    redBorder = [center - redLength - krazekWidth, center + redLength + krazekWidth]
    orangeBorder = [redBorder[0]-orangeLength, redBorder[1]+orangeLength]
    yellowBorder = [orangeBorder[0] - yellowLength, orangeBorder[1] + yellowLength]
    return redBorder,orangeBorder,yellowBorder
def rysujPlansze():
    pygame.draw.line(screen,yellow,(yellowBorder[0],windowHeight-1),(yellowBorder[1],windowHeight-1),2)
    pygame.draw.line(screen, orange, (orangeBorder[0],windowHeight-1), (orangeBorder[1], windowHeight-1),2)
    pygame.draw.line(screen, red, (redBorder[0], windowHeight-1), (redBorder[1], windowHeight-1),2)

def rysujPunkty():
    punkty=k1.zdobytePunkty
    pygame.draw.rect(screen, black, (windowWidth - 50, 0, 50, 30))
    text = font.render(str(punkty), True, white, black)
    textRect = text.get_rect()
    textRect.center = (windowWidth - 40, 20)
    screen.blit(text, textRect)

class krazek:
    def __init__(self,width,height,x,y,color):
        self.width=width
        self.height=height
        self.x=x
        self.y=y
        self.color=color
        self.m=m
        self.v=0
        self.stopped=False
        self.checked=False
        self.zdobytePunkty=0
    def rysuj(self):
        screen.fill((0,0,0))
        pygame.draw.polygon(screen, white, [(0, windowHeight-gapY), (0 + l, windowHeight-gapY), (0, windowHeight - h-gapY)], 1)
        rysujPlansze()
        rysujPunkty()
        if self.y >= windowHeight -2:
            pygame.draw.rect(screen, white, (self.x, self.y - self.height, self.width, self.height))
        else:
            pygame.draw.polygon(screen, white, [(self.x, self.y - gapY), (self.x, self.y - self.height - gapY), (
                self.x + self.width * np.cos(kat), self.y + self.width * np.sin(kat) - self.height - gapY), (
                                                    self.x + self.width * np.cos(kat),
                                                    self.y + self.width * np.sin(kat) - gapY)])
        pygame.display.update()

    def sprawdz(self):
        punkt=0
        if((self.x>=redBorder[0] and self.x+1<=redBorder[1]) or (self.x+self.width>=redBorder[0] and self.x+self.width-1<=redBorder[1])):
            print("czerwone")
            punkt=3
        elif((self.x>=orangeBorder[0] and self.x+1<=orangeBorder[1]) or (self.x+self.width>=orangeBorder[0] and self.x+self.width-1<=orangeBorder[1])):
            print("pomaranczowe")
            punkt=2
        elif((self.x>=yellowBorder[0] and self.x+1<=yellowBorder[1]) or (self.x+self.width>=yellowBorder[0] and self.x+self.width-1<=yellowBorder[1])):
            print("zolte")
            punkt=1
        self.checked=True
        self.zdobytePunkty+=punkt
    def przesunKrazek(self):
        self.rysuj()
        if(self.checked):
            return
        elif(self.stopped):
            self.sprawdz()
            return
        else:
            if (self.y >= windowHeight - 2):
                self.v -= (f*m*g)/m
                if (self.v < 0):
                    self.stopped=True
                    return
                self.y = windowHeight - 2
                self.x+=self.v
            else:
                self.v += (m * g * np.sin(kat) - (f * m * g)) / m
                self.x = self.x + self.v * np.cos(kat)
                self.y=self.y+self.v*np.sin(kat)
pygame.init()

slider = Slider(screen, 20, 20, 100, 20, min=45, max=160, step=5, initial=50)
font=pygame.font.Font('freesansbold.ttf',16)

redBorder,orangeBorder,yellowBorder=generujPlansze()
k1 = krazek(krazekWidth,krazekHeight,0,windowHeight-h,white)

while run:
    events=pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            run=False
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_d:
            k1.x=0
            k1.y=windowHeight-h
            k1.v=0
            k1.stopped=False
            k1.checked=False
            kat = np.arctan((h + gapY) / l)
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_g:
            redBorder,orangeBorder,yellowBorder=generujPlansze()
    k1.przesunKrazek()
    h=int(slider.getValue())
    pygame_widgets.update(events)
    pygame.display.update()
    pygame.time.delay(100)
pygame.quit()