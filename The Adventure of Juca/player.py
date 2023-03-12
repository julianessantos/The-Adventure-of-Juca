import pygame
from poder import Poder


class Player(pygame.sprite.Sprite):
    def __init__(self, x,y, mudar_vida):
        super().__init__()
        self.image = self.get_frame_by_gid(0)
        self.rect = self.image.get_rect(topleft=(x,y))

        self.caminhando_direita = [2, 3]
        self.caminhando_esquerda = [4, 5]
        self.parado_direita = [0]

        self.lista_quadro = self.parado_direita
        self.quadros = 2

        self.direcao = pygame.math.Vector2(0, 0)
        self.velocidade_player = 1
        self.gravidade = 0.8
        self.pulo_velocidade = -5

        self.mudar_vida = mudar_vida
        self.invencivel = False
        self.invencivel_duracao = 400
        self.dor_tempo = 0

    def get_frame_by_gid(self, gid):
        self.player = pygame.image.load("./imagens/JUCA64.png").convert_alpha()

        columns = 2
        width = 64
        height = 64
        margin = 0
        top = 0
        space_h = 0
        space_v = 0

        linha = gid // columns
        coluna = gid % columns
        x = (coluna * (width + space_h)) + margin
        y = (linha * (height + space_v)) + top

        self.quadro = self.player.subsurface(pygame.Rect((x, y), (width, height)))
        return self.quadro

    def animacao(self):
        self.quadros = self.quadros + 1
        if self.quadros >= len(self.lista_quadro):
            self.quadros = 0

        self.gid = self.lista_quadro[self.quadros]

        self.frame = self.get_frame_by_gid(self.gid)
        return self.frame

    def movimentacao(self):
        #Movimentação do personagem de acordo com eventos de teclado da biblioteca pygame
        keys = pygame.key.get_pressed()
        time = pygame.time.get_ticks()
        tempo_bacana = 500
        if keys[pygame.K_RIGHT]:
            self.rect.x += 1
            self.direcao.x = 1
            self.lista_quadro = self.caminhando_direita
        elif keys[pygame.K_LEFT]:
            self.rect.x -= 1
            self.direcao.x = -1
            self.lista_quadro = self.caminhando_esquerda
        else:
            self.direcao.x = 0
            self.lista_quadro = self.parado_direita

        if keys[pygame.K_SPACE]:
            self.pulo()

    def player_gravidade(self):
        self.direcao.y += self.gravidade
        self.rect.y += self.direcao.y

    def pulo(self):
        self.direcao.y = self.pulo_velocidade

    def danos(self, dano):
        if not self.invencivel:
            self.mudar_vida(dano)
            self.invencivel = True
            self.dor_tempo = pygame.time.get_ticks()

    def invensibilidade(self):
        if self.invencivel:
            tempo_atual = pygame.time.get_ticks()
            if tempo_atual - self.dor_tempo >= self.invencivel_duracao:
                self.invencivel = False

    def update(self, tela):
        self.image = self.animacao()
        self.movimentacao()
        self.invensibilidade()
