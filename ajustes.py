import pygame

def ajustes_tela(screen, estado_global):
    pygame.init()
    clock = pygame.time.Clock()

    # Fonte
    try:
        fonte = pygame.font.Font("imagens/PixelOperator8.ttf", 22)
    except:
        fonte = pygame.font.Font(None, 22)

    # Cores
    VERDE = (50, 100, 50)
    ROXO = (80, 0, 80)
    CINZA = (240, 240, 240)
    LINE_COLOR = (150, 150, 150)

    largura = screen.get_width()
    altura = screen.get_height()

    # Fundo e logo
    fundo = pygame.image.load("imagens/background.png").convert()
    fundo = pygame.transform.scale(fundo, (largura, altura))

    logo = pygame.image.load("imagens/logo.png").convert_alpha()
    logo = pygame.transform.scale(logo, (300, 170))

    # Caixa translúcida centralizada
    caixa_w, caixa_h = int(largura * 0.78), int(altura * 0.62)
    caixa_x = (largura - caixa_w) // 2
    caixa_y = (altura - caixa_h) // 2

    padding = 60  # novas margens internas

    # Estado atual das opções
    musica_ativa = estado_global['musica_ativa']
    efeito_ativo = estado_global['efeito_ativo']

    # Carregar som de clique APENAS se efeito_ativo = True
    som_click = None
    if efeito_ativo:
        try:
            som_click = pygame.mixer.Sound("imagens/click.wav")
        except:
            print("⚠️ Arquivo de som 'click.wav' não encontrado.")

    # Botões posicionados com margens maiores
    botao_musica = pygame.Rect(caixa_x + caixa_w - padding - 70, caixa_y + padding + 70, 70, 35)
    botao_efeitos = pygame.Rect(caixa_x + caixa_w - padding - 70, caixa_y + padding + 140, 70, 35)

    botao_x = pygame.Rect(0, 0, 0, 0)

    rodando = True
    while rodando:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                rodando = False

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:

                # --- Botão X ---
                if botao_x.collidepoint(event.pos):
                    rodando = False

                # --- Música ---
                elif botao_musica.collidepoint(event.pos):
                    musica_ativa = not musica_ativa
                    estado_global['musica_ativa'] = musica_ativa

                    if musica_ativa:
                        pygame.mixer.music.unpause()
                    else:
                        pygame.mixer.music.pause()

                    if efeito_ativo and som_click:
                        som_click.play()

                # --- Efeitos Sonoros ---
                elif botao_efeitos.collidepoint(event.pos):
                    efeito_ativo = not efeito_ativo
                    estado_global['efeito_ativo'] = efeito_ativo

                    # Atualizar som_click dinamicamente
                    if efeito_ativo:
                        try:
                            som_click = pygame.mixer.Sound("imagens/click.wav")
                        except:
                            som_click = None
                    else:
                        som_click = None

                    if efeito_ativo and som_click:
                        som_click.play()

        # --- Desenho da tela ---
        screen.blit(fundo, (0, 0))
        screen.blit(logo, (80, 10))

        caixa = pygame.Surface((caixa_w, caixa_h), pygame.SRCALPHA)
        caixa.fill((225, 225, 225, 225))
        screen.blit(caixa, (caixa_x, caixa_y))

        # Título
        texto_titulo = fonte.render("Ajustes", True, VERDE)
        pos_titulo_x = caixa_x + padding
        pos_titulo_y = caixa_y + padding
        screen.blit(texto_titulo, (pos_titulo_x, pos_titulo_y))

        # Botão X
        texto_x = fonte.render("X", True, VERDE)
        w_x, h_x = texto_x.get_size()
        pos_x_x = caixa_x + caixa_w - padding - w_x
        pos_y_x = pos_titulo_y
        botao_x = pygame.Rect(pos_x_x, pos_y_x, w_x, h_x)
        screen.blit(texto_x, (pos_x_x, pos_y_x))

        # Linha abaixo do título
        pygame.draw.line(
            screen, LINE_COLOR,
            (pos_titulo_x, pos_titulo_y + 45),
            (caixa_x + caixa_w - padding, pos_titulo_y + 45),
            2
        )

        # Textos
        screen.blit(fonte.render("Música", True, VERDE), (caixa_x + padding, caixa_y + padding + 70))
        screen.blit(fonte.render("Efeitos Sonoros", True, VERDE), (caixa_x + padding, caixa_y + padding + 140))

        # ----- Botões toggle -----
        # Música
        pygame.draw.rect(screen, CINZA, botao_musica, border_radius=15)
        pygame.draw.circle(
            screen,
            VERDE if musica_ativa else ROXO,
            (botao_musica.x + (50 if musica_ativa else 20), botao_musica.y + 17),
            14
        )

        # Efeitos sonoros
        pygame.draw.rect(screen, CINZA, botao_efeitos, border_radius=15)
        pygame.draw.circle(
            screen,
            VERDE if efeito_ativo else ROXO,
            (botao_efeitos.x + (50 if efeito_ativo else 20), botao_efeitos.y + 17),
            14
        )

        pygame.display.flip()
        clock.tick(60)
