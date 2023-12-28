# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import pygame as pg
from pygame.math import Vector2
import sys, random

pg.init()


#Título
fonte_titu = pg.font.Font(None, 30)

#pontuação na tela
fonte_pont = pg.font.Font(None, 30)



#color
PINK = (173,30,96)
GREEN = (173,204,96)
DARK_GREEN = (43,51,24)

#Formato e tamanho das entradas
celula= 20
numero_de_células = 15

OFFSET = 45

class Comida:
    def __init__(self,cobra_body):
        self.position = self.generate_random_pos(cobra_body)
        #self.position2 = Vector2(7,7)
        
    def draw(self):
        comida_rect1 = pg.Rect(OFFSET + self.position.x *celula,OFFSET +  self.position.y *celula, celula, celula)
        #pg.draw.rect(screen,PINK,comida_rect1)
        
        screen.blit(comida_surface,comida_rect1)
        
        
    def generate_random_Cell(self):
        x = random.randint(0,numero_de_células- 1)
        y = random.randint(0,numero_de_células- 1)
        return Vector2(x,y)
        
    def generate_random_pos(self,cobra_body):
        position =self.generate_random_Cell()
        
        while position in cobra_body:
            position = self.generate_random_Cell()
            
        return position 
class Cobra:
    def __init__(self):
        self.body = [Vector2(6,9),Vector2(5,9),Vector2(4,9)]
        self.direction = Vector2(1,0)
        self.add_segment = False
        self.eat_sound = pg.mixer.Sound("comer.mp3")
        self.hit = pg.mixer.Sound("morrer.mp3")
        
    def draw(self):
        for segment in self.body:
            segment_rect = (OFFSET +segment.x *celula, OFFSET + segment.y*celula,celula, celula)
            pg.draw.rect(screen,DARK_GREEN,segment_rect,0,7)
      
    def update(self):
        self.body.insert(0,self.body[0] + self.direction)
        if self.add_segment == True:
            self.add_segment =False
        else:    
            self.body = self.body[:-1]
    
    def reset(self):
        self.body = [Vector2(6,9),Vector2(5,9),Vector2(4,9)]
        self.direction = Vector2(1,0)
        
        
class Game:
    #Inicia o jogo
    def __init__(self):
        self.cobra = Cobra()
        self.comida = Comida(self.cobra.body)
        self.state =  "Running"
        self.score = 0
        
        
        
    #Define as imagens e graficos
    def draw(self):
        self.comida.draw()
        self.cobra.draw()
        
    #Aplica ações em resposta ao jogador   
    def update(self):
        if self.state == "Running":
            self.cobra.update()
            self.cobra_comeu()
            self.colisao()
            self.colisao_c()
 
    #Define ação de comer
    def cobra_comeu(self):
        if self.cobra.body[0] == self.comida.position:
            self.comida.position = self.comida.generate_random_pos(self.cobra.body)
            self.cobra.add_segment = True
            self.score += 1
            self.cobra.eat_sound.play()
            
    #Define ação de colidir       
    def colisao(self):
        if self.cobra.body[0].x == numero_de_células or self.cobra.body[0].x == -1:
            self.game_over()
        if self.cobra.body[0].y ==  numero_de_células or self.cobra.body[0].y == -1:
            self.game_over()
            
    #Definindo ação de colidir com próprio
    def colisao_c(self):
        headless_body = self.cobra.body[1:]
        if self.cobra.body[0] in headless_body:
            self.game_over()
     
    #Define fim de jogo
    def game_over(self):
        self.cobra.reset()
        self.comida.position = self.comida.generate_random_pos(self.cobra.body)
        self.state = "STOPPED"
        self.score = 0
        self.cobra.hit.play()
        
    
        
        
game = Game()

#Imagem
imagem = pg.image.load("teste.png.png")
# Set the size for the image
DEFAULT_IMAGE_SIZE = (15, 15)
  
# Scale the image to your needed size
comida_surface = pg.transform.scale(imagem, DEFAULT_IMAGE_SIZE)



COBRA_UPT = pg.USEREVENT
pg.time.set_timer(COBRA_UPT,100)





#Tamanho da tela"
screen = pg.display.set_mode((2*OFFSET + celula * numero_de_células, 2*OFFSET +celula * numero_de_células))
pg.display.set_caption("Joguinho1")
clock = pg.time.Clock()

while True:
    for event in pg.event.get():
        if event.type == COBRA_UPT:
            game.update()
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()
            
        #controles
        if event.type ==pg.KEYDOWN:
            if game.state == "STOPPED":
                game.state = "Running"
            if event.key == pg.K_UP and game.cobra.direction != Vector2(0,1):
                game.cobra.direction = Vector2(0,-1)
            
            if event.key == pg.K_DOWN and game.cobra.direction != Vector2(0,-1):
                game.cobra.direction = Vector2(0,1)
            
            if event.key == pg.K_LEFT and game.cobra.direction != Vector2(1,0):
                game.cobra.direction = Vector2(-1,0)
            if event.key == pg.K_RIGHT and game.cobra.direction != Vector2(-1,0):
                game.cobra.direction = Vector2(1,0)
                
             
    
    #Desenhando na tela
    screen.fill(GREEN)
    pg.draw.rect(screen, DARK_GREEN,(OFFSET - 5, OFFSET-5, celula*numero_de_células + 10,celula*numero_de_células + 10), 5)
    game.draw()
    title_surface = fonte_titu.render("Retro Cobrinha", True, PINK)
    score_surface = fonte_pont.render(str(game.score),True,PINK)
    screen.blit(title_surface, (OFFSET - 5,20))
    screen.blit(score_surface, (OFFSET + 250,20))
    
    pg.display.update()
    clock.tick(60)