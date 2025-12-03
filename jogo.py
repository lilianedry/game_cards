import pygame
import sys
import os
import textwrap
import ajustes
import pause
import fim_de_jogo
import random


def load_image_safe(path, size=None, alpha=True):
    try:
        img = pygame.image.load(path)
        img = img.convert_alpha() if alpha else img.convert()
        if size:
            img = pygame.transform.smoothscale(img, size)
        return img
    except Exception:
        w, h = size if size else (100, 100)
        surf = pygame.Surface((w, h), pygame.SRCALPHA)
        surf.fill((200, 200, 200, 255))
        pygame.draw.rect(surf, (160, 160, 160), (0, 0, w, h), 3)
        return surf


def wrap_text_lines(text, font, max_width):
    wrapper = textwrap.TextWrapper()
    sample = font.size("M")[0] or 10
    est_chars = max(10, int(max_width / sample))
    wrapper.width = est_chars
    lines = []
    for paragraph in text.split("\n"):
        lines.extend(wrapper.wrap(paragraph))
        if paragraph != text.split("\n")[-1]:
            lines.append("")
    return lines


def render_multiline_center(surface, lines, font, color, centerx, y_top, line_spacing=6):
    y = y_top
    for line in lines:
        rendered = font.render(line, True, color)
        rect = rendered.get_rect(centerx=centerx)
        rect.top = y
        surface.blit(rendered, rect)
        y += rendered.get_height() + line_spacing
    return y


def calcular_altura_texto(lines, font, line_spacing=6):
    h = 0
    for line in lines:
        h += font.size(line)[1] + line_spacing
    return max(0, h - line_spacing)


