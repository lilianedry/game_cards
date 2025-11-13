# fim_de_jogo.py
import pygame
import sys

def tela_fim_de_jogo(screen, venceu=False):
    """
    Tela de fim de jogo — exibida ao ganhar ou perder.
    Opcoes:
      - REINICIAR → reinicia o jogo (retorna "reiniciar")
      - PAGINA INICIAL → volta para o main.py (retorna "menu")
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
        print("⚠️ Fonte Silkscreen nao encontrada, usando padrao.")

    # --- Cores ---
    VERDE = (50, 100, 50)
    BRANCO = (245, 245, 245)
    LINE_COLOR = (150, 150, 150)
    BG_ALPHA = 225

    largura, altura = screen.get_size()

    # --- Fundo principal ---
    try:
        fundo = pygame.image.load("imagens/background.png").convert()
        fundo = pygame.transform.smoothscale(fundo, (largura, altura))
    except Exception:
        fundo = pygame.Surface((largura, altura))
        fundo.fill((230, 230, 230))

    # --- Caixa translúcida ---
    caixa_w, caixa_h = int(largura * 0.55), int(altura * 0.45)
    caixa_x = (largura - caixa_w) // 2
    caixa_y = (altura - caixa_h) // 2
    caixa = pygame.Surface((caixa_w, caixa_h), pygame.SRCALPHA)
    caixa.fill((225, 225, 225, BG_ALPHA))

    # --- Título ---
    texto_titulo = fonte_titulo.render("Fim de jogo", True, VERDE)
    pos_titulo_x = caixa_x + (caixa_w // 2 - texto_titulo.get_width() // 2)
    pos_titulo_y = caixa_y + 40
    linha_y = pos_titulo_y + 45

    # --- Mensagem ---
    if venceu:
        msg = "Parabéns, você salvou o planeta!!"
    else:
        msg = "Uma ODS chegou a zero. Fim de jogo!"
    texto_msg = fonte_botao.render(msg, True, VERDE)
    texto_msg_rect = texto_msg.get_rect(center=(largura // 2, linha_y + 55))

    # --- Botoes lado a lado ---
    espacamento = 40
    largura_botao = 240
    altura_botao = 60
    centro_x = largura // 2
    y_botoes = caixa_y + caixa_h - 110

    bot_reiniciar = pygame.Rect(centro_x - largura_botao - espacamento // 2, y_botoes, largura_botao, altura_botao)
    bot_menu = pygame.Rect(centro_x + espacamento // 2, y_botoes, largura_botao, altura_botao)

    def desenhar_pill(surface, texto, rect, cor_texto, hover=False):
        sombra = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
        pygame.draw.rect(sombra, (0, 0, 0, 70), sombra.get_rect(), border_radius=rect.height // 2)
        offset_sombra = (3, 3) if hover else (6, 6)
        offset_pill = (0, -2) if hover else (0, 0)
        surface.blit(sombra, (rect.x + offset_sombra[0], rect.y + offset_sombra[1]))

        pill_rect = pygame.Rect(rect.x + offset_pill[0], rect.y + offset_pill[1], rect.width, rect.height)
        pygame.draw.rect(surface, BRANCO, pill_rect, border_radius=pill_rect.height // 2)
        pygame.draw.rect(surface, (200, 200, 200), pill_rect, width=2, border_radius=pill_rect.height // 2)

        text_surf = fonte_botao.render(texto, True, cor_texto)
        text_rect = text_surf.get_rect(center=pill_rect.center)
        surface.blit(text_surf, text_rect)

    rodando = True
    acao = None

    while rodando:
        mx, my = pygame.mouse.get_pos()
        hover_reiniciar = bot_reiniciar.collidepoint((mx, my))
        hover_menu = bot_menu.collidepoint((mx, my))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if bot_reiniciar.collidepoint(event.pos):
                    acao = "reiniciar"
                    rodando = False
                elif bot_menu.collidepoint(event.pos):
                    acao = "menu"
                    rodando = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                acao = "menu"
                rodando = False

        # --- Desenho completo ---
        screen.blit(fundo, (0, 0))
        screen.blit(caixa, (caixa_x, caixa_y))
        screen.blit(texto_titulo, (pos_titulo_x, pos_titulo_y))
        pygame.draw.line(screen, LINE_COLOR, (caixa_x + 40, linha_y), (caixa_x + caixa_w - 40, linha_y), 2)
        screen.blit(texto_msg, texto_msg_rect)
        desenhar_pill(screen, "REINICIAR", bot_reiniciar, VERDE, hover_reiniciar)
        desenhar_pill(screen, "PAGINA INICIAL", bot_menu, VERDE, hover_menu)

        pygame.display.flip()
        clock.tick(60)

    return acao
