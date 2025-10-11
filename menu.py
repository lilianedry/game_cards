import pygame

class Botao:
    def __init__(self, x, y, imagem_normal, imagem_hover, acao=None):
        self.imagem_normal = pygame.image.load(imagem_normal).convert_alpha()
        self.imagem_hover = pygame.image.load(imagem_hover).convert_alpha()
        self.imagem_atual = self.imagem_normal
        self.rect = self.imagem_atual.get_rect(topleft=(x, y))
        self.acao = acao
        
    def desenhar(self, surface):
        surface.blit(self.imagem_atual, self.rect)
        
    def verificar_clique(self, pos, evento):
        if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
            if self.rect.collidepoint(pos):
                if self.acao:
                    return self.acao
        return None
        
    def atualizar(self, pos_mouse):
        if self.rect.collidepoint(pos_mouse):
            self.imagem_atual = self.imagem_hover
        else:
            self.imagem_atual = self.imagem_normal

def desenhar_tela(screen, botoes, eventos=None):
    fundo = pygame.image.load("imagens/background.png").convert()
    fundo = pygame.transform.scale(fundo, (1280, 720))
    screen.blit(fundo, (0, 0))
    
    logo = pygame.image.load("imagens/logo.png").convert_alpha()
    logo = pygame.transform.scale(logo, (580, 327)) 
    
    largura_tela = screen.get_width()
    altura_tela = screen.get_height()
    pos_x = (largura_tela - logo.get_width()) // 2
    pos_y = 50
    
    screen.blit(logo, (pos_x, pos_y))
    
    pos_mouse = pygame.mouse.get_pos()
    
    for botao in botoes:
        botao.atualizar(pos_mouse)
        botao.desenhar(screen)
        
    if eventos:
        for evento in eventos:
            for botao in botoes:
                acao = botao.verificar_clique(pos_mouse, evento)
                if acao:
                    return acao
    return None