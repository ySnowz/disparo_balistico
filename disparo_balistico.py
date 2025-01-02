# Importando bibliotecas necessárias
import math  # Para funções matemáticas (sqrt, radians, sin, cos, etc.)
import random  # Para gerar números aleatórios

# Função para gerar parâmetros aleatórios para a simulação
def gerar_parametros_aleatorios(distancia):
    """
    Gera parâmetros aleatórios para a simulação, exceto a distância.

    Parâmetros:
        distancia (float): Distância até o alvo em metros.

    Retorna:
        Uma tupla contendo:
        - velocidade_inicial (float): Velocidade inicial do projétil em m/s.
        - peso_graos (float): Peso do projétil em grains.
        - bc (float): Coeficiente balístico.
        - densidade_ar (float): Densidade do ar em kg/m³.
        - velocidade_vento (float): Velocidade do vento em m/s.
        - direcao_vento_graus (float): Direção do vento em graus.
        - latitude_graus (float): Latitude em graus.
        - gravidade (float): Aceleração devido à gravidade em m/s².
    """
    # Gera uma velocidade inicial aleatória entre 700 e 900 m/s (intervalo típico para projéteis)
    velocidade_inicial = random.uniform(700, 900)

    # Gera um peso aleatório para o projétil entre 150 e 180 grains (exemplo de faixa comum)
    peso_graos = random.uniform(150, 180)

    # Gera um coeficiente balístico (BC) aleatório entre 0.4 e 0.6 (valores típicos)
    bc = random.uniform(0.4, 0.6)

    # Gera uma densidade do ar aleatória entre 1.1 e 1.3 kg/m³ (varia com altitude e condições)
    densidade_ar = random.uniform(1.1, 1.3)

    # Gera uma velocidade do vento aleatória entre 0 e 10 m/s
    velocidade_vento = random.uniform(0, 10)

    # Gera uma direção do vento aleatória entre 0 e 360 graus
    direcao_vento_graus = random.uniform(0, 360)

    # Gera uma latitude aleatória entre -90 e 90 graus
    latitude_graus = random.uniform(-90, 90)

    # Define a aceleração devido à gravidade (valor padrão da Terra)
    gravidade = 9.8

    # Retorna todos os parâmetros gerados
    return velocidade_inicial, peso_graos, bc, densidade_ar, velocidade_vento, direcao_vento_graus, latitude_graus, gravidade


# Função para calcular a trajetória do projétil
def calcular_disparo_avancado(distancia, velocidade_inicial, peso_graos, bc, densidade_ar, velocidade_vento, direcao_vento_graus, latitude_graus, gravidade=9.8):
    """
    Calcula a trajetória do projétil considerando arrasto, vento e efeito de Coriolis.

    Parâmetros:
        distancia (float): Distância até o alvo em metros.
        velocidade_inicial (float): Velocidade inicial do projétil em m/s.
        peso_graos (float): Peso do projétil em grains.
        bc (float): Coeficiente balístico.
        densidade_ar (float): Densidade do ar em kg/m³.
        velocidade_vento (float): Velocidade do vento em m/s.
        direcao_vento_graus (float): Direção do vento em graus.
        latitude_graus (float): Latitude em graus.
        gravidade (float): Aceleração devido à gravidade em m/s² (padrão: 9.8).

    Retorna:
        Uma tupla contendo:
        - z (float): Queda (altitude) do projétil em metros.
        - y (float): Desvio lateral do projétil em metros.
    """
    # Converte o peso do projétil de grains para quilogramas
    peso_kg = peso_graos * 0.0000647989

    # Define o intervalo de tempo para a simulação (passo de integração)
    dt = 0.001

    # Define a posição inicial do projétil (x, y, z)
    x, y, z = 0, 0, 0

    # Define a velocidade inicial do projétil (vx, vy, vz)
    vx, vy, vz = velocidade_inicial, 0, 0

    # Loop para simular a trajetória até o projétil atingir a distância do alvo
    while x < distancia:
        # Calcula a velocidade atual do projétil
        velocidade = math.sqrt(vx**2 + vy**2 + vz**2)

        # Calcula a força de arrasto aerodinâmico
        forca_arrasto = 0.5 * (peso_kg / bc) * densidade_ar * velocidade**2

        # Calcula as componentes da aceleração devido ao arrasto
        ax = -forca_arrasto * vx / velocidade
        ay = -forca_arrasto * vy / velocidade
        az = -forca_arrasto * vz / velocidade - gravidade

        # Calcula as componentes do vento
        direcao_vento_rad = math.radians(direcao_vento_graus)  # Converte graus para radianos
        vento_x = velocidade_vento * math.cos(direcao_vento_rad)
        vento_y = velocidade_vento * math.sin(direcao_vento_rad)

        # Aplica o efeito do vento na aceleração (simplificado)
        ay += vento_y / (peso_kg / gravidade)
        ax += vento_x / (peso_kg / gravidade)

        # Calcula o efeito de Coriolis
        velocidade_angular_terra = 7.292e-5  # Velocidade angular da Terra em rad/s
        latitude_rad = math.radians(latitude_graus)  # Converte latitude para radianos
        desvio_coriolis = 2 * velocidade * math.sin(latitude_rad) * velocidade_angular_terra * dt
        ay += desvio_coriolis  # Aplica o efeito de Coriolis na aceleração

        # Atualiza a velocidade e a posição usando o método de Euler
        vx += ax * dt
        vy += ay * dt
        vz += az * dt
        x += vx * dt
        y += vy * dt
        z += vz * dt

    # Retorna a queda (z) e o desvio lateral (y) do projétil
    return z, y


# Exemplo de uso do código
if __name__ == "__main__":
    # Solicita ao usuário a distância até o alvo
    distancia_alvo = float(input("Digite a distância até o alvo em metros: "))

    # Gera parâmetros aleatórios para a simulação
    velocidade_inicial, peso_graos, bc, densidade_ar, velocidade_vento, direcao_vento_graus, latitude_graus, gravidade = gerar_parametros_aleatorios(distancia_alvo)

    # Calcula a trajetória do projétil
    queda, desvio = calcular_disparo_avancado(distancia_alvo, velocidade_inicial, peso_graos, bc, densidade_ar, velocidade_vento, direcao_vento_graus, latitude_graus, gravidade)

    # Exibe os resultados
    print(f"Distância do alvo: {distancia_alvo:.2f} metros")
    print(f"Velocidade Inicial: {velocidade_inicial:.2f} m/s")
    print(f"Peso do Projétil: {peso_graos:.2f} grains")
    print(f"Coeficiente Balístico (BC): {bc:.2f}")
    print(f"Densidade do Ar: {densidade_ar:.2f} kg/m³")
    print(f"Velocidade do Vento: {velocidade_vento:.2f} m/s")
    print(f"Direção do Vento: {direcao_vento_graus:.2f} graus")
    print(f"Latitude: {latitude_graus:.2f} graus")
    print(f"Queda: {queda:.2f} metros, Desvio Lateral: {desvio:.2f} metros")