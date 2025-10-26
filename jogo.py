import pygame
import sys
import os
import textwrap
import ajustes  # Tela de ajustes
import pause    # Tela de pause
import fim_de_jogo



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


def rodar_jogo(screen):
    clock = pygame.time.Clock()

    try:
        FONT = pygame.font.Font(os.path.join("imagens", "Silkscreen.ttf"), 20)
        FONT_BIG = pygame.font.Font(os.path.join("imagens", "Silkscreen.ttf"), 30)
    except Exception:
        FONT = pygame.font.SysFont("dejavusans", 20)
        FONT_BIG = pygame.font.SysFont("dejavusans", 30)

    SCREEN_W, SCREEN_H = screen.get_size()

    # --- tamanhos ajustados ---
    ICON_SIZE = int(SCREEN_W * 0.04)  # ícones menores
    CARD_W = int(SCREEN_W * 0.20)     # carta menor
    CARD_H = int(SCREEN_H * 0.42)
    ICON_GAP = int(SCREEN_W * 0.10)

    # --- imagens ---
    background = load_image_safe(os.path.join("imagens", "background.png"), size=(SCREEN_W, SCREEN_H), alpha=False)
    carta_img = load_image_safe(os.path.join("imagens", "carta.png"), size=(CARD_W, CARD_H), alpha=True)
    ajuste_icon = load_image_safe(os.path.join("imagens", "ajuste.png"), size=(40, 40), alpha=True)
    pause_icon = load_image_safe(os.path.join("imagens", "pause.png"), size=(40, 40), alpha=True)

    # --- ícones ODS ---
    ods_icons = {
        "ODS1": load_image_safe(os.path.join("imagens", "economia.png"), size=(ICON_SIZE, ICON_SIZE)),
        "ODS3": load_image_safe(os.path.join("imagens", "saude.png"), size=(ICON_SIZE, ICON_SIZE)),
        "ODS4": load_image_safe(os.path.join("imagens", "educacao.png"), size=(ICON_SIZE, ICON_SIZE)),
        "ODS15": load_image_safe(os.path.join("imagens", "natureza.png"), size=(ICON_SIZE, ICON_SIZE)),
    }

    # --- posições dos botões ---
    ajuste_rect = ajuste_icon.get_rect(topright=(SCREEN_W - 20, 20))
    pause_rect = pause_icon.get_rect(topleft=(20, 20))

    # --- estado inicial ---
    ods = {"ODS1": 5, "ODS3": 5, "ODS4": 5, "ODS15": 5}

    # --- cartas ---
    cards = [
        {"text": "A populacao mais pobre enfrenta escassez apos seca. Voce libera auxilio emergencial nacional?",
         "right": [("ODS1", +1), ("ODS4", -1)],
         "left": [("ODS1", -1)]},
        {"text": "Um surto ameaca a populacao rural. Tornar vacina obrigatoria?",
         "right": [("ODS3", +1), ("ODS4", -1)],
         "left": [("ODS3", -1)]},
        {"text": "Investir em energia solar e hortas nas escolas publicas?",
         "right": [("ODS4", +1), ("ODS15", +1), ("ODS1", -1)],
         "left": [("ODS4", -1)]},
        {"text": "Autorizar ampliar cultivo em reservas naturais?",
         "right": [("ODS1", +1), ("ODS15", -2)],
         "left": [("ODS15", +1), ("ODS1", -1)]},
        {"text": "Em ensino remoto para areas rurais?",
         "right": [("ODS4", +1), ("ODS3", -1)],
         "left": [("ODS4", -1)]},
        {"text": "Autorizar novos pesticidas para aumentar producao?",
         "right": [("ODS1", +1), ("ODS15", -1), ("ODS3", -1)],
         "left": [("ODS15", +1), ("ODS3", +1)]},
        {"text": "Profissionais em medicina ambiental?",
         "right": [("ODS3", +1), ("ODS15", +1), ("ODS1", -1)],
         "left": [("ODS3", -1)]},
        {"text": "Cada empresa planta arvores proporcionalmente?",
         "right": [("ODS15", +1), ("ODS1", -1)],
         "left": [("ODS1", +1), ("ODS15", -1)]},
        {"text": "Reduzir ultraprocessados mesmo que afete industrias?",
         "right": [("ODS3", +1), ("ODS1", -1)],
         "left": [("ODS1", +1), ("ODS3", -1)]},
        {"text": "Renda para quem cuida de reflorestamento?",
         "right": [("ODS1", +1), ("ODS15", +1), ("ODS4", -1)],
         "left": [("ODS1", -1)]},
        {"text": "Governo reduz verbas em setores sociais para equilibrar conta.",
         "right": [("ODS1", -2), ("ODS4", -1)],
         "left": [("ODS1", +1)]},
        {"text": "Injecao de capital, mas com poluicao elevada.",
         "right": [("ODS1", +1), ("ODS15", -2), ("ODS3", -1)],
         "left": [("ODS15", +1)]}
    ]

    # --- carta inicial ---
    card_rect = carta_img.get_rect(center=(SCREEN_W // 2, SCREEN_H // 2 + 40))
    card_start_pos = card_rect.topleft
    dragging = False
    mouse_offset = (0, 0)
    threshold = SCREEN_W * 0.22
    current_index = 0
    game_over = False
    win = False

    # --- funções auxiliares ---
    def apply_effects(effects):
        for name, delta in effects:
            if name in ods:
                ods[name] = ods.get(name, 0) + delta

    def check_end():
        for v in ods.values():
            if v <= 0:
                return True, False
        if current_index >= len(cards):
            return True, True
        return False, False

    # --- loop principal ---
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                # Clique no botão de ajustes
                if ajuste_rect.collidepoint(event.pos):
                    ajustes.ajustes_tela(screen)
                
                # Clique no botão de pause
                elif pause_rect.collidepoint(event.pos):
                    acao = pause.pause_tela(screen)
                    if acao == "menu":
                        print("🔁 Voltando ao menu principal...")
                        return  # Sai de rodar_jogo() e volta ao main.py
                
                # Clique na carta
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
                        if cx > center + threshold:
                            apply_effects(cards[current_index]["right"])
                            current_index += 1
                        elif cx < center - threshold:
                            apply_effects(cards[current_index]["left"])
                            current_index += 1
                        else:
                            card_rect.topleft = card_start_pos
                    end, won = check_end()
                    if end:
                        game_over = True
                        win = won
                    card_rect = carta_img.get_rect(center=(SCREEN_W // 2, SCREEN_H // 2 + 40))
                    card_start_pos = card_rect.topleft

            if event.type == pygame.MOUSEMOTION and dragging and not game_over:
                mx, my = event.pos
                card_rect.x = mx - mouse_offset[0]
                card_rect.y = my - mouse_offset[1]

        # --- fundo ---
        screen.blit(background, (0, 0))

        # --- ícones ODS ---
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

        # --- botões pause e ajustes ---
        screen.blit(pause_icon, pause_rect)
        screen.blit(ajuste_icon, ajuste_rect)

        # --- cartas e textos ---
        if not game_over and current_index < len(cards):
            text_block = cards[current_index]["text"]
            max_text_w = min(SCREEN_W * 0.8, CARD_W * 1.8)
            y_text_top = y_bar + 25
            lines = wrap_text_lines(text_block, FONT, max_text_w)
            text_height = calcular_altura_texto(lines, FONT, line_spacing=6)
            desired_card_top = int(y_text_top + text_height + 10)
            if not dragging:
                card_center_y = max(SCREEN_H // 2 + 40, desired_card_top + CARD_H // 2)
                card_rect.centery = card_center_y
                card_rect.centerx = SCREEN_W // 2
                card_start_pos = card_rect.topleft
            screen.blit(carta_img, card_rect.topleft)
            render_multiline_center(screen, lines, FONT, (20, 60, 20), SCREEN_W // 2, y_text_top, line_spacing=6)
        else:
            screen.blit(carta_img, card_rect.topleft)

        # --- cartas restantes ---
        rem = max(0, len(cards) - current_index)
        rem_surf = FONT.render(f"Cartas restantes: {rem}", True, (40, 40, 40))
        rem_rect = rem_surf.get_rect(center=(SCREEN_W // 2, card_rect.bottom + 22))
        screen.blit(rem_surf, rem_rect)

        # --- feedback visual ---
        if card_rect.centerx > SCREEN_W // 2 + threshold * 0.5:
            screen.blit(FONT_BIG.render("APROVAR ✓", True, (30, 120, 30)), (SCREEN_W - 260, SCREEN_H // 2 + CARD_H // 3))
        elif card_rect.centerx < SCREEN_W // 2 - threshold * 0.5:
            screen.blit(FONT_BIG.render("REJEITAR ✕", True, (150, 30, 30)), (40, SCREEN_H // 2 + CARD_H // 3))

        # --- fim de jogo ---
        if game_over:
            from fim_de_jogo import tela_fim_de_jogo
            escolha = tela_fim_de_jogo(screen, venceu=win)
            if escolha == "reiniciar":
                return rodar_jogo(screen)      # reinicia o jogo
            elif escolha == "menu":
                return                        # volta ao main.py

        pygame.display.flip()
        clock.tick(60)
