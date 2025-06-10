import pygame, random, sys, os

pygame.init()
largura, altura = 800, 500
tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption("Snake Game")
relogio = pygame.time.Clock()
fonte = pygame.font.SysFont("Arial", 25)
tamanho = 10

def carregar_high_score():
    if os.path.exists("highscore.txt"):
        with open("highscore.txt", "r") as f:
            return int(f.read())
    return 0

def salvar_high_score(pontos):
    with open("highscore.txt", "w") as f:
        f.write(str(pontos))

def desenhar_texto(msg, y, cor=(255, 255, 255)):
    texto = fonte.render(msg, True, cor)
    ret = texto.get_rect(center=(largura // 2, y))
    tela.blit(texto, ret)

def tela_inicial():
    while True:
        tela.fill((0, 0, 0))
        desenhar_texto("🐍 Bem-vindo ao Snake Game!", 120)
        desenhar_texto("Use as setas para mover a cobrinha.", 160)
        desenhar_texto("Pressione qualquer tecla para começar!", 220)
        pygame.display.update()
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN:
                return

def tela_game_over(pontos, recorde):
    while True:
        tela.fill((0, 0, 0))
        desenhar_texto("💀 Game Over!", 120, (255, 0, 0))
        desenhar_texto(f"Pontos: {pontos}", 170)
        desenhar_texto(f"Maior Pontuação: {recorde}", 200)
        desenhar_texto("Pressione R para jogar novamente ou ESC para sair", 260)
        pygame.display.update()
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return "sair"
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_r:
                    return "reiniciar"
                elif evento.key == pygame.K_ESCAPE:
                    return "sair"

def main():
    x = largura // 2
    y = altura // 2
    vel_x = tamanho
    vel_y = 0
    cobra = [[x, y]]
    comida = [random.randrange(0, largura // tamanho) * tamanho,
              random.randrange(0, altura // tamanho) * tamanho]
    pontos = 0
    recorde = carregar_high_score()

    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return "sair"
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_UP and vel_y == 0:
                    vel_x, vel_y = 0, -tamanho
                elif evento.key == pygame.K_DOWN and vel_y == 0:
                    vel_x, vel_y = 0, tamanho
                elif evento.key == pygame.K_LEFT and vel_x == 0:
                    vel_x, vel_y = -tamanho, 0
                elif evento.key == pygame.K_RIGHT and vel_x == 0:
                    vel_x, vel_y = tamanho, 0

        x += vel_x
        y += vel_y

        if (x < 0 or x >= largura or y < 0 or y >= altura or [x, y] in cobra):
            if pontos > recorde:
                salvar_high_score(pontos)
            return tela_game_over(pontos, max(pontos, recorde))

        cobra.insert(0, [x, y])
        if x == comida[0] and y == comida[1]:
            pontos += 1
            comida = [random.randrange(0, largura // tamanho) * tamanho,
                      random.randrange(0, altura // tamanho) * tamanho]
        else:
            cobra.pop()

        tela.fill((0, 0, 0))
        pygame.draw.rect(tela, (255, 0, 0), (*comida, tamanho, tamanho))
        for seg in cobra:
            pygame.draw.rect(tela, (0, 255, 0), (*seg, tamanho, tamanho))

        desenhar_texto(f"Pontos: {pontos}", 20)
        pygame.display.update()
        relogio.tick(15)

def executar_jogo():
    while True:
        tela_inicial()
        resultado = main()
        if resultado == "sair":
            break

executar_jogo()
pygame.quit()
sys.exit()
