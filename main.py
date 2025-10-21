import pygame
import menu
import ajustes
import ajuda
import jogo

# --- Ações dos botões ---
def retomar_progresso():
    print("Retomando progresso salvo... (implementar lógica aqui)")

def iniciar_jogo():
    return jogo.rodar_jogo(screen)

def opcoes():
    ajustes.ajustes_tela(screen)

def ajuda_acao():
    ajuda.ajuda_tela(screen)

def sair():
    pygame.quit()
    exit()

# --- Inicialização ---
pygame.init()
screen = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("Meu Jogo")
clock = pygame.time.Clock()

# --- Botões de menu principal ---
botoes = [
    menu.Botao(460, 340, 360, 72, "RETOMAR PROGRESSO", retomar_progresso),
    menu.Botao(460, 430, 360, 72, "INICIAR JOGO", iniciar_jogo),
    menu.Botao(460, 520, 360, 72, "SAIR", sair)
]

# --- Botões de ícones (ajuste e ajuda) ---
botao_ajuste = menu.Botao(
    10, 10,
    "imagens/ajuste.png",  # imagem normal
    "imagens/ajuste.png",  # imagem hover (pode mudar se quiser efeito)
    opcoes
)

botao_ajuda = menu.Botao(
    1200, 20,
    "imagens/ajuda.png",  
    "imagens/ajuda.png",  
    ajuda_acao
)

# --- Loop principal ---
running = True
estado = "menu"

while running:
    eventos = pygame.event.get()
    
    for event in eventos:
        if event.type == pygame.QUIT:
            running = False

    screen.fill((0, 0, 0))  
    
    if estado == "menu":
        # Desenhar todos os botões do menu
        acao = menu.desenhar_tela(screen, botoes, eventos)

        # Obter posição do mouse
        pos_mouse = pygame.mouse.get_pos()

        # Desenhar e atualizar ícones
        for botao_icon in [botao_ajuste, botao_ajuda]:
            botao_icon.atualizar(pos_mouse)
            botao_icon.desenhar(screen)

            # Verificar clique
            for evento in eventos:
                acao_icon = botao_icon.verificar_clique(pos_mouse, evento)
                if acao_icon:
                    acao_icon()

        # Executar ação de qualquer botão do menu
        if acao:
            acao()
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
