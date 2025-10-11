import pygame
import menu

# Definir ações dos botões
def iniciar_jogo():
    print("aqui fica a tela de inicio")
    

def opcoes():
    print("aqui vai ficar a tela de opção")

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
    menu.Botao(540, 540, "imagens/play.png", "imagens/play.png", sair)
]

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
        if acao:
            acao()
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()