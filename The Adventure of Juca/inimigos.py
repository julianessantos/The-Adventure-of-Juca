import pygame
from bloco import CorteBloco
from random import randint

class Inimigos(CorteBloco):
    def __init__(self, x,y, tamanho):
        super().__init__(x,y, tamanho, pygame.image.load('./Imagens/Inimigos/monstro64.png').convert_alpha())
        self.velocidade_inimigo = randint(2,3)

    def mover_inimigo(self):
        self.rect.x += self.velocidade_inimigo

    #def imagem_reversa(self):
     #   if self.velocidade_inimigo <0:
      #      self.image = pygame.transform.flip(self.image, True, False)

    def reverso(self):
        self.velocidade_inimigo *= -1

    def update(self, deslocamento):
        self.rect.x += deslocamento
        self.mover_inimigo()
        #self.imagem_reversa()
