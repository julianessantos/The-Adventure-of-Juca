from csv import reader
from config import *
import pygame


def import_csv_layout(path):
    level_map = []
    with open(path) as map:
        level = reader(map, delimiter = ',')
        for linha in level:
            level_map.append(list(linha))

        return level_map

def import_cut(path):
    configuracao = Configuracao()
    bloco = pygame.image.load((path)).convert_alpha()
    bloco_x = int(bloco.get_size()[0] / configuracao.tamanho_bloco)
    bloco_y = int(bloco.get_size()[1] / configuracao.tamanho_bloco)

    corte_bloco = []
    for linha in range(bloco_y):
        for coluna in range(bloco_x):
            x = coluna * configuracao.tamanho_bloco
            y = linha * configuracao.tamanho_bloco
            corte = pygame.Surface((configuracao.tamanho_bloco,configuracao.tamanho_bloco), flags = pygame.SRCALPHA)
            corte.blit(bloco, (0,0), pygame.Rect(x, y, configuracao.tamanho_bloco, configuracao.tamanho_bloco))
            corte_bloco.append(corte)

    return corte_bloco