# popup_sair.py
import pygame
import sys

def popup_confirmar_saida(screen):
    """
    Exibe um popup perguntando se o jogador realmente deseja sair.
    Retorna:
      - "sair" → volta ao main.py
      - "cancelar" → volta ao jogo.py
    """
    clock = pygame.time.Clock()

    # --- Fontes ---
    fonte_path = "imagens/PixelOperator8.ttf"
    try:
        fonte_titulo = pygame.font.Font(fonte_path, 20)
        fonte_botao = pygame.font.Font(fonte_path, 15)
    except Exception:
        fonte_titulo = pygame.font.Font(None, 48)
        fonte_botao = pygame.font.Font(None, 32)
        print("⚠️ Fonte Silkscreen não encontrada, usando padrão.")

    # --- Cores ---
    VERDE = (50, 100, 50)
    BRANCO = (245, 245, 245)
    LINE_COLOR = (150, 150, 150)
    BG_ALPHA = 225

    largura, altura = screen.get_size()

    # --- Fundo principal (usa imagem padrão do jogo) ---
    try:
        fundo = pygame.image.load("imagens/background.png").convert()
        fundo = pygame.transform.smoothscale(fundo, (largura, altura))
    except Exception:
        fundo = pygame.Surface((largura, altura))
        fundo.fill((230, 230, 230))

    # --- Camada escurecida ---
    overlay = pygame.Surface((largura, altura), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 120))

    # --- Caixa central translúcida ---
    caixa_w, caixa_h = int(largura * 0.6), int(altura * 0.4)
    caixa_x = (largura - caixa_w) // 2
    caixa_y = (altura - caixa_h) // 2
    caixa = pygame.Surface((caixa_w, caixa_h), pygame.SRCALPHA)
    caixa.fill((225, 225, 225, BG_ALPHA))

    # --- Título ---
    texto_titulo = fonte_titulo.render("Confirmar saída", True, VERDE)
    pos_titulo_x = caixa_x + 40
    pos_titulo_y = caixa_y + 30
    linha_y = pos_titulo_y + 50

    # --- Texto principal ---
    texto_pergunta = fonte_botao.render("Tem certeza que deseja sair do jogo?", True, VERDE)
    texto_pergunta_rect = texto_pergunta.get_rect(center=(largura // 2, linha_y + 70))

    # --- Botões ---
    bot_sair = pygame.Rect(caixa_x + caixa_w // 2 - 180, caixa_y + caixa_h - 110, 160, 60)
    bot_cancelar = pygame.Rect(caixa_x + caixa_w // 2 + 20, caixa_y + caixa_h - 110, 160, 60)

    def desenhar_pill(surface, texto, rect, cor_texto, hover=False):
        sombra = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
        pygame.draw.rect(sombra, (0, 0, 0, 80), sombra.get_rect(), border_radius=rect.height // 2)
        offset_sombra = (3, 3) if hover else (6, 6)
        offset_pill = (0, -3) if hover else (0, 0)
        surface.blit(sombra, (rect.x + offset_sombra[0], rect.y + offset_sombra[1]))

        pill_rect = pygame.Rect(rect.x + offset_pill[0], rect.y + offset_pill[1], rect.width, rect.height)
        pygame.draw.rect(surface, BRANCO, pill_rect, border_radius=pill_rect.height // 2)
        pygame.draw.rect(surface, (200, 200, 200), pill_rect, width=2, border_radius=pill_rect.height // 2)

        text_surf = fonte_botao.render(texto, True, cor_texto)
        text_rect = text_surf.get_rect(center=pill_rect.center)
        surface.blit(text_surf, text_rect)

    rodando = True
    acao = "cancelar"

    while rodando:
        mx, my = pygame.mouse.get_pos()
        hover_sair = bot_sair.collidepoint((mx, my))
        hover_cancelar = bot_cancelar.collidepoint((mx, my))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if bot_sair.collidepoint(event.pos):
                    acao = "sair"
                    rodando = False
                elif bot_cancelar.collidepoint(event.pos):
                    acao = "cancelar"
                    rodando = False

            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                acao = "cancelar"
                rodando = False

        # --- Desenho completo ---
        screen.blit(fundo, (0, 0))
        screen.blit(overlay, (0, 0))
        screen.blit(caixa, (caixa_x, caixa_y))
        screen.blit(texto_titulo, (pos_titulo_x, pos_titulo_y))
        pygame.draw.line(screen, LINE_COLOR, (pos_titulo_x, linha_y), (caixa_x + caixa_w - 40, linha_y), 2)
        screen.blit(texto_pergunta, texto_pergunta_rect)

        desenhar_pill(screen, "Sair", bot_sair, VERDE, hover_sair)
        desenhar_pill(screen, "Cancelar", bot_cancelar, VERDE, hover_cancelar)

        pygame.display.flip()
        clock.tick(60)

    return acao