def criar_deck_cartas():
    # teu baralho de cartas, igual ao que você já tinha
    cards = [
        {
            "text": "A população mais pobre enfrenta escassez após uma seca. Você libera auxílio emergencial nacional?",
            "right": [["ODS1", 2], ["ODS15", 1]],
            "left": [["ODS1", -2], ["ODS3", -1]]
        },
        {
            "text": "Um surto ameaça a população rural. Tornar a vacina obrigatória?",
            "right": [["ODS3", 2], ["ODS1", -1]],
            "left": [["ODS3", -2], ["ODS1", 1]]
        },
        {
            "text": "Investir em energia solar e hortas nas escolas públicas?",
            "right": [["ODS4", 2], ["ODS15", 1], ["ODS1", -2]],
            "left": [["ODS4", -2], ["ODS1", 2]]
        },
        {
            "text": "Autorizar a ampliação do cultivo em reservas naturais para aumentar a produção de alimentos?",
            "right": [["ODS1", 2], ["ODS15", -3], ["ODS3", -1]],
            "left": [["ODS15", 2], ["ODS1", -2]]
        },
        {
            "text": "Implementar ensino remoto obrigatório para áreas rurais?",
            "right": [["ODS4", 2], ["ODS3", -2], ["ODS15", -1]],
            "left": [["ODS4", -2], ["ODS15", 1]]
        },
        {
            "text": "Autorizar novos pesticidas para aumentar a produção agrícola?",
            "right": [["ODS1", 2], ["ODS15", -2], ["ODS3", -2]],
            "left": [["ODS15", 2], ["ODS3", 1], ["ODS1", -1]]
        },
        {
            "text": "Criar um programa nacional de profissionais em medicina ambiental?",
            "right": [["ODS3", 2], ["ODS15", 1], ["ODS1", -2]],
            "left": [["ODS3", -2], ["ODS1", 1]]
        },
        {
            "text": "Obrigar cada empresa a plantar árvores proporcionalmente ao número de funcionários?",
            "right": [["ODS15", 2], ["ODS1", -2], ["ODS4", 1]],
            "left": [["ODS1", 2], ["ODS15", -2]]
        },
        {
            "text": "Reduzir o consumo de ultraprocessados, mesmo que afete empregos na indústria?",
            "right": [["ODS3", 2], ["ODS1", -3], ["ODS4", -1]],
            "left": [["ODS1", 2], ["ODS3", -1]]
        },
        {
            "text": "Criar renda básica para quem cuida de áreas de reflorestamento?",
            "right": [["ODS1", -2], ["ODS15", 1], ["ODS4", -2]],
            "left": [["ODS1", 2], ["ODS4", 1]]
        },
        {
            "text": "O governo deve reduzir drasticamente verbas de setores sociais para equilibrar as contas públicas?",
            "right": [["ODS1", 3], ["ODS4", -2], ["ODS3", -1]],
            "left": [["ODS1", 1], ["ODS15", -1]]
        },
        {
            "text": "Promover injeção massiva de capital em indústrias, com flexibilização das leis ambientais?",
            "right": [["ODS1", 3], ["ODS15", -3], ["ODS3", -2]],
            "left": [["ODS15", 2], ["ODS1", -2]]
        },
        {
            "text": "Permitir mineração em terras indígenas para gerar royalties para as comunidades?",
            "right": [["ODS1", 2], ["ODS15", -3], ["ODS4", -1]],
            "left": [["ODS15", 2], ["ODS1", -2], ["ODS3", -1]]
        },
        {
            "text": "Reduzir a idade penal para combater a violência, mesmo afetando programas sociais?",
            "right": [["ODS3", 1], ["ODS4", -2], ["ODS1", -2]],
            "left": [["ODS4", 1], ["ODS1", 1], ["ODS3", -1]]
        },
        {
            "text": "Investir pesado em armamento para a segurança pública?",
            "right": [["ODS3", 1], ["ODS1", -3], ["ODS4", -1]],
            "left": [["ODS1", 2], ["ODS4", 1], ["ODS3", -1]]
        },
        {
            "text": "Permitir cultivo transgênico em larga escala para combater a fome?",
            "right": [["ODS1", 2], ["ODS15", -2], ["ODS3", -1]],
            "left": [["ODS15", 2], ["ODS1", -1], ["ODS3", 1]]
        },
        {
            "text": "Implementar pedágio urbano para reduzir congestionamentos e poluição?",
            "right": [["ODS15", 2], ["ODS3", 1], ["ODS1", -2]],
            "left": [["ODS1", 2], ["ODS15", -1], ["ODS4", -1]]
        },
        {
            "text": "Obrigar empresas a oferecer creches gratuitas para suas funcionárias?",
            "right": [["ODS4", 2], ["ODS1", 1], ["ODS3", -2]],
            "left": [["ODS3", 2], ["ODS4", -2], ["ODS1", -1]]
        },
        {
            "text": "Destinar verba da saúde para campanhas de prevenção em vez de tratamentos?",
            "right": [["ODS3", 1], ["ODS4", 1], ["ODS1", -2]],
            "left": [["ODS1", 2], ["ODS3", -2], ["ODS4", -1]]
        },
        {
            "text": "Permitir queimadas controladas para agricultura tradicional?",
            "right": [["ODS1", 2], ["ODS15", -3], ["ODS3", -2]],
            "left": [["ODS15", 3], ["ODS1", -2], ["ODS3", 1]]
        },
        {
            "text": "Implementar semana de quatro dias nas escolas públicas para reduzir custos?",
            "right": [["ODS4", -2], ["ODS1", 2], ["ODS15", 1]],
            "left": [["ODS4", 2], ["ODS1", -2], ["ODS3", -1]]
        },
        {
            "text": "Aprovar lei que permite trabalho infantil em negócios familiares?",
            "right": [["ODS1", 2], ["ODS4", -3], ["ODS3", -2]],
            "left": [["ODS4", 2], ["ODS3", 1], ["ODS1", -2]]
        },
        {
            "text": "Permitir o patenteamento de sementes nativas por multinacionais?",
            "right": [["ODS1", 1], ["ODS15", -3], ["ODS4", -1]],
            "left": [["ODS15", 2], ["ODS1", -1], ["ODS4", 1]]
        },
        {
            "text": "Reduzir proteções trabalhistas para atrair investimentos estrangeiros?",
            "right": [["ODS1", 3], ["ODS3", -2], ["ODS4", -1]],
            "left": [["ODS3", 2], ["ODS4", 1], ["ODS1", -2]]
        },
        {
            "text": "Implementar racionamento de água em períodos de crise hídrica?",
            "right": [["ODS15", 2], ["ODS3", -2], ["ODS1", -1]],
            "left": [["ODS3", 2], ["ODS1", 1], ["ODS15", -2]]
        },
        {
            "text": "Permitir publicidade infantil para aumentar as vendas de produtos nacionais?",
            "right": [["ODS1", 2], ["ODS4", -2], ["ODS3", -1]],
            "left": [["ODS4", 2], ["ODS3", 1], ["ODS1", -1]]
        },
    ]
    return cards


