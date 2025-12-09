import time
import math
import random
from collections import deque

# Variables constantes
MAX_PROFUNDIDAD = 3                             # Define la profundidad del MiniMax
PUNTAJE_GATO_CAPTURA_RATON = -1000              # Puntaje cuando el gato captura al raton
PUNTAJE_RATON_ESCAPA = 1000                     # Puntaje cuando el raton escapa
PESO_DIST_RATON_GATO = 3                        # Peso distancia entre gato y raton
PESO_DIST_RATON_SALIDA = 4                      # Peso distancia entre raton y salida
TURNOS_ALEATORIOS = 5                           # Numero de turnos iniciales con movimiento aleatorio para el raton
MOVIMIENTOS = [(1,0), (-1,0), (0,1), (0,-1)]    # Variable Global: Derecha, Izquierda, Arriba, Abajo

# Funcion donde creamos una matriz que sera nuestro Laberinto Fijos
def laberinto_fijo():
    # Creamos una matriz 11x11 - Impar para tener paredes exteriores - 0 es Camino - 1 es Pared
    matriz = [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
              [1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1],
              [1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1],
              [1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1],
              [1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1],
              [1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1],
              [1, 1, 1, 0, 1, 0, 1, 0, 1, 1, 1],
              [1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1],
              [1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1],
              [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
              [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]
    return matriz #Retornamos Matriz

# Inicializamos la variable Laberinto que tendra la matriz de la funcion
laberinto = laberinto_fijo() 

# Definimos las posiciones del Gato, Raton y Salida
gato, raton, salida = (5,9), (1,1), (9,9) 

# Funcion para determinar los movimientos validos
def movimientos_validos(posicion, laberinto):
    validos = [] # Lista para almacenar movimientos validos
    for dir_x, dir_y in MOVIMIENTOS: # Recorremos las direcciones posibles
        new_x, new_y = posicion[0] + dir_x, posicion[1] + dir_y # Calculamos nueva posicion
         # Verificamos si la nueva posicion esta dentro de los limites del laberinto y es un camino (0)
        if 0 <= new_x < len(laberinto) and 0 <= new_y < len(laberinto[0]):
            if laberinto[new_x][new_y] == 0:
                validos.append((new_x, new_y)) # Agregamos la nueva posicion a la lista de validos
    return validos # Retornamos la lista de movimientos validos

# Funcion para mostrar el laberinto en consola
def mostrar_laberinto_fijo(raton, gato, salida, raton_visible):
    for fila in range(len(laberinto)):
        dibujo = [] # Una lista para almacenar los caracteres
        for celda in range(len(laberinto[0])):
            posicion_actual = (fila, celda) # Posicion actual en el laberinto
            if posicion_actual == raton and raton_visible:
                caracter = "🐭"
            elif posicion_actual == gato:
                caracter = "🐱"
            elif posicion_actual == salida:
                caracter = "🚪"
            elif laberinto[fila][celda] == 1:
                caracter = "⬜️"
            else:
                caracter = "  "
            dibujo.append(caracter) # Agregamos el/los caracteres a la lista
        print("".join(dibujo)) #Unimos todos los caracteres de la lista en una sola operacion rapida
    print()

# Funcion BFS que calcula la distancia real entre inicio y objetivo
def distancia_real(laberinto, inicio, objetivo):
    # Caso base
    if inicio == objetivo:
        return 0
    
    cola = deque([(inicio, 0)]) # Cola de tuplas (posicion inicial, distancia)
    visitados = {inicio} # Conjunto de posiciones visitadas (Set)

    # Bucle BFS
    while cola:
        #Posicion_actual es una Tupla de Coordenadas (x, y)
        posicion_actual, distancia = cola.popleft() # Desencolar el primer elemento
        for posicion_nueva in movimientos_validos(posicion_actual, laberinto):
            #Posicion_nueva es una Tupla de Coordenadas (x, y)
            if posicion_nueva == objetivo: # Si llegamos al objetivo
                return distancia + 1 # Retornamos la distancia incrementada
            if posicion_nueva not in visitados: # Si no ha sido visitado
                visitados.add(posicion_nueva) # Marcar como visitado
                cola.append((posicion_nueva, distancia + 1)) # Encolar nueva posicion con distancia incrementada
    
    return math.inf # Si no se encuentra camino, retornamos infinito

# Funcion que evalua valores que requiere para funcionar el MiniMax
def evualuar_estado(laberinto, raton, gato, salida):
    if raton == gato:
        return PUNTAJE_GATO_CAPTURA_RATON
    if raton == salida:
        return PUNTAJE_RATON_ESCAPA

    dist_raton_gato = distancia_real(laberinto, raton, gato) # Distancia real entre raton y gato
    dist_raton_salida = distancia_real(laberinto,raton, salida) # Distancia real entre raton y salida
    valor = (dist_raton_gato * PESO_DIST_RATON_GATO) - (dist_raton_salida * PESO_DIST_RATON_SALIDA) # Evaluacion del estado
    
    return valor

# Funcion que contiene el algoritmo Minimax, funcion que le da inteligencia a los personajes
def minimax(laberinto, raton, gato, salida, profundidad, es_turno_raton):
    # Caso base
    if raton == gato or raton == salida or profundidad == 0:
        return evualuar_estado(laberinto, raton, gato, salida)
    
    # Si es el turno del raton (maximizador)
    if es_turno_raton:
        mejor_puntaje = -math.inf
        for mov in movimientos_validos(raton, laberinto): # Recorremos los movimientos validos del raton
            valor_minimax = minimax(laberinto, mov, gato, salida, profundidad - 1, False) # Llamada recursiva
            mejor_puntaje = max(valor_minimax, mejor_puntaje) # Maximizamos el puntaje
        return mejor_puntaje # Retornamos el mejor puntaje
    else: # Si es el turno del gato (minimizador)
        peor_puntaje = math.inf
        for mov in movimientos_validos(gato, laberinto): # Recorremos los movimientos validos del gato
            valor_minimax = minimax(laberinto, raton, mov, salida, profundidad - 1, True) # Llamada recursiva
            peor_puntaje = min(valor_minimax, peor_puntaje) # Minimizamos el puntaje
        return peor_puntaje # Retornamos el peor puntaje

# Funcion para que los personajes tengan el mejor movimiento respecto a su rival
def encontrar_mejor_movimiento(laberinto, pos_personaje, pos_rival, salida, es_maximizador, profundidad):
    if es_maximizador: # Raton
        comparador = max # Funcion Maximizadora
        mejor_valor = -math.inf # Inicializamos mejor valor
        turno_a_pasar = False # Proximo turno es del Gato
    else:
        comparador = min # Funcion Minimizadora
        mejor_valor = math.inf  # Inicializamos mejor valor
        turno_a_pasar = True # Proximo turno es del Raton

    mejor_mov = pos_personaje # Inicializamos mejor movimiento

    for mov in movimientos_validos(pos_personaje, laberinto): # Recorremos los movimientos validos del personaje
        if es_maximizador: # Raton
            pos_raton_simulado = mov # Simulamos el movimiento del raton
            pos_gato_simulado = pos_rival # Gato permanece en su posicion
        else:
            pos_raton_simulado = pos_rival # Raton permanece en su posicion
            pos_gato_simulado = mov # Simulamos el movimiento del gato
            
        valor = minimax(laberinto, pos_raton_simulado, pos_gato_simulado, salida, profundidad, turno_a_pasar) # Llamada a minimax
    
        if comparador(valor, mejor_valor) == valor: # Comparamos valores
            mejor_valor = valor # Actualizamos mejor valor
            mejor_mov = mov # Actualizamos mejor movimiento

    return mejor_mov, mejor_valor # Retornamos mejor movimiento y su valor

#Banderas para el Ciclo While
es_turno_raton = True
contador_turno = 1
turnos_jugados_raton = 0

# Ciclo while para que se ejecute el programa
while True:
    print(f"Turno: {contador_turno} - {'Raton' if es_turno_raton else 'Gato'}")
    mostrar_laberinto_fijo(raton, gato, salida, raton_visible = True)
    time.sleep(0.5)

    # Logica de Turnos    
    if es_turno_raton: # Turno del Raton
        if turnos_jugados_raton < TURNOS_ALEATORIOS: # Movimiento aleatorio inicial para el raton
            movs = movimientos_validos(raton, laberinto) # Obtener movimientos validos
            if movs: # Si hay movimientos validos
                nuevo_raton = random.choice(movs) # Elegir un movimiento aleatorio
            else: # Si no hay movimientos validos, el raton se queda en su lugar
                nuevo_raton = raton 
            print(f"Raton se mueve aleatoriamente ({turnos_jugados_raton + 1}/{TURNOS_ALEATORIOS})")
            turnos_jugados_raton += 1 # Incrementamos el contador de turnos jugados por el raton
        else: # Movimiento inteligente con Minimax
            nuevo_raton, _ = encontrar_mejor_movimiento(laberinto, raton, gato, salida, True, MAX_PROFUNDIDAD) # Obtener mejor movimiento para el raton
        raton = nuevo_raton # Actualizar posicion del raton
        print(f"Raton se movio a : {raton}")
        if raton == gato: # Si el raton es capturado por el gato
            print("Raton fue capturado por el Gato")
            mostrar_laberinto_fijo(raton, gato, salida, raton_visible = False)
            break
        if raton == salida: # Si el raton escapa
            print("Raton logró escapar del Laberinto")
            mostrar_laberinto_fijo(raton, gato, salida, raton_visible = False)
            break
    else: # Turno del Gato
        nuevo_gato, _ = encontrar_mejor_movimiento(laberinto, gato, raton, salida, False, MAX_PROFUNDIDAD) # Obtener mejor movimiento para el gato
        gato = nuevo_gato # Actualizar posicion del gato
        print(f"El gato se movio a : {gato}")
        if gato == raton: # Si el gato captura al raton
            print("Gato ha capturado al Raton")
            mostrar_laberinto_fijo(raton, gato, salida, raton_visible = False)
            break
        if raton == salida: # Si el raton escapa
            print("Al Gato se le escapó el Raton")
            mostrar_laberinto_fijo(raton, gato, salida, raton_visible = False)
            break

    if contador_turno > 150: # Condicion de escape para evitar bucles infinitos
        print("Fin de los turnos, Gato y raton se pusieron a bailar sin parar")
        break

    contador_turno += 1 # Incrementamos el contador de turnos
    es_turno_raton = not es_turno_raton # Cambiamos el turno
# Fin del Codigo