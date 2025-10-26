import pygame
import sys
import json
import os
import popup_sair


def pause_tela(screen, progresso_atual=None):
    """
    Tela de pausa do jogo.
    Permite salvar progresso atual em arquivo local e sair para o menu.
    """
    clock = pygame.time.Clock()

    # --- Fontes ---
    fonte_path = "imagens/Silkscreen.ttf"
    try:
        fonte_titulo = pygame.font.Font(fonte_path, 30)
        fonte_botao = pygame.font.Font(fonte_path, 22)
    except Exception:
        fonte_titulo = pygame.font.Font(None, 50)
        fonte_botao = pygame.font.Font(None, 28)
        print("⚠️ Fonte Silkscreen não encontrada, usando padrão.")

    # --- Cores ---
    VERDE = (50, 100, 50)
    BRANCO = (245, 245, 245)
    LINE_COLOR = (150, 150, 150)
    BG_ALPHA = 225

    # --- Fundo e logo ---
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
        logo = pygame.Surface((300, 170), pygame.SRCALPHA)
        logo.fill((200, 200, 200, 0))

    # --- Caixa translúcida ---
    caixa_w, caixa_h = int(screen.get_width() * 0.78), int(screen.get_height() * 0.62)
    caixa_x = (screen.get_width() - caixa_w) // 2
    caixa_y = (screen.get_height() - caixa_h) // 2
    caixa = pygame.Surface((caixa_w, caixa_h), pygame.SRCALPHA)
    caixa.fill((225, 225, 225, BG_ALPHA))

    # --- Título e botão X ---
    texto_titulo = fonte_titulo.render("PAUSADO", True, VERDE)
    pos_titulo_x = caixa_x + 40
    pos_titulo_y = caixa_y + 20

    texto_x = fonte_titulo.render("X", True, VERDE)
    largura_x, altura_x = texto_x.get_size()
    pos_x_x = caixa_x + caixa_w - 40 - largura_x
    pos_y_x = pos_titulo_y
    botao_x = pygame.Rect(pos_x_x, pos_y_x, largura_x, altura_x)

    # --- Botões principais ---
    bot_salvar = pygame.Rect(caixa_x + (caixa_w - 360) // 2, caixa_y + caixa_h // 2 - 30, 360, 72)
    bot_sair = pygame.Rect(caixa_x + (caixa_w - 360) // 2, caixa_y + caixa_h // 2 + 60, 360, 72)

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

    mensagem = ""
    rodando = True
    acao = "resume"

    while rodando:
        mx, my = pygame.mouse.get_pos()
        hover_salvar = bot_salvar.collidepoint((mx, my))
        hover_sair = bot_sair.collidepoint((mx, my))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                acao = "resume"
                rodando = False

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if botao_x.collidepoint(event.pos):
                    acao = "resume"
                    rodando = False

                elif bot_salvar.collidepoint(event.pos):
                    if progresso_atual:
                        try:
                            with open("progresso.json", "w", encoding="utf-8") as f:
                                json.dump(progresso_atual, f, indent=2)
                            mensagem = "Progresso salvo!"
                            print("✅ Progresso salvo:", progresso_atual)
                        except Exception as e:
                            mensagem = "Erro ao salvar!"
                            print("❌ Falha ao salvar:", e)
                    else:
                        mensagem = "Nenhum progresso para salvar."

                #elif bot_sair.collidepoint(event.pos):
                #    acao = "menu"
                #rodando = False
                
                elif bot_sair.collidepoint((mx, my)):
                    escolha = popup_sair.popup_confirmar_saida(screen)
                    if escolha == "sair":
                        acao = "menu"
                        rodando = False
                    else:
                        # Apenas fecha o popup e continua na tela de pause
                        mensagem = ""

                    
                    
                    
                    

        # --- Desenho da interface ---
        screen.blit(fundo, (0, 0))
        screen.blit(logo, (80, 10))
        screen.blit(caixa, (caixa_x, caixa_y))
        screen.blit(texto_titulo, (pos_titulo_x, pos_titulo_y))
        screen.blit(texto_x, (pos_x_x, pos_y_x))
        pygame.draw.line(screen, LINE_COLOR, (pos_titulo_x, pos_titulo_y + 50),
                         (caixa_x + caixa_w - 20, pos_titulo_y + 50), 2)
        desenhar_pill(screen, "SALVAR PROGRESSO", bot_salvar, VERDE, hover_salvar)
        desenhar_pill(screen, "SAIR DO JOGO", bot_sair, VERDE, hover_sair)

        if mensagem:
            msg_surf = fonte_botao.render(mensagem, True, VERDE)
            msg_rect = msg_surf.get_rect(center=(screen.get_width() // 2, bot_sair.bottom + 30))
            screen.blit(msg_surf, msg_rect)

        pygame.display.flip()
        clock.tick(60)
        

    return acao

    