def rodar_jogo(screen, estado_global=None, progresso_carregado=None):
    clock = pygame.time.Clock()

    if estado_global is None:
        estado_global = {}

    # Som
    som_arrastar = None
    if estado_global.get("efeito_ativo", True):
        try:
            som_arrastar = pygame.mixer.Sound("sons/carta.mp3")
        except Exception:
            som_arrastar = None

    # Fontes
    try:
        FONT = pygame.font.Font(os.path.join("imagens", "PixelOperator8.ttf"), 15)
        FONT_BIG = pygame.font.Font(os.path.join("imagens", "PixelOperator8.ttf"), 20)
    except Exception:
        FONT = pygame.font.SysFont("dejavusans", 15)
        FONT_BIG = pygame.font.SysFont("dejavusans", 20)

    SCREEN_W, SCREEN_H = screen.get_size()

    ICON_SIZE = int(SCREEN_W * 0.04)
    CARD_W = int(SCREEN_W * 0.20)
    CARD_H = int(SCREEN_H * 0.42)
    ICON_GAP = int(SCREEN_W * 0.10)

    # Imagens
    background = load_image_safe(os.path.join("imagens", "background.png"), size=(SCREEN_W, SCREEN_H), alpha=False)
    carta_img = load_image_safe(os.path.join("imagens", "carta.png"), size=(CARD_W, CARD_H), alpha=True)
    ajuste_icon = load_image_safe(os.path.join("imagens", "ajuste.png"), size=(40, 40), alpha=True)
    pause_icon = load_image_safe(os.path.join("imagens", "pause.png"), size=(40, 40), alpha=True)

    # Ícones ODS
    ods_icons = {
        "ODS1": load_image_safe(os.path.join("imagens", "economia.png"), size=(ICON_SIZE, ICON_SIZE)),
        "ODS3": load_image_safe(os.path.join("imagens", "saude.png"), size=(ICON_SIZE, ICON_SIZE)),
        "ODS4": load_image_safe(os.path.join("imagens", "educacao.png"), size=(ICON_SIZE, ICON_SIZE)),
        "ODS15": load_image_safe(os.path.join("imagens", "natureza.png"), size=(ICON_SIZE, ICON_SIZE)),
    }

    ajuste_rect = ajuste_icon.get_rect(topright=(SCREEN_W - 20, 20))
    pause_rect = pause_icon.get_rect(topleft=(20, 20))

    # ---------------------------
    # CARREGAR PROGRESSO OU NOVO
    # ---------------------------
    carta_jogo = 10  # alvo para vitória / contagem base
    if progresso_carregado:
        ods = progresso_carregado.get("ods", {"ODS1": 5, "ODS3": 5, "ODS4": 5, "ODS15": 5})
        cards = progresso_carregado.get("cards") or criar_deck_cartas()
        current_index = progresso_carregado.get("current_index", 0)
    else:
        ods = {"ODS1": 5, "ODS3": 5, "ODS4": 5, "ODS15": 5}
        cards = criar_deck_cartas()
        random.shuffle(cards)
        current_index = 0

    # ---------------------------
    # ESTADO VISUAL DA CARTA
    # ---------------------------
    card_rect = carta_img.get_rect(center=(SCREEN_W // 2, SCREEN_H // 2 + 40))
    card_start_pos = card_rect.topleft
    dragging = False
    mouse_offset = (0, 0)
    threshold = SCREEN_W * 0.22
    game_over = False
    win = False
    ods_zerada = None

    # ---------------------------
    # FUNÇÕES AUXILIARES
    # ---------------------------
    def apply_effects(effects):
        for name, delta in effects:
            if name in ods:
                ods[name] = ods.get(name, 0) + delta

    def check_end():
        # alguma ODS zerou?
        for nome, valor in ods.items():
            if valor <= 0:
                return True, False, nome
        # vitória por cartas jogadas
        rem_local = max(0, carta_jogo - current_index)
        if current_index >= carta_jogo or rem_local <= 0:
            return True, True, None
        return False, False, None

    # ---------------------------
    # LOOP PRINCIPAL
    # ---------------------------
    while True:
        # calcula cartas restantes SEMPRE no início do frame
        rem = max(0, carta_jogo - current_index)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                # ajustes
                if ajuste_rect.collidepoint(event.pos):
                    ajustes.ajustes_tela(screen, estado_global)

                # pause (salvar progresso)
                elif pause_rect.collidepoint(event.pos):
                    dados_do_jogo = {
                        "ods": ods,
                        "current_index": current_index,
                        "cards": cards,
                        "rem": rem
                    }
                    acao = pause.pause_tela(screen, dados_do_jogo)
                    if acao == "menu":
                        return

                # começar a arrastar carta
                elif not game_over and card_rect.collidepoint(event.pos):
                    dragging = True
                    mx, my = event.pos
                    mouse_offset = (mx - card_rect.x, my - card_rect.y)

            if event.type == pygame.MOUSEBUTTONUP and event.button == 1 and not game_over:
                if dragging:
                    dragging = False
                    cx = card_rect.centerx
                    center = SCREEN_W // 2

                    if current_index < len(cards):
                        if cx > center + threshold:  # APROVAR
                            if som_arrastar:
                                som_arrastar.play()
                            apply_effects(cards[current_index]["right"])
                            current_index += 1

                        elif cx < center - threshold:  # REJEITAR
                            if som_arrastar:
                                som_arrastar.play()
                            apply_effects(cards[current_index]["left"])
                            current_index += 1

                        else:
                            # volta para o centro se não passou do limite
                            card_rect.topleft = card_start_pos

                        end, won, ods_caiu = check_end()
                        if end:
                            game_over = True
                            win = won
                            ods_zerada = ods_caiu

                        # reseta posição da carta
                        card_rect = carta_img.get_rect(center=(SCREEN_W // 2, SCREEN_H // 2 + 40))
                        card_start_pos = card_rect.topleft

            if event.type == pygame.MOUSEMOTION and dragging and not game_over:
                mx, my = event.pos
                card_rect.x = mx - mouse_offset[0]
                card_rect.y = my - mouse_offset[1]

        # ---------------------------
        # DESENHO DA TELA
        # ---------------------------
        screen.blit(background, (0, 0))

        # ODS no topo
        keys_order = ["ODS15", "ODS1", "ODS4", "ODS3"]
        total_icons = len(keys_order)
        center_x = SCREEN_W // 2
        full_width = (total_icons - 1) * ICON_GAP
        start_x = center_x - full_width // 2
        y_icon = 25
        y_bar = y_icon + ICON_SIZE + 8

        for i, key in enumerate(keys_order):
            x = start_x + i * ICON_GAP
            icon_surf = ods_icons.get(key)
            icon_rect = icon_surf.get_rect(center=(x, y_icon + ICON_SIZE // 2))
            screen.blit(icon_surf, icon_rect)

            bar_w, bar_h = int(ICON_SIZE * 1.5), 10
            bar_x = x - bar_w // 2
            pygame.draw.rect(screen, (210, 210, 210), (bar_x, y_bar, bar_w, bar_h))

            val = max(0, min(ods.get(key, 0), 10))
            fill_w = int((val / 10) * bar_w)
            pygame.draw.rect(screen, (50, 120, 50), (bar_x, y_bar, fill_w, bar_h))

        # botões
        screen.blit(pause_icon, pause_rect)
        screen.blit(ajuste_icon, ajuste_rect)

        # carta + texto
        if not game_over and current_index < len(cards):
            text_block = cards[current_index]["text"]
            max_text_w = min(SCREEN_W * 0.8, CARD_W * 1.8)
            y_text_top = y_bar + 60
            lines = wrap_text_lines(text_block, FONT, max_text_w)
            text_height = calcular_altura_texto(lines, FONT)

            if not dragging:
                card_center_y = max(SCREEN_H // 2 + 40, y_text_top + text_height + CARD_H // 2)
                card_rect.centery = card_center_y
                card_rect.centerx = SCREEN_W // 2
                card_start_pos = card_rect.topleft

            screen.blit(carta_img, card_rect.topleft)
            render_multiline_center(screen, lines, FONT, (20, 60, 20), SCREEN_W // 2, y_text_top)
        else:
            screen.blit(carta_img, card_rect.topleft)

        # cartas restantes
        rem_surf = FONT.render(f"Cartas restantes: {rem}", True, (40, 40, 40))
        rem_rect = rem_surf.get_rect(center=(SCREEN_W // 2, card_rect.bottom + 22))
        screen.blit(rem_surf, rem_rect)

        # feedback aprovar/rejeitar
        if card_rect.centerx > SCREEN_W // 2 + threshold * 0.5:
            screen.blit(FONT_BIG.render("APROVAR", True, (30, 120, 30)),
                        (SCREEN_W - 260, SCREEN_H // 2 + CARD_H // 3))
        elif card_rect.centerx < SCREEN_W // 2 - threshold * 0.5:
            screen.blit(FONT_BIG.render("REJEITAR", True, (150, 30, 30)),
                        (40, SCREEN_H // 2 + CARD_H // 3))

        # fim de jogo
        if game_over:
            escolha = fim_de_jogo.tela_fim_de_jogo(screen, venceu=win, ods_zerada=ods_zerada)
            if escolha == "reiniciar":
                return rodar_jogo(screen, estado_global)
            elif escolha == "menu":
                return

        pygame.display.flip()
        clock.tick(60)
