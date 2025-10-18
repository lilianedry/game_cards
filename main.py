import pygame
import menu
import ajustes
import ajuda

# --- Ações dos botões ---
def iniciar_jogo():
    print("aqui fica a tela de inicio")

def opcoes():
    ajustes.ajustes_tela(screen)

def ajuda_acao():
    ajuda.ajuda_tela(screen)

def sair():
    pygame.quit()
    exit()

pygame.init()
screen = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("Meu Jogo")
clock = pygame.time.Clock()

botoes = [
    menu.Botao(540, 400, "imagens/play.png", "imagens/play.png", iniciar_jogo),
    menu.Botao(540, 470, "imagens/ajustes.png", "imagens/ajustes.png", opcoes),
    menu.Botao(540, 540, "imagens/sair.png", "imagens/sair.png", sair)
]


botao_ajuda = menu.Botao(
    1200, 20,
    "imagens/ajuda.png",  
    "imagens/ajuda.png",  
    ajuda_acao 
)

running = True
estado = "menu"

while running:
    eventos = pygame.event.get()
    
    for event in eventos:
        if event.type == pygame.QUIT:
            running = False

    screen.fill((0, 0, 0))  
    
    if estado == "menu":
        acao = menu.desenhar_tela(screen, botoes, eventos)

        # Atualiza e desenha o botão de ajuda manualmente
        pos_mouse = pygame.mouse.get_pos()
        botao_ajuda.atualizar(pos_mouse)
        botao_ajuda.desenhar(screen)

        for evento in eventos:
            acao_ajuda = botao_ajuda.verificar_clique(pos_mouse, evento)
            if acao_ajuda:
                acao_ajuda()

        if acao:
            acao()
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
