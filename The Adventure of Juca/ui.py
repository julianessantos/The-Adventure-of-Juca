import pygame


class Ui:
    def __init__(self, surface):
        self.display = surface

        self.barra_vida_completa = pygame.image.load("./Imagens/UI/Barra de vida/V3.png")
        self.barra_vida_dois_terco = pygame.image.load("./Imagens/UI/Barra de vida/V2.png")
        self.barra_vida_um_terco = pygame.image.load("./Imagens/UI/Barra de vida/V1.png")
        self.barra_vida_vazia = pygame.image.load("./Imagens/UI/Barra de vida/V0.png")

        self.moedas = pygame.image.load('./Imagens/moedas 64.png')
        self.moedas_rect = self.moedas.get_rect(topleft = (50,50))

        self.font = pygame.font.Font('./Imagens/UI/ARCADEPI.TTF',30)

    def show_vida(self, atual):
        if atual == 150:
            self.display.blit(self.barra_vida_completa, (20,10))
        elif atual == 100:
            self.display.blit(self.barra_vida_dois_terco, (20, 10))
        elif atual == 50:
            self.display.blit(self.barra_vida_um_terco, (20, 10))
        else:
            self.display.blit(self.barra_vida_vazia, (20, 10))


    def show_moedas(self, total):
        self.display.blit(self.moedas, self.moedas_rect)

        moedas_display = self.font.render(str(total),False,"#e2e2e2")
        moedas_display_rect = moedas_display.get_rect(midleft = (self.moedas_rect.right + 4, self.moedas_rect.centery))

        self.display.blit(moedas_display, moedas_display_rect)
