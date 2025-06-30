import pygame
import random
import sys
import os
import wave
import struct
import math

# Sons automáticos
def criar_som_comer():
    if not os.path.exists("comer.wav"):
        framerate = 44100
        duration = 0.2
        freq = 700.0
        wav = wave.open("comer.wav", "w")
        wav.setnchannels(1)
        wav.setsampwidth(2)
        wav.setframerate(framerate)
        for i in range(int(duration * framerate)):
            value = int(32767.0 * 0.5 * math.sin(2 * math.pi * freq * i / framerate))
            wav.writeframes(struct.pack('<h', value))
        wav.close()

def criar_som_morte():
    if not os.path.exists("morte.wav"):
        framerate = 44100
        duration = 0.4
        start_freq = 600.0
        end_freq = 100.0
        wav = wave.open("morte.wav", "w")
        wav.setnchannels(1)
        wav.setsampwidth(2)
        wav.setframerate(framerate)
        for i in range(int(duration * framerate)):
            freq = start_freq + (end_freq - start_freq) * (i / (duration * framerate))
            value = int(32767.0 * 0.5 * math.sin(2 * math.pi * freq * i / framerate))
            wav.writeframes(struct.pack('<h', value))
        wav.close()

criar_som_comer()
criar_som_morte()

# Inicialização
pygame.init()
try:
    pygame.mixer.init()
    som_comida = pygame.mixer.Sound("comer.wav")
    som_morte = pygame.mixer.Sound("morte.wav")
except pygame.error:
    print("Erro ao carregar sons.")
    som_comida = None
    som_morte = None

largura, altura = 800, 500
tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption("Snake Game")
relogio = pygame.time.Clock()
fonte = pygame.font.SysFont("Arial", 25)
tamanho = 10

def carregar_high_score():
    if os.path.exists("highscore.txt"):
        try:
            with open("highscore.txt", "r") as f:
                return int(f.read())
        except:
            return 0
    return 0

def salvar_high_score(pontos):
    try:
        with open("highscore.txt", "w") as f:
            f.write(str(pontos))
    except:
        pass

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
    x, y = largura // 2, altura // 2
    vel_x, vel_y = tamanho, 0
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

        if x < 0 or x >= largura or y < 0 or y >= altura or [x, y] in cobra:
            if som_morte:
                som_morte.play()
            if pontos > recorde:
                salvar_high_score(pontos)
            return tela_game_over(pontos, max(pontos, recorde))

        cobra.insert(0, [x, y])
        if [x, y] == comida:
            pontos += 1
            if som_comida:
                som_comida.play()
            comida = [random.randrange(0, largura // tamanho) * tamanho,
                      random.randrange(0, altura // tamanho) * tamanho]
        else:
            cobra.pop()

        # Fundo com grade estilo arcade
        tela.fill((0, 0, 0))
        for i in range(0, largura, tamanho):
            pygame.draw.line(tela, (30, 30, 30), (i, 0), (i, altura))
        for j in range(0, altura, tamanho):
            pygame.draw.line(tela, (30, 30, 30), (0, j), (largura, j))

        # Comida com brilho
        sombra_comida = (comida[0] + 2, comida[1] + 2)
        pygame.draw.rect(tela, (50, 10, 50), (*sombra_comida, tamanho, tamanho))
        pygame.draw.rect(tela, (255, 0, 180), (*comida, tamanho, tamanho))
        pygame.draw.rect(tela, (255, 100, 200), (*comida, tamanho, tamanho), width=1)

        # Cobra com sombra e contorno
        for seg in cobra:
            sombra = (seg[0] + 2, seg[1] + 2)
            pygame.draw.rect(tela, (10, 40, 10), (*sombra, tamanho, tamanho))
            pygame.draw.rect(tela, (0, 255, 100), (*seg, tamanho, tamanho))
            pygame.draw.rect(tela, (0, 150, 100), (*seg, tamanho, tamanho), width=1)

        desenhar_texto(f"Pontos: {pontos}", 20, (0, 200, 255))
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
