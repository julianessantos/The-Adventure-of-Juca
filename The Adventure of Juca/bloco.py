import pygame


class Bloco(pygame.sprite.Sprite):
    def __init__(self, x,y, tamanho):
        super().__init__()
        self.image = pygame.Surface((tamanho, tamanho))
        self.rect = self.image.get_rect(topleft = (x,y))

    def update(self, x_deslocamento):
        self.rect.x += x_deslocamento

class CorteBloco(Bloco):
    def __init__(self, x,y, tamanho, corte):
        super().__init__(x,y, tamanho)
        self.image = corte

class Lava(CorteBloco):
    def __init__(self, x,y, tamanho):
        super().__init__(x,y, tamanho, pygame.image.load('./Imagens/lava.png').convert_alpha())

class Moeda(CorteBloco):
    def __init__(self, x,y, tamanho):
        super().__init__(x,y, tamanho, pygame.image.load('./Imagens/moedas 64.png').convert_alpha())

class VidaExtra(CorteBloco):
    def __init__(self, x,y, tamanho):
        super().__init__(x,y, tamanho, pygame.image.load('./Imagens/vida_extra.png').convert_alpha())
