import pygame

def ajuda_tela(screen):
    pygame.init()
    clock = pygame.time.Clock()

    # --- Fontes SEPARADAS para título e texto ---
    try:
        fonte_titulo = pygame.font.Font("imagens/Silkscreen.ttf", 30)  
        fonte_texto = pygame.font.Font("imagens/Silkscreen.ttf", 15)  
    except:
        fonte_titulo = pygame.font.Font(None, 50)  
        fonte_texto = pygame.font.Font(None, 25)   
        print("⚠️ Fonte Silkscreen não encontrada, usando padrão.")

    # --- Cores ---
    VERDE = (50, 100, 50)
    PRETO = (30, 30, 30)
    CINZA = (240, 240, 240)
    LINE_COLOR = (150, 150, 150)

    icones = {
        "pobreza": pygame.image.load("imagens/ajuda.png").convert_alpha(),
        "saude": pygame.image.load("imagens/ajuda.png").convert_alpha(),
        "educacao": pygame.image.load("imagens/ajuda.png").convert_alpha(),
        "vida": pygame.image.load("imagens/ajuda.png").convert_alpha()
    }

    for chave in icones:
        icones[chave] = pygame.transform.smoothscale(icones[chave], (40, 40))

    textos = [
        ("pobreza", "POBREZA - Mede a desigualdade social. Valores altos indicam crise econômica."),
        ("saude", "SAUDE - Representa o bem-estar da população. Mantenha o equilíbrio."),
        ("educacao", "EDUCACAO - Reflete o acesso ao conhecimento e desenvolvimento do país."),
        ("vida", "VIDA TERRESTRE - Mostra o estado da natureza e dos ecossistemas. Preserve-a.")
    ]

    rodando = True
    while rodando:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 and botao_x.collidepoint(event.pos):
                    rodando = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                rodando = False

        fundo = pygame.image.load("imagens/background.png").convert()
        fundo = pygame.transform.scale(fundo, (1280, 720))
        screen.blit(fundo, (0, 0))

        logo = pygame.image.load("imagens/logo.png").convert_alpha()
        logo = pygame.transform.scale(logo, (300, 170))
        screen.blit(logo, (80, 10))

        caixa = pygame.Surface((1000, 450), pygame.SRCALPHA)
        caixa.fill((225, 225, 225, 225))
        screen.blit(caixa, (140, 180))

        texto_titulo = fonte_titulo.render("AJUDA", True, VERDE)
        pos_titulo_x = 220
        pos_titulo_y = 200  
        screen.blit(texto_titulo, (pos_titulo_x, pos_titulo_y))

        texto_x = fonte_titulo.render("X", True, VERDE)
        largura_x = texto_x.get_width()
        altura_x = texto_x.get_height()
        pos_x_x = 1050
        pos_y_x = pos_titulo_y
        botao_x = pygame.Rect(pos_x_x, pos_y_x, largura_x, altura_x)
        screen.blit(texto_x, (pos_x_x, pos_y_x))

        
        pygame.draw.line(screen, LINE_COLOR, (pos_titulo_x, pos_titulo_y + 50), (1070, pos_titulo_y + 50), 2)

        
        def render_text_wrapped(surface, text, font, color, rect, line_spacing=5):
            words = text.split(' ')
            lines = []
            while words:
                line_words = []
                while words:
                    line_words.append(words.pop(0))
                    fw, _ = font.size(' '.join(line_words + words[:1]))
                    if fw > rect.width:
                        break
                lines.append(' '.join(line_words))

            y = rect.top
            for line in lines:
                line_surf = font.render(line, True, color)
                surface.blit(line_surf, (rect.x, y))
                y += font.get_height() + line_spacing

        
        y_inicial = 280  
        for nome, texto in textos:
            screen.blit(icones[nome], (180, y_inicial))
            texto_rect = pygame.Rect(230, y_inicial, 850, 0)
            render_text_wrapped(screen, texto, fonte_texto, VERDE, texto_rect)  
            y_inicial += 90  

        pygame.display.flip()
        clock.tick(60)