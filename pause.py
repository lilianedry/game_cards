# pause.py
import pygame
import sys

def pause_tela(screen):
    # assume pygame já iniciado
    clock = pygame.time.Clock()

    # --- Fontes ---
    fonte_path = "imagens/Silkscreen.ttf"
    try:
        fonte_titulo = pygame.font.Font(fonte_path, 30)
        fonte_botao = pygame.font.Font(fonte_path, 22)
    except Exception:
        fonte_titulo = pygame.font.Font(None, 50)
        fonte_botao = pygame.font.Font(None, 28)
        print("⚠️ Fonte Silkscreen nao encontrada, usando padrao.")

    # --- Cores ---
    VERDE = (50, 100, 50)
    BRANCO = (245, 245, 245)
    LINE_COLOR = (150, 150, 150)
    BG_ALPHA = 225

    # fundo e logo (fallbacks)
    try:
        fundo = pygame.image.load("imagens/background.png").convert()
        fundo = pygame.transform.smoothscale(fundo, screen.get_size())
    except Exception:
        fundo = pygame.Surface(screen.get_size())
        fundo.fill((230, 230, 230))

    try:
        logo = pygame.image.load("imagens/logo.png").convert_alpha()
        logo = pygame.transform.smoothscale(logo, (300, 170))
    except Exception:
        logo = pygame.Surface((300,170), pygame.SRCALPHA)
        logo.fill((200,200,200,0))

    # caixa central translúcida
    caixa_w, caixa_h = int(screen.get_width()*0.78), int(screen.get_height()*0.62)
    caixa_x = (screen.get_width() - caixa_w) // 2
    caixa_y = (screen.get_height() - caixa_h) // 2
    caixa = pygame.Surface((caixa_w, caixa_h), pygame.SRCALPHA)
    caixa.fill((225, 225, 225, BG_ALPHA))

    # Titulo e botao X (dentro da caixa)
    texto_titulo = fonte_titulo.render("PAUSADO", True, VERDE)
    pos_titulo_x = caixa_x + 40
    pos_titulo_y = caixa_y + 20

    texto_x = fonte_titulo.render("X", True, VERDE)
    largura_x = texto_x.get_width()
    altura_x = texto_x.get_height()
    pos_x_x = caixa_x + caixa_w - 40 - largura_x
    pos_y_x = pos_titulo_y
    botao_x = pygame.Rect(pos_x_x, pos_y_x, largura_x, altura_x)

    # Botões SALVAR e SAIR (tamanho e posição de acordo com sua UI)
    bot_salvar = pygame.Rect(caixa_x + (caixa_w-360)//2, caixa_y + caixa_h//2 - 30, 360, 72)
    bot_sair  = pygame.Rect(caixa_x + (caixa_w-360)//2, caixa_y + caixa_h//2 + 60, 360, 72)

    def desenhar_pill(surface, texto, rect, cor_texto, hover=False):
        """
        desenha um botão em estilo 'pill' (fundo branco, sombra e texto verde)
        hover altera a sombra e deslocamento para parecer que o botão sobe.
        """

        # shadow surface
        shadow_surf = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
        # cor da sombra com alpha
        shadow_color = (0, 0, 0, 80)
        pygame.draw.rect(shadow_surf, shadow_color, shadow_surf.get_rect(), border_radius=rect.height//2)

        # offsets: quando hover, sombra menor e mais perto; quando normal, sombra maior e mais deslocada
        if hover:
            shadow_offset = (3, 3)
            pill_offset = (0, -3)  # sobe
        else:
            shadow_offset = (6, 6)
            pill_offset = (0, 0)

        # blitar sombra
        surface.blit(shadow_surf, (rect.x + shadow_offset[0], rect.y + shadow_offset[1]))

        # draw pill (fundo branco)
        pill_rect = pygame.Rect(rect.x + pill_offset[0], rect.y + pill_offset[1], rect.width, rect.height)
        pygame.draw.rect(surface, BRANCO, pill_rect, border_radius=pill_rect.height//2)
        # leve contorno sutil
        pygame.draw.rect(surface, (200,200,200), pill_rect, width=2, border_radius=pill_rect.height//2)

        # render do texto (tentar usar fonte_botao, e reduzir se for maior que o botão)
        text_surf = fonte_botao.render(texto, True, cor_texto)
        # se texto maior que o botão, reduzimos proporcionalmente
        max_text_width = pill_rect.width - 30
        if text_surf.get_width() > max_text_width:
            scale = max_text_width / text_surf.get_width()
            new_w = int(text_surf.get_width() * scale)
            new_h = int(text_surf.get_height() * scale)
            text_surf = pygame.transform.smoothscale(text_surf, (new_w, new_h))

        # posicione centralizado
        text_rect = text_surf.get_rect(center=pill_rect.center)
        surface.blit(text_surf, text_rect)

    # Acao que sera retornada ao chamador de pause_tela:
    # 'resume' = voltar ao jogo, 'menu' = sair para menu
    acao_pos_loop = None
    mensagem = ""

    rodando = True
    while rodando:
        mx, my = pygame.mouse.get_pos()
        hover_salvar = bot_salvar.collidepoint((mx, my))
        hover_sair = bot_sair.collidepoint((mx, my))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    acao_pos_loop = "resume"
                    rodando = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                # clique do mouse
                mx, my = event.pos
                if botao_x.collidepoint((mx, my)):
                    acao_pos_loop = "resume"
                    rodando = False
                elif bot_salvar.collidepoint((mx, my)):
                    # Aqui voce integra o salvamento real; por agora so mostra feedback
                    mensagem = "Progresso salvo com sucesso!"
                elif bot_sair.collidepoint((mx, my)):
                    acao_pos_loop = "menu"
                    rodando = False

        # redesenho
        screen.blit(fundo, (0, 0))
        screen.blit(logo, (80, 10))
        screen.blit(caixa, (caixa_x, caixa_y))
        screen.blit(texto_titulo, (pos_titulo_x, pos_titulo_y))
        screen.blit(texto_x, (pos_x_x, pos_y_x))
        pygame.draw.line(screen, LINE_COLOR, (pos_titulo_x, pos_titulo_y + 50), (caixa_x + caixa_w - 20, pos_titulo_y + 50), 2)

        # desenha botões no estilo "pill" branco com sombra e texto verde
        desenhar_pill(screen, "SALVAR PROGRESSO", bot_salvar, VERDE, hover_salvar)
        desenhar_pill(screen, "SAIR", bot_sair, VERDE, hover_sair)

        if mensagem:
            msg_surf = fonte_botao.render(mensagem, True, VERDE)
            msg_rect = msg_surf.get_rect(center=(screen.get_width() // 2, bot_sair.bottom + 30))
            screen.blit(msg_surf, msg_rect)

        pygame.display.flip()
        clock.tick(60)

    # retorna a acao escolhida ao chamador (jogo.py)
    return acao_pos_loop or "resume"
