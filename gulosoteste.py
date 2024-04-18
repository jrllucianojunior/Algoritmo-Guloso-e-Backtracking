import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def inicializa_plot(matrix, start, end):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    
    for point in np.ndindex(matrix.shape):
        x, y, z = point
        if point == start:
            ax.scatter(x, y, z, color='green', s=100) 
        elif point == end:
            ax.scatter(x, y, z, color='yellow', s=100)  
        else:
            ax.scatter(x, y, z, color='blue', s=1)  
    plt.ion()  
    plt.show()
    return fig, ax

def plot_caminho(ax, caminhos_coletados, block=False):
    xs, ys, zs = zip(*caminhos_coletados)
    ax.plot(xs, ys, zs, color='red', marker='o')
    plt.draw()
    plt.pause(0.1)  
    if block:
        plt.ioff()  
        plt.show()

def Coletar(matrix, start, end):
    caminhos_coletados = [start]
    total_coletado = 0
    posicao_atual = start
    fig, ax = inicializa_plot(matrix, start, end)  

    direcoes = [
    (1, 0, 0), (-1, 0, 0),  # Movimento no eixo X
    (0, 1, 0), (0, -1, 0),  # Movimento no eixo Y
    (0, 0, 1), (0, 0, -1),  # Movimento no eixo Z
    (1, 1, 0), (-1, 1, 0),  # Movimento diagonal XY
    (1, -1, 0), (-1, -1, 0),  # Movimento diagonal XY
    (1, 0, 1), (-1, 0, 1),  # Movimento diagonal XZ
    (1, 0, -1), (-1, 0, -1),  # Movimento diagonal XZ
    (0, 1, 1), (0, -1, 1),  # Movimento diagonal YZ
    (0, 1, -1), (0, -1, -1)  # Movimento diagonal YZ
    ]


    def limites(pos):
        x, y, z = pos
        return 0 <= x < matrix.shape[0] and 0 <= y < matrix.shape[1] and 0 <= z < matrix.shape[2]
   
    def coleta_valor(pos):
        nonlocal total_coletado
        x, y, z = pos
        valor = matrix[x][y][z]
        total_coletado += valor

    def eh_extremo(pos):
        return pos in [(0,0,0), (matrix.shape[0]-1, matrix.shape[1]-1, matrix.shape[2]-1), (0, matrix.shape[1]-1, 0), (matrix.shape[0]-1, 0, 0), (0, 0, matrix.shape[2]-1), (0, matrix.shape[1]-1, matrix.shape[2]-1), (matrix.shape[0]-1, 0, matrix.shape[2]-1)]

    def pode_escapar(pos):
        for dx, dy, dz in direcoes:
            prox_pos = (pos[0] + dx, pos[1] + dy, pos[2] + dz)
            if limites(prox_pos) and prox_pos not in caminhos_coletados:
                return True
        return False

    while posicao_atual != end:
        if total_coletado >= 2000 or total_coletado <= -2000:
            break

        posicoes_possiveis = []
        for dx, dy, dz in direcoes:
            prox_pos = (posicao_atual[0] + dx, posicao_atual[1] + dy, posicao_atual[2] + dz)
            if limites(prox_pos) and prox_pos not in caminhos_coletados:
                if not eh_extremo(prox_pos) or pode_escapar(prox_pos):
                    posicoes_possiveis.append(prox_pos)

        if not posicoes_possiveis:
            break

        proxima_posicao = max(posicoes_possiveis, key=lambda pos: matrix[pos])
        coleta_valor(proxima_posicao)
        caminhos_coletados.append(proxima_posicao)
        posicao_atual = proxima_posicao

        plot_caminho(ax, caminhos_coletados)
        print('Total Coletado:',total_coletado)
        print('Posição atual:',posicao_atual)

    plot_caminho(ax, caminhos_coletados, block=True)
    return total_coletado, caminhos_coletados, posicao_atual

matrix = np.zeros((10, 10, 10), dtype=int)  
ini = 100
for y in range(10):  
    if y % 2 == 0: 
        for x in range(10):
            matrix[x, y, 0] = ini
            ini -= 1  
    else:  
        for x in range(9, -1, -1):  
            matrix[x, y, 0] = ini
            ini -= 1  

cordenada_inicial = 0,0,0 
cordenada_final = tuple(np.random.randint(0, 10, size=3))

# Coletando valores e visualizando o caminho
total, caminho_coletado, posicao_parada = Coletar(matrix, cordenada_inicial, cordenada_final)

print('Cordenada de parada:', posicao_parada)
print('Cordenada inicial:', cordenada_inicial)
print('Cordenada final:', cordenada_final)
print('Total coletado:', total)

