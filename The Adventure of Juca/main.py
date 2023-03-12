import pygame, sys

from config import Configuracao
from mapa import Mapa
from desenho_mapa import *
from ui import Ui


class JucaGame:
    def __init__(self):
        pygame.init()
        self.configuracao = Configuracao()
        self.tela = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
        #self.configuracao.screen_width = self.tela.get_rect().width
        #self.configuracao.screen_height = self.tela.get_rect().height

        self.mapa = Mapa(level_0, self.tela, self.mudar_pontuacao, self.mudar_vida)

        self.vida_atual = 150
        self.moedas = 0

        self.ui = Ui(self.tela)

        pygame.display.set_caption('As Aventuras de Juca')

    def run_game(self):
        while True:
            self.eventos()
            self.atualizar_tela()

    def eventos(self):
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                sys.exit()
            elif evento.type == pygame.KEYDOWN:
                self._check_keydown_events(evento)

    def _check_keydown_events(self, evento):
        if evento.key == pygame.K_q:
            sys.exit()

    def mudar_pontuacao(self, total):
        self.moedas += total

    def mudar_vida(self, total):
        self.vida_atual += total

    def atualizar_tela(self):
        self.tela.fill(self.configuracao.bg_cor)

        self.mapa.run()
        self.ui.show_vida(self.vida_atual)
        self.ui.show_moedas(self.moedas)

        pygame.display.flip()
        pygame.display.update()


if __name__ == '__main__':
    jg = JucaGame()
    jg.run_game()
