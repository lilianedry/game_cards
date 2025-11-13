import pygame

def ajuda_tela(screen):
    pygame.init()
    clock = pygame.time.Clock()

    try:
        fonte_titulo = pygame.font.Font("imagens/PixelOperator8.ttf", 22)
        fonte_texto = pygame.font.Font("imagens/PixelOperator8.ttf", 17)
    except:
        fonte_titulo = pygame.font.Font(None, 22)
        fonte_texto = pygame.font.Font(None, 17)

    VERDE = (50, 100, 50)
    LINE_COLOR = (150, 150, 150)

    largura = screen.get_width()
    altura = screen.get_height()

    textos = [
        "Ao iniciar o jogo, uma carta com uma pergunta aparece no centro da tela.",
        "Arraste a carta para a DIREITA para APROVAR a proposta ou para a ESQUERDA para REJEITAR.",
        "Cada decisão altera as barras no topo da tela: Pobreza, Saúde, Educação e Vida Terrestre.",
        "Mantenha os indicadores equilibrados. Se algum chegar a zero, o jogo termina e você perde.",
    ]

    caixa_w, caixa_h = int(largura * 0.78), int(altura * 0.62)
    caixa_x = (largura - caixa_w) // 2
    caixa_y = (altura - caixa_h) // 2

    botao_x = pygame.Rect(0, 0, 0, 0)

    def render_text_wrapped(surface, text, font, color, rect, line_spacing=8):
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
            surf = font.render(line, True, color)
            surface.blit(surf, (rect.x, y))
            y += font.get_height() + line_spacing

    rodando = True
    while rodando:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                rodando = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if botao_x.collidepoint(event.pos):
                    rodando = False

        fundo = pygame.image.load("imagens/background.png").convert()
        fundo = pygame.transform.scale(fundo, (largura, altura))
        screen.blit(fundo, (0, 0))

        logo = pygame.image.load("imagens/logo.png").convert_alpha()
        logo = pygame.transform.scale(logo, (300, 170))
        screen.blit(logo, (80, 10))

        caixa = pygame.Surface((caixa_w, caixa_h), pygame.SRCALPHA)
        caixa.fill((225, 225, 225, 225))
        screen.blit(caixa, (caixa_x, caixa_y))

        # Margens maiores
        padding = 60

        texto_titulo = fonte_titulo.render("Ajuda", True, VERDE)
        pos_titulo_x = caixa_x + padding
        pos_titulo_y = caixa_y + padding
        screen.blit(texto_titulo, (pos_titulo_x, pos_titulo_y))

        texto_x = fonte_titulo.render("X", True, VERDE)
        w_x, h_x = texto_x.get_size()
        pos_x_x = caixa_x + caixa_w - padding - w_x
        pos_y_x = pos_titulo_y
        botao_x = pygame.Rect(pos_x_x, pos_y_x, w_x, h_x)
        screen.blit(texto_x, (pos_x_x, pos_y_x))

        pygame.draw.line(
            screen, LINE_COLOR,
            (pos_titulo_x, pos_titulo_y + 45),
            (caixa_x + caixa_w - padding, pos_titulo_y + 45),
            2
        )

        y_inicial = pos_titulo_y + 80  # maior espaço abaixo do título
        for texto in textos:
            texto_rect = pygame.Rect(
                caixa_x + padding,
                y_inicial,
                caixa_w - padding * 2,
                0
            )
            render_text_wrapped(screen, texto, fonte_texto, VERDE, texto_rect)
            y_inicial += 95  # mais espaçamento entre blocos

        pygame.display.flip()
        clock.tick(60)
