import pygame
import menu
import ajustes
import ajuda
import jogo
import json
import os

def retomar_progresso():
    """Le o arquivo de progresso salvo e retoma o jogo."""
    if not os.path.exists("progresso.json"):
        print("Nenhum progresso salvo encontrado. Iniciando novo jogo...")
        return jogo.rodar_jogo(screen)

    try:
        with open("progresso.json", "r", encoding="utf-8") as f:
            progresso = json.load(f)
        print("✅ Progresso carregado:", progresso)
        return jogo.rodar_jogo(screen, progresso)
    except Exception as e:
        print(f"❌ Erro ao carregar progresso: {e}")
        return jogo.rodar_jogo(screen)


def iniciar_jogo():
    """Inicia um novo jogo do zero."""
    return jogo.rodar_jogo(screen)


def opcoes():
    ajustes.ajustes_tela(screen)


def ajuda_acao():
    ajuda.ajuda_tela(screen)


def sair():
    pygame.quit()
    exit()


# --- Inicializacao ---
pygame.init()
screen = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("Meu Jogo")
clock = pygame.time.Clock()

# --- Botoes de menu principal ---
botoes = [
    menu.Botao(460, 340, 360, 72, "RETOMAR PROGRESSO", retomar_progresso),
    menu.Botao(460, 430, 360, 72, "INICIAR JOGO", iniciar_jogo),
    menu.Botao(460, 520, 360, 72, "SAIR", sair)
]

# --- Icones padronizados (40x40) ---
try:
    icone_ajuste = pygame.image.load("imagens/ajuste.png").convert_alpha()
    icone_ajuste = pygame.transform.smoothscale(icone_ajuste, (40, 40))

    icone_ajuda = pygame.image.load("imagens/ajuda.png").convert_alpha()
    icone_ajuda = pygame.transform.smoothscale(icone_ajuda, (40, 40))
except Exception:
    icone_ajuste = pygame.Surface((40, 40))
    icone_ajuda = pygame.Surface((40, 40))
    icone_ajuste.fill((180, 180, 180))
    icone_ajuda.fill((180, 180, 180))

# --- Posicoes dos icones ---
ajuste_rect = icone_ajuste.get_rect(topleft=(20, 20))
ajuda_rect = icone_ajuda.get_rect(topright=(1260, 20))  # alinhado ao canto direito

# --- Loop principal ---
running = True
while running:
    eventos = pygame.event.get()
    for event in eventos:
        if event.type == pygame.QUIT:
            running = False

    screen.fill((0, 0, 0))

    # Desenha o menu principal
    acao = menu.desenhar_tela(screen, botoes, eventos)

    # Desenha os icones padronizados
    screen.blit(icone_ajuste, ajuste_rect)
    screen.blit(icone_ajuda, ajuda_rect)

    # Detecta cliques nos icones
    for event in eventos:
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if ajuste_rect.collidepoint(event.pos):
                opcoes()
            elif ajuda_rect.collidepoint(event.pos):
                ajuda_acao()

    # Executa acao dos botoes
    if acao:
        acao()

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
