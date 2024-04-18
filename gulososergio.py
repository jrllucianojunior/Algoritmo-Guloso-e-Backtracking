import numpy as np  
import matplotlib.pyplot as plt  
from mpl_toolkits.mplot3d import Axes3D  

def inicializa_plot(matrix, start, end):  
    fig = plt.figure()  # Cria uma nova figura para plotagem.
    ax = fig.add_subplot(111, projection='3d')  
    for point in np.ndindex(matrix.shape):  
        x, y, z = point  # Desempacota as coordenadas do ponto.
        if point == start:  
            ax.scatter(x, y, z, color='green', s=100)  # Marca o ponto de início em verde.
        elif point == end:  
            ax.scatter(x, y, z, color='yellow', s=100)  # Marca o ponto de fim em amarelo.
        else:  
            ax.scatter(x, y, z, color='blue', s=1)  # Plota os demais pontos em azul.
    plt.ion()  
    plt.show()  
    return fig, ax  # Retorna a figura e os eixos para futuras modificações.

def plot_caminho(ax, valores_coletados, block=False):
    xs, ys, zs = zip(*valores_coletados) 
    ax.plot(xs, ys, zs, color='red', marker='o')  # Plota o caminho coletado em vermelho.
    plt.draw()  
    plt.pause(0.1)  
    if block:  
        plt.ioff()  
        plt.show()  # Mostra o plot final.

def Coletar(matrix, start, end):
    caminhos_coletados = [start]  # Inicializa a lista de valores coletados com a posição inicial.
    total_coletado = 0  
    posicao_atual = start  
    fig, ax = inicializa_plot(matrix, start, end)  # Inicializa o plot com pontos iniciais e finais.

    direcoes = [
    (1, 0, 0), (-1, 0, 0),   
    (0, 1, 0), (0, -1, 0),  
    (0, 0, 1), (0, 0, -1),  
    (1, 1, 0), (-1, 1, 0),  
    (1, -1, 0), (-1, -1, 0),  
    (1, 0, 1), (-1, 0, 1),  
    (1, 0, -1), (-1, 0, -1), 
    (0, 1, 1), (0, -1, 1),  
    (0, 1, -1), (0, -1, -1)  
    ]

    def limites(pos):  # Função auxiliar para verificar se uma posição está dentro dos limites da matriz.
        x, y, z = pos
        return 0 <= x < matrix.shape[0] and 0 <= y < matrix.shape[1] and 0 <= z < matrix.shape[2]
   
    def coleta_valor(pos):  # Função auxiliar para coletar o valor de uma posição.
        nonlocal total_coletado 
        x, y, z = pos
        valor = matrix[x][y][z]  # Pega o valor na posição especificada.
        total_coletado += valor  # Adiciona o valor ao total coletado.

    def eh_extremo(pos):  # Função para verificar se uma posição é um extremo da matriz.
        # Compara a posição com todos os cantos da matriz.
        return pos in [(0,0,0), (matrix.shape[0]-1, matrix.shape[1]-1, matrix.shape[2]-1), (0, matrix.shape[1]-1, 0), (matrix.shape[0]-1, 0, 0), (0, 0, matrix.shape[2]-1), (0, matrix.shape[1]-1, matrix.shape[2]-1), (matrix.shape[0]-1, 0, matrix.shape[2]-1)]

    def pode_escapar(pos):  # Verifica se é possível escapar de uma posição sem ficar preso.
        for dx, dy, dz in direcoes: 
            prox_pos = (pos[0] + dx, pos[1] + dy, pos[2] + dz)  # Calcula a próxima posição.
            if limites(prox_pos) and prox_pos not in caminhos_coletados:  # Verifica se a próxima posição é válida e não foi visitada.
                return True  # Retorna True se houver pelo menos um movimento válido.
        return False  
    
    while posicao_atual != end: 
        if total_coletado >= 2000 or total_coletado <= -2000:  # Verifica se o total coletado atingiu os limites.
            break 

        posicoes_possiveis = []  # Lista para armazenar posições válidas para o próximo movimento.
        for dx, dy, dz in direcoes:  
            prox_pos = (posicao_atual[0] + dx, posicao_atual[1] + dy, posicao_atual[2] + dz)
            if limites(prox_pos) and prox_pos not in caminhos_coletados:  # Verifica se a próxima posição é válida e ainda não foi visitada.
                # Se a próxima posição não é um extremo ou se é um extremo do qual é possível escapar, adicione-a à lista de próximas posições.
                if not eh_extremo(prox_pos) or pode_escapar(prox_pos):
                    posicoes_possiveis.append(prox_pos)  # Adiciona a próxima posição válida à lista.

        if not posicoes_possiveis:  # Se não houver próximas posições válidas, interrompa o loop.
            break

       
        proxima_posicao = max(posicoes_possiveis, key=lambda pos: matrix[pos]) # Escolhe o próximo ponto com o maior valor na matriz.
        coleta_valor(proxima_posicao)  # Atualiza o total coletado com o valor da próxima posição escolhida.
        caminhos_coletados.append(proxima_posicao)  # Adiciona a próxima posição à lista de posições visitadas.
        posicao_atual = proxima_posicao  # Atualiza a posição atual para a próxima posição.

        plot_caminho(ax, caminhos_coletados) 
        print('Total Coletado:', total_coletado) 
        print('Posição atual:', posicao_atual)  

    plot_caminho(ax, caminhos_coletados, block=True)  
    return total_coletado, caminhos_coletados, posicao_atual  # Retorna o total coletado, a lista de posições visitadas e a posição final.

matrix = np.random.randint(-100, 101, size=(10, 10, 10))  # Gera uma matriz 10x10x10 com valores aleatórios entre -100 e 100.
cordenada_inicial = tuple(np.random.randint(0, 10, size=3))  # Gera uma coordenada inicial aleatória.
cordenada_final = tuple(np.random.randint(0, 10, size=3))  # Gera uma coordenada final aleatória.

total, caminho_coletado, posicao_parada = Coletar(matrix, cordenada_inicial, cordenada_final)  # Inicia o processo de coleta baseado na matriz e nas coordenadas iniciais e finais.

print('Cordenada de parada:', posicao_parada) 
print('Cordenada inicial:', cordenada_inicial) 
print('Cordenada final:', cordenada_final)  
print('Total coletado:', total) 
