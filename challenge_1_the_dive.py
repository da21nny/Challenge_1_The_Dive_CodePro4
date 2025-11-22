import random
import time
import math

MAX_PROFUNDIDAD = 3 #Variable constante - Define la profundidad del MiniMax

movimientos = [(1,0), (-1,0), (0,1), (0,-1)] # Variable Global: Derecha, Izquierda, Arriba, Abajo

def laberinto_fijo():
    #Laberinto definido 11x11 - Impar para tener paredes exteriores - 0 es Camino - 1 es Pared
    matriz = [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
              [1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1],
              [1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1],
              [1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1],
              [1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1],
              [1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1],
              [1, 1, 1, 0, 1, 0, 1, 0, 1, 1, 1],
              [1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1],
              [1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1],
              [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
              [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]
    return matriz

laberinto = laberinto_fijo()
raton, gato, salida = (1,1), (5,9), (9,9)

def movimientos_validos(posicion, laberinto):
    validos = []
    for dir_x, dir_y in movimientos:
        new_x, new_y = posicion[0] + dir_x, posicion[1] + dir_y
        if 0 <= new_x < len(laberinto) and 0 <= new_y < len(laberinto[0]):
            if laberinto[new_x][new_y] == 0:
                validos.append((new_x, new_y))
    return validos

def mostrar_laberinto_fijo(raton, gato, salida, raton_visible):
    for fila in range(len(laberinto)):
        dibujo = ""
        for celda in range(len(laberinto[0])):
            if (fila, celda) == raton and raton_visible:
                dibujo += "🐭"
            elif (fila, celda) == gato:
                dibujo += "🐱"
            elif (fila, celda) == salida:
                dibujo += "🚪"
            elif laberinto[fila][celda] == 1:
                dibujo += "⬜️"
            else:
                dibujo += "  "
        print(dibujo)
    print()

def calcular_distancia(dist_a, dist_b):
    return (abs(dist_a[0] - dist_b[0]) + abs(dist_a[1] - dist_b[1]))

def evualuar_estado(raton, gato, salida):
    dist_raton_gato = calcular_distancia(raton, gato)
    dist_raton_salida = calcular_distancia(raton, salida)
    valor = (dist_raton_gato * 3) - (dist_raton_salida * 4)

    if raton == gato:
        return -1000
    if raton == salida:
        return 1000
    
    return valor

def minimax(laberinto, raton, gato, salida, profundidad, es_turno_raton):
    if raton == gato or raton == salida or profundidad == 0:
        return evualuar_estado(raton, gato, salida)
    
    if es_turno_raton:
        mejor_puntaje = -math.inf
        for mov in movimientos_validos(raton, laberinto):
            valor_minimax = minimax(laberinto, mov, gato, salida, profundidad - 1, False)
            mejor_puntaje = max(valor_minimax, mejor_puntaje)
        return mejor_puntaje
    else:
        peor_puntaje = math.inf
        for mov in movimientos_validos(gato, laberinto):
            valor_minimax = minimax(laberinto, raton, mov, salida, profundidad - 1, True)
            peor_puntaje = min(valor_minimax, peor_puntaje)
        return peor_puntaje

def encontrar_mejor_movimiento(laberinto, pos_personaje, pos_rival, salida, es_maximizador, profundidad):
    if es_maximizador:
        mejor_valor = -math.inf
        turno_a_pasar = False
    else:
        mejor_valor = math.inf
        turno_a_pasar = True

    mejor_mov = pos_personaje
    movimientos = movimientos_validos(pos_personaje, laberinto)

    for mov in movimientos:
        if es_maximizador:
            pos_raton_simulado = mov
            pos_gato_simulado = pos_rival
        else:
            pos_raton_simulado = pos_rival
            pos_gato_simulado = mov
        valor = minimax(laberinto, pos_raton_simulado, pos_gato_simulado, salida, profundidad, turno_a_pasar)
    
        if es_maximizador:
            if valor > mejor_valor:
                mejor_valor = valor
                mejor_mov = mov
        else:
            if valor < mejor_valor:
                mejor_valor = valor
                mejor_mov = mov

    return mejor_mov, mejor_valor


es_turno_raton = True
contador_turno = 0

while True:
    print(f"Turno: {contador_turno} - {'Raton' if es_turno_raton else 'Gato'}")
    mostrar_laberinto_fijo(raton, gato, salida, raton_visible = True)
    time.sleep(1)

    if es_turno_raton:
        nuevo_raton, _ = encontrar_mejor_movimiento(laberinto, raton, gato, salida, True, MAX_PROFUNDIDAD)
        raton = nuevo_raton
        print(f"Raton se movio a : {raton}")
        if raton == gato:
            print("Raton fue capturado por el Gato")
            mostrar_laberinto_fijo(raton, gato, salida, raton_visible = False)
            break
        if raton == salida:
            print("Raton logró escapar del Laberinto")
            mostrar_laberinto_fijo(raton, gato, salida, raton_visible = False)
            break
    else:
        nuevo_gato, _ = encontrar_mejor_movimiento(laberinto, gato, raton, salida, False, MAX_PROFUNDIDAD)
        gato = nuevo_gato
        print(f"El gato se movio a : {gato}")
        if gato == raton:
            print("Gato ha capturado al Raton")
            mostrar_laberinto_fijo(raton, gato, salida, raton_visible = False)
            break
        if raton == salida:
            print("Al Gato se le escapó el Raton")
            mostrar_laberinto_fijo(raton, gato, salida, raton_visible = False)
            break

    if contador_turno > 150:
        print("Fin de los turnos, Gato y raton se pusieron a bailar sin parar")
        break

    contador_turno += 1
    es_turno_raton = not es_turno_raton
