import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import threading
import time
import random
import tkinter as tk
from tkinter import messagebox

TAMANHO_JOGO = 10
PONTUACAO_MAXIMA = 2000
TAMANHO_ALEATORIO = 100
pontuacao = 0

# Cria a matriz tridimensional com valores aleatórios
matriz = np.random.randint(-TAMANHO_ALEATORIO * 2, TAMANHO_ALEATORIO + 1, size=(TAMANHO_JOGO, TAMANHO_JOGO, TAMANHO_JOGO))
matriz[0, 0, 0] = 0

posicao_cubo = [0, 0, 0]

plt.rcParams['toolbar'] = 'None'

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Configurações da plotagem inicial
ax.set_xlim(0, TAMANHO_JOGO)
ax.set_ylim(0, TAMANHO_JOGO)
ax.set_zlim(0, TAMANHO_JOGO)
ax.set_xticks(range(0, TAMANHO_JOGO))
ax.set_yticks(range(0, TAMANHO_JOGO))
ax.set_zticks(range(0, TAMANHO_JOGO))

# Posição inicial do cubo aleatório (vermelho)
posicao_cubo_aleatorio = [random.randint(0, TAMANHO_JOGO - 1),
                          random.randint(0, TAMANHO_JOGO - 1),
                          random.randint(0, TAMANHO_JOGO - 1)]

posicoes_visitadas = []






def desenhar_cubos():
    global posicoes_visitadas
    ax.clear()
    ax.set_xlim(0, TAMANHO_JOGO)
    ax.set_ylim(0, TAMANHO_JOGO)
    ax.set_zlim(0, TAMANHO_JOGO)
    ax.set_xticks(range(0, TAMANHO_JOGO))
    ax.set_yticks(range(0, TAMANHO_JOGO))
    ax.set_zticks(range(0, TAMANHO_JOGO))

    # Plotar o cubo aleatório amarelo
    ax.scatter(posicao_cubo_aleatorio[0], posicao_cubo_aleatorio[1], posicao_cubo_aleatorio[2], color='yellow', s=50)

    # Plotar todos os pontos por onde o cubo passou
    for posicao in posicoes_visitadas:
        ax.scatter(posicao[0], posicao[1], posicao[2], color='red', s=50)

    # Plotar o cubo atual (azul)
    ax.scatter(posicao_cubo[0], posicao_cubo[1], posicao_cubo[2], color='blue', s=50)

    # Adicionar a linha vermelha que conecta os pontos
    if len(posicoes_visitadas) > 1:
        xs, ys, zs = zip(*posicoes_visitadas)
        ax.plot(xs, ys, zs, color='red', linewidth=2)  # Ajuste a largura da linha conforme necessário

    plt.draw()



def movimento_valido(nova_posicao):
    return all(0 <= coord < TAMANHO_JOGO for coord in nova_posicao)


def gerar_movimento_aleatorio():
    global posicao_cubo, posicoes_visitadas, pontuacao
    nova_posicao = posicao_cubo.copy()
    for i in range(3):
        nova_posicao[i] += random.choice([-1, 0, 1])

    while not movimento_valido(nova_posicao) or nova_posicao in posicoes_visitadas:
        nova_posicao = posicao_cubo.copy()
        for i in range(3):
            nova_posicao[i] += random.choice([-1, 0, 1])

    posicao_cubo = nova_posicao
    posicoes_visitadas.append(posicao_cubo)

    pontuacao += matriz[nova_posicao[0], nova_posicao[1], nova_posicao[2]]

    desenhar_cubos()


def verificar_se_cubo_encontrado():
    if pontuacao >= PONTUACAO_MAXIMA:
        messagebox.showinfo("Parabéns!", "Você atingiu mais que {}.".format(PONTUACAO_MAXIMA))
        plt.close()
    elif pontuacao <= -PONTUACAO_MAXIMA:
        messagebox.showinfo("Perdeu!", "Sua pontuação é menor que {}.".format(-PONTUACAO_MAXIMA))
        plt.close()
    elif posicao_cubo == posicao_cubo_aleatorio:
        messagebox.showinfo("Parabéns!", "Você encontrou o cubo vermelho.")
        plt.close()


def gerar_movimentos():
    while True:
        gerar_movimento_aleatorio()
        verificar_se_cubo_encontrado()
        time.sleep(0.75)


def placar():
    root = tk.Tk()
    root.title("Pontuação")
    placar_label = tk.Label(root, text="Pontuação: 0")
    placar_label.pack()
    while True:
        placar_label.config(text="Pontuação: {}".format(pontuacao))
        root.update()
        time.sleep(0.5)


thread = threading.Thread(target=gerar_movimentos)
thread.daemon = True
thread.start()

thread2 = threading.Thread(target=placar)
thread2.daemon = True
thread2.start()

desenhar_cubos()
plt.show()

# Adicionando as funções para plotagem de caminho
def inicializa_plot(matrix, start, end):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    for point in np.ndindex(matrix.shape):
        x, y, z = point
        if point == start:
            ax.scatter(x, y, z, color='green', s=50)
        elif point == end:
            ax.scatter(x, y, z, color='yellow', s=50)
        else:
            ax.scatter(x, y, z, color='blue', s=10)
    plt.ion()
    plt.show