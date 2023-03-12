import pygame
from config import Configuracao
from leitor import import_csv_layout, import_cut
from desenho_mapa import *
from bloco import Bloco, CorteBloco, Lava, Moeda, VidaExtra
from inimigos import Inimigos
from player import Player
from poder import Poder


class Mapa:
    def __init__(self, desenho_mapa, tela, mudar_pontuacao, mudar_vida):
        self.display = tela
        self.velocidade_deslocamento = 0
        self.configuracao = Configuracao()

        self.mudar_pontuacao = mudar_pontuacao

        player_layout = import_csv_layout(desenho_mapa["player"])
        self.player = pygame.sprite.GroupSingle()
        self.goal = pygame.sprite.GroupSingle()
        self.player_setup(player_layout, mudar_vida)

        self.poder_sprite = pygame.sprite.Group()
        self.ultimo_tiro = pygame.time.get_ticks()

        fundo_layout = import_csv_layout(desenho_mapa["fundo"])
        self.fundo_sprites = self.config_mapa(fundo_layout, "fundo")

        level_layout = import_csv_layout(desenho_mapa["level"])
        self.level_sprites = self.config_mapa(level_layout, "level")

        moedas_layout = import_csv_layout(desenho_mapa["moedas"])
        self.moedas_sprites = self.config_mapa(moedas_layout, "moedas")

        vida_extra_layout = import_csv_layout(desenho_mapa["vida_extra"])
        self.vida_extra_sprites = self.config_mapa(vida_extra_layout, "vida_extra")

        correntes_layout = import_csv_layout(desenho_mapa["correntes"])
        self.correntes_sprites = self.config_mapa(correntes_layout, "correntes")

        espinhos_layout = import_csv_layout(desenho_mapa["espinhos"])
        self.espinhos_sprites = self.config_mapa(espinhos_layout, "espinhos")

        lava_layout = import_csv_layout(desenho_mapa["lava"])
        self.lava_sprites = self.config_mapa(lava_layout, "lava")

        inimigos_layout = import_csv_layout(desenho_mapa["inimigos"])
        self.inimigos_sprites = self.config_mapa(inimigos_layout, "inimigos")

        barreira_layout = import_csv_layout(desenho_mapa["barreira"])
        self.barreira_sprites = self.config_mapa(barreira_layout, "barreira")

    def config_mapa(self, layout, type):
        sprite_group = pygame.sprite.Group()

        for indice_linha, linha in enumerate(layout):
            for indice_coluna, cedula in enumerate(linha):
                if cedula != "-1":
                    x = indice_coluna * self.configuracao.tamanho_bloco
                    y = indice_linha * self.configuracao.tamanho_bloco

                    if type == "fundo":
                        fundo_lista = import_cut('./Imagens/fundo.png')
                        fundo_surface = fundo_lista[int(cedula)]
                        sprite = CorteBloco(x, y, self.configuracao.tamanho_bloco, fundo_surface)
                        sprite_group.add(sprite)

                    if type == "level":
                        level_lista = import_cut('./Imagens/tileset64x64.png')
                        bloco_surface = level_lista[int(cedula)]
                        sprite = CorteBloco(x,y, self.configuracao.tamanho_bloco, bloco_surface)
                        sprite_group.add(sprite)

                    if type == "moedas":
                        sprite = Moeda(x,y,self.configuracao.tamanho_bloco)
                        sprite_group.add(sprite)

                    if type == "vida_extra":
                        sprite = VidaExtra(x,y, self.configuracao.tamanho_bloco)
                        sprite_group.add(sprite)

                    if type == "correntes":
                        correntes_lista = import_cut('./Imagens/correntes.png')
                        bloco_surface = correntes_lista[int(cedula)]
                        sprite = CorteBloco(x,y, self.configuracao.tamanho_bloco, bloco_surface)
                        sprite_group.add(sprite)

                    if type == "lava":
                        sprite = Lava(x,y, self.configuracao.tamanho_bloco)
                        sprite_group.add(sprite)

                    if type == "espinhos":
                        espinhos_lista = import_cut('./Imagens/espinhooos.png')
                        bloco_surface = espinhos_lista[int(cedula)]
                        sprite = CorteBloco(x, y, self.configuracao.tamanho_bloco, bloco_surface)
                        sprite_group.add(sprite)

                    if type == "inimigos":
                        sprite = Inimigos(x,y, self.configuracao.tamanho_bloco)
                        sprite_group.add(sprite)

                    if type == "barreira":
                        sprite = Bloco(x,y, self.configuracao.tamanho_bloco)
                        sprite_group.add(sprite)

        return sprite_group

    def player_setup(self, layout, mudar_vida):
        for indice_linha, linha in enumerate(layout):
            for indice_coluna, cedula in enumerate(linha):
                x = indice_coluna * self.configuracao.tamanho_bloco
                y = indice_linha * self.configuracao.tamanho_bloco
                if cedula == "0":
                    sprite = Player(x,y, mudar_vida)
                    self.player.add(sprite)
                if cedula == "1":
                    star_lista = import_cut('./Imagens/player.png')
                    star_suface = star_lista[int(cedula)]
                    sprite = CorteBloco(x,y, self.configuracao.tamanho_bloco, star_suface)
                    self.goal.add(sprite)

    def poder(self):
        keys = pygame.key.get_pressed()
        time = pygame.time.get_ticks()
        tempo_bom = 500

        player = self.player.sprite

        if keys[pygame.K_x] and time - self.ultimo_tiro > tempo_bom:
            sprite = Poder(player.rect.centerx, player.rect.centery, player.direcao.x)
            self.poder_sprite.add(sprite)
            self.ultimo_tiro = time

    def colisao_inimigos_barreira(self):
        for inimigos in self.inimigos_sprites.sprites():
            if pygame.sprite.spritecollide(inimigos, self.barreira_sprites, False):
                inimigos.reverso()

    def colisao_horizontal(self):
        player = self.player.sprite
        player.rect.x += player.direcao.x * player.velocidade_player

        for sprite in self.level_sprites.sprites():
            if sprite.rect.colliderect(player.rect):
                if player.direcao.x < 0:
                    player.rect.left = sprite.rect.right
                elif player.direcao.x > 0:
                    player.rect.right = sprite.rect.left

    def colisao_vertical(self):
        player = self.player.sprite
        player.player_gravidade()

        for sprite in self.level_sprites.sprites():
            if sprite.rect.colliderect(player.rect):
                if player.direcao.y > 0:
                    player.rect.bottom = sprite.rect.top
                    player.direcao.y = 0
                elif player.direcao.y < 0:
                    player.rect.top = sprite.rect.bottom
                    player.direcao.y = 0

    def colisao_player_inimigos(self):
        inimigo_colisao = pygame.sprite.spritecollide(self.player.sprite, self.inimigos_sprites, False)

        if inimigo_colisao:
            self.player.sprite.danos(-50)

    def colisao_player_lava(self):
        lava_colisao = pygame.sprite.spritecollide(self.player.sprite, self.lava_sprites, False)

        if lava_colisao:
            self.player.sprite.danos(-50)

    def colisao_player_espinho(self):
        espinho_colisao = pygame.sprite.spritecollide(self.player.sprite, self.espinhos_sprites, False)

        if espinho_colisao:
            self.player.sprite.danos(-50)

    def movimentacao_mapa(self):
        self.configuracao = Configuracao()

        player = self.player.sprite
        player_x = player.rect.centerx
        direcao_x = player.direcao.x

        if player_x < (self.configuracao.screen_width / 4) and direcao_x < 0:
            self.velocidade_deslocamento = 4
            player.velocidade_player = 0
        elif player_x > self.configuracao.screen_width - (self.configuracao.screen_width / 4) and direcao_x > 0:
            self.velocidade_deslocamento = -4
            player.velocidade_player = 0
        else:
            self.velocidade_deslocamento = 0
            player.velocidade_player = 1

    def poder_colisao(self):
        for poder in self.poder_sprite.sprites():
            for inimigo in self.inimigos_sprites:
                if pygame.sprite.spritecollide(poder, self.inimigos_sprites, False):
                    inimigo.kill()
                    poder.kill()

    def moedas_colisao(self):
        colisao_moedas = pygame.sprite.spritecollide(self.player.sprite, self.moedas_sprites, True)

        if colisao_moedas:
            for moeda in colisao_moedas:
                self.mudar_pontuacao(1)

    def vida_extra_colisao(self):
        vida_extra_colisao = pygame.sprite.spritecollide(self.player.sprite, self.vida_extra_sprites, True)

        if vida_extra_colisao:
            for vida in vida_extra_colisao:
                self.player.sprite.danos(+50)

    def run(self):
        self.fundo_sprites.update(self.velocidade_deslocamento)
        self.fundo_sprites.draw(self.display)

        self.level_sprites.update(self.velocidade_deslocamento)  # Movimentando o mapa
        self.level_sprites.draw(self.display)  # Desenhando os blocos criados na tela

        self.moedas_sprites.update(self.velocidade_deslocamento)
        self.moedas_sprites.draw(self.display)

        self.vida_extra_sprites.update(self.velocidade_deslocamento)
        self.vida_extra_sprites.draw(self.display)

        self.correntes_sprites.update(self.velocidade_deslocamento)
        self.correntes_sprites.draw(self.display)

        self.lava_sprites.update(self.velocidade_deslocamento)
        self.lava_sprites.draw(self.display)

        self.espinhos_sprites.update(self.velocidade_deslocamento)
        self.espinhos_sprites.draw(self.display)

        self.inimigos_sprites.update(self.velocidade_deslocamento)
        self.barreira_sprites.update(self.velocidade_deslocamento)
        self.colisao_inimigos_barreira()
        self.inimigos_sprites.draw(self.display)

        self.poder()
        self.poder_sprite.draw(self.display)
        self.poder_sprite.update()
        self.poder_colisao()

        self.player.update(self.display)
        self.colisao_horizontal()
        self.colisao_vertical()
        self.movimentacao_mapa()
        self.player.draw(self.display)
        self.goal.update(self.velocidade_deslocamento)
        self.goal.draw(self.display)

        self.moedas_colisao()
        self.colisao_player_inimigos()
        self.colisao_player_espinho()
        self.colisao_player_lava()
        self.vida_extra_colisao()
