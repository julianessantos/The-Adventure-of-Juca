import pygame
from config import Configuracao


class Poder(pygame.sprite.Sprite):
    def __init__(self, x, y, direcao):
        super().__init__()
        self.image = pygame.image.load('./Imagens/poder.png')
        self.rect = self.image.get_rect()
        self.rect.center = [x,y]
        self.direcao = direcao
        self.velocidade_poder = 6
        self.poder_sprite = pygame.sprite.Group()

    def update(self):
        self.configuracao = Configuracao()
        self.rect.x += (self.direcao * self.velocidade_poder)
        if self.rect.right < 0 or self.rect.left > self.configuracao.screen_width - 100:
            self.kill()
