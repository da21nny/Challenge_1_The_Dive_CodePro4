import math
import time

# --- CONFIGURACIÓN DEL LABERINTO ---
# 0 = camino, 1 = pared
lab = [
    [0, 0, 1, 0, 0],
    [1, 0, 1, 0, 1],
    [0, 0, 0, 0, 0],
    [0, 1, 1, 1, 0],
    [0, 0, 0, 1, 0],
    [1, 0, 0, 0, 0],
]

raton = (4, 0)   # Posición inicial del ratón
gato = (0, 4)    # Posición inicial del gato
salida = (0, 0)  # Posición de la salida

movimientos = [(1,0), (-1,0), (0,1), (0,-1)]  # abajo, arriba, derecha, izquierda


# --- FUNCIONES DE UTILIDAD ---
def mostrar_laberinto(raton, gato):
    for i in range(len(lab)):
        fila = ""
        for j in range(len(lab[0])):
            if (i, j) == raton:
                fila += "R "
            elif (i, j) == gato:
                fila += "G "
            elif (i, j) == salida:
                fila += "S "
            elif lab[i][j] == 1:
                fila += "█ "
            else:
                fila += ". "
        print(fila)
    print()


def es_valido(pos):
    x, y = pos
    return 0 <= x < len(lab) and 0 <= y < len(lab[0]) and lab[x][y] == 0


def distancia(a, b):
    # Distancia Manhattan (no diagonal)
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


# --- FUNCIÓN DE EVALUACIÓN (cuánto conviene un estado al ratón) ---
def evaluar(raton, gato):
    # Cuanto más lejos esté del gato y más cerca de la salida, mejor
    return distancia(gato, raton) - distancia(raton, salida)


# --- ALGORITMO MINIMAX ---
def minimax(raton, gato, profundidad, turno_max):
    # Condiciones de fin
    if profundidad == 0 or raton == gato or raton == salida:
        return evaluar(raton, gato)

    if turno_max:  # Turno del ratón (MAX)
        mejor_valor = -math.inf
        for dx, dy in movimientos:
            nuevo_raton = (raton[0] + dx, raton[1] + dy)
            if es_valido(nuevo_raton):
                valor = minimax(nuevo_raton, gato, profundidad - 1, False)
                mejor_valor = max(mejor_valor, valor)
        return mejor_valor
    else:  # Turno del gato (MIN)
        peor_valor = math.inf
        for dx, dy in movimientos:
            nuevo_gato = (gato[0] + dx, gato[1] + dy)
            if es_valido(nuevo_gato):
                valor = minimax(raton, nuevo_gato, profundidad - 1, True)
                peor_valor = min(peor_valor, valor)
        return peor_valor


# --- DECISIÓN DEL RATÓN ---
def mover_raton(raton, gato):
    mejor_mov = raton
    mejor_valor = -math.inf

    for dx, dy in movimientos:
        nuevo_raton = (raton[0] + dx, raton[1] + dy)
        if es_valido(nuevo_raton):
            valor = minimax(nuevo_raton, gato, 3, False)  # profundidad limitada
            if valor > mejor_valor:
                mejor_valor = valor
                mejor_mov = nuevo_raton

    return mejor_mov


# --- MOVIMIENTO DEL GATO (simple: se acerca al ratón) ---
def mover_gato(gato, raton):
    mejor_mov = gato
    menor_dist = distancia(gato, raton)

    for dx, dy in movimientos:
        nuevo_gato = (gato[0] + dx, gato[1] + dy)
        if es_valido(nuevo_gato):
            dist = distancia(nuevo_gato, raton)
            if dist < menor_dist:
                menor_dist = dist
                mejor_mov = nuevo_gato

    return mejor_mov


# --- SIMULACIÓN DEL JUEGO ---
turno = 1
while True:
    print(f"--- Turno {turno} ---")
    mostrar_laberinto(raton, gato)
    time.sleep(1)

    if raton == gato:
        print("🐱 ¡El gato atrapó al ratón!")
        break
    if raton == salida:
        print("🐭 ¡El ratón escapó por la salida!")
        break

    raton = mover_raton(raton, gato)
    gato = mover_gato(gato, raton)
    turno += 1
