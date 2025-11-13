# menu.py (compatível com imagens OU pill branco)
import pygame
import os

class Botao:
    def __init__(self, *args):
        """
        Suporta duas formas:
        1) image-mode: Botao(x, y, imagem_normal_path, imagem_hover_path, acao)
        2) pill-mode:  Botao(x, y, largura, altura, texto, acao)
        """
        if len(args) == 5 and isinstance(args[2], str):
            # imagem-based
            x, y, img_normal, img_hover, acao = args
            self.mode = "image"
            self.acao = acao
            # tenta carregar imagens, se falhar cria fallback surface
            def load_img(path):
                try:
                    img = pygame.image.load(path).convert_alpha()
                    return img
                except Exception:
                    # fallback: superfície cinza
                    s = pygame.Surface((300, 70), pygame.SRCALPHA)
                    s.fill((180, 180, 180))
                    pygame.draw.rect(s, (120,120,120), s.get_rect(), 3)
                    return s
            self.imagem_normal = load_img(img_normal)
            self.imagem_hover = load_img(img_hover)
            self.imagem_atual = self.imagem_normal
            self.rect = self.imagem_atual.get_rect(topleft=(x, y))

        elif len(args) == 6:
            # pill-based
            x, y, largura, altura, texto, acao = args
            self.mode = "pill"
            self.rect = pygame.Rect(int(x), int(y), int(largura), int(altura))
            self.texto = texto
            self.acao = acao
            self.hover = False
        else:
            raise TypeError("Botao: assinatura inválida. Use image-mode ou pill-mode.")

    # para ambos os modos
    def atualizar(self, pos_mouse):
        if self.mode == "image":
            if self.rect.collidepoint(pos_mouse):
                self.imagem_atual = self.imagem_hover
            else:
                self.imagem_atual = self.imagem_normal
        else:
            self.hover = self.rect.collidepoint(pos_mouse)

    def desenhar(self, screen, fonte=None, cor_texto=(50,100,50), cor_fundo=(245,245,245), cor_sombra=(0,0,0,80)):
        if self.mode == "image":
            screen.blit(self.imagem_atual, self.rect)
        else:
            # desenhar pill (mesmo estilo do pause)
            sombra_offset = (3, 3) if self.hover else (6, 6)
            shadow_surf = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)
            pygame.draw.rect(shadow_surf, cor_sombra, shadow_surf.get_rect(), border_radius=self.rect.height // 2)
            screen.blit(shadow_surf, (self.rect.x + sombra_offset[0], self.rect.y + sombra_offset[1]))

            desloc_y = -3 if self.hover else 0
            pill_rect = pygame.Rect(self.rect.x, self.rect.y + desloc_y, self.rect.width, self.rect.height)
            pygame.draw.rect(screen, cor_fundo, pill_rect, border_radius=pill_rect.height // 2)
            pygame.draw.rect(screen, (200,200,200), pill_rect, 2, border_radius=pill_rect.height // 2)

            # render texto (usa fonte passada ou padrao)
            if fonte is None:
                try:
                    fonte = pygame.font.Font("imagens/PixelOperator8.ttf", 22)
                except Exception:
                    fonte = pygame.font.Font(None, 32)
            text_surf = fonte.render(self.texto, True, cor_texto)
            text_rect = text_surf.get_rect(center=pill_rect.center)
            screen.blit(text_surf, text_rect)

    def verificar_clique(self, pos_mouse, evento):
        if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
            if self.rect.collidepoint(pos_mouse):
                return self.acao
        return None


def desenhar_tela(screen, botoes, eventos=None):
    largura, altura = screen.get_size()
    VERDE = (50, 100, 50)
    BRANCO = (245, 245, 245)
    COR_SOMBRA = (0,0,0,80)

    # fonte para pill buttons
    try:
        fonte = pygame.font.Font("imagens/PixelOperator8.ttf", 15)
    except:
        fonte = pygame.font.Font(None, 20)

    # fundo e logo com fallback
    try:
        fundo = pygame.image.load("imagens/background.png").convert()
        fundo = pygame.transform.smoothscale(fundo, (largura, altura))
    except:
        fundo = pygame.Surface((largura, altura))
        fundo.fill((230, 230, 230))
    screen.blit(fundo, (0,0))

    try:
        logo = pygame.image.load("imagens/logo.png").convert_alpha()
        logo = pygame.transform.smoothscale(logo, (400, 220))
        screen.blit(logo, (largura//2 - logo.get_width()//2, 80))
    except:
        pass

    pos_mouse = pygame.mouse.get_pos()
    for botao in botoes:
        botao.atualizar(pos_mouse)
        # para modo image, desenhar sem parâmetros; para pill, passar fonte e cores
        if getattr(botao, "mode", None) == "image":
            botao.desenhar(screen)
        else:
            botao.desenhar(screen, fonte, VERDE, BRANCO, COR_SOMBRA)

    if eventos:
        for evento in eventos:
            for botao in botoes:
                acao = botao.verificar_clique(pos_mouse, evento)
                if acao:
                    return acao
    return None
