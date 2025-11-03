import pygame

def ajustes_tela(screen, estado_global):
    pygame.init()
    clock = pygame.time.Clock()

    try:
        fonte = pygame.font.Font("imagens/Silkscreen.ttf", 30)
    except:
        fonte = pygame.font.Font(None, 40)
        print("⚠️ Fonte Silkscreen não encontrada, usando padrão.")

    # Cores
    VERDE = (50, 100, 50)
    ROXO = (80, 0, 80)
    BRANCO = (255, 255, 255)
    CINZA = (240, 240, 240)
    LINE_COLOR = (150,150,150)
    info = pygame.display.Info()
    largura = info.current_w
    altura = info.current_h

    # Estados das opções
    musica_ativa = estado_global['musica_ativa']
    efeito_ativo = estado_global['efeito_ativo']
    linguas = ["Portugues", "Ingles", "Espanhol"]
    indice_lingua = linguas.index(estado_global['lingua'])

    # Imagens
    fundo = pygame.image.load("imagens/background.png").convert()
    fundo = pygame.transform.scale(fundo, (largura, altura))

    logo = pygame.image.load("imagens/logo.png").convert_alpha()
    logo = pygame.transform.scale(logo, (300, 170))

    # Retângulos de interação
    botao_musica = pygame.Rect(850, 340, 60, 30)
    botao_efeitos = pygame.Rect(850, 410, 60, 30)
    # botao_lingua_esq = pygame.Rect(720, 480, 40, 40)
    botao_lingua_dir = pygame.Rect(940, 480, 40, 40)

    rodando = True
    while rodando:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # clique esquerdo
                    if botao_x.collidepoint(event.pos):
                        rodando = False  # volta ao menu
                    elif botao_musica.collidepoint(event.pos):
                        musica_ativa = not musica_ativa
                        estado_global['musica_ativa']=musica_ativa
                        if musica_ativa:
                            pygame.mixer.music.unpause()
                        else:
                            pygame.mixer.music.pause()
                    elif botao_efeitos.collidepoint(event.pos):
                        efeito_ativo = not efeito_ativo
                        estado_global['efeito_ativo']=efeito_ativo
                    # elif botao_lingua_dir.collidepoint(event.pos):
                    #     indice_lingua = (indice_lingua + 1) % len(linguas)
                    # elif botao_lingua_esq.collidepoint(event.pos):
                    #     indice_lingua = (indice_lingua - 1) % len(linguas)

        # Fundo e logo
        screen.blit(fundo, (0, 0))
        screen.blit(logo, (80, 10))   

        # Caixa translúcida central
        caixa = pygame.Surface((1000, 450), pygame.SRCALPHA)
        caixa.fill((225, 225, 225, 225))  # leve transparência
        screen.blit(caixa, (140, 180))

        # Título
        texto_titulo = fonte.render("AJUSTES", True, VERDE)
        pos_titulo_x = 220
        pos_titulo_y = 230
        screen.blit(texto_titulo, (pos_titulo_x, pos_titulo_y))

        # Botão X (alinhado horizontalmente com o título)
        texto_x = fonte.render("X", True, VERDE)
        largura_x = texto_x.get_width()
        altura_x = texto_x.get_height()
        pos_x_x = 1050  # alinhado na lateral oposta
        pos_y_x = pos_titulo_y
        botao_x = pygame.Rect(pos_x_x, pos_y_x, largura_x, altura_x)
        screen.blit(texto_x, (pos_x_x, pos_y_x))

        # Linha divisória
        pygame.draw.line(screen, LINE_COLOR, (pos_titulo_x, 270), (1070, 270), 1)

        # Textos das opções
        texto_musica = fonte.render("MUSICA", True, VERDE)
        screen.blit(texto_musica, (220, 350))

        texto_efeitos = fonte.render("EFEITOS SONOROS", True, VERDE)
        screen.blit(texto_efeitos, (220, 420))

        # texto_lingua = fonte.render("LINGUA", True, VERDE)
        # screen.blit(texto_lingua, (220, 490))

        # Botões toggle
        pygame.draw.rect(screen, CINZA, botao_musica, border_radius=15)
        pygame.draw.circle(screen, VERDE if musica_ativa else ROXO,
                           (botao_musica.x + (45 if musica_ativa else 15), botao_musica.y + 15), 12)

        pygame.draw.rect(screen, CINZA, botao_efeitos, border_radius=15)
        pygame.draw.circle(screen, VERDE if efeito_ativo else ROXO,
                           (botao_efeitos.x + (45 if efeito_ativo else 15), botao_efeitos.y + 15), 12)

        # Setas de idioma
        # seta_esq = fonte.render("<", True, VERDE)
        # seta_dir = fonte.render(">", True, VERDE)
        # screen.blit(seta_esq, (botao_lingua_esq.x + 10, botao_lingua_esq.y + 2))
        # screen.blit(seta_dir, (botao_lingua_dir.x + 30, botao_lingua_dir.y + 2))

        # # Idioma atual
        # texto_lingua_atual = fonte.render(linguas[indice_lingua], True, VERDE)
        # screen.blit(texto_lingua_atual, (botao_lingua_esq.x + 60, botao_lingua_esq.y + 5))

        pygame.display.flip()
        clock.tick(60)
