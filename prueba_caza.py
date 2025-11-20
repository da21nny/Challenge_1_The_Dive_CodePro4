import math

# --- LABERINTO (0 = libre, 1 = pared) ---
lab = [
    [0, 0, 1, 0, 0],
    [1, 0, 1, 0, 1],
    [0, 0, 0, 0, 0],
    [0, 1, 1, 1, 0],
    [0, 0, 0, 1, 0]
]

raton = (4, 0)   # inicio del ratón
gato = (0, 4)    # inicio del gato
salida = (0, 0)  # salida

# movimientos válidos: abajo, arriba, derecha, izquierda
movimientos = [(1,0), (-1,0), (0,1), (0,-1)]
movimientos_agil = [(1,0), (-1,0), (0,1), (0,-1), (1,1), (-1,1), (1,-1), (-1, -1)]


# --- FUNCIONES AUXILIARES ---
def es_valido(pos):
    x, y = pos
    return 0 <= x < len(lab) and 0 <= y < len(lab[0]) and lab[x][y] == 0

def distancia(a, b):
    # distancia Manhattan (no diagonal)
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

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


# --- FUNCIÓN DE EVALUACIÓN ---
def evaluar(raton, gato):
    """
    Cuanto más lejos esté del gato y más cerca de la salida, mejor.
    Si llega a la salida => valor alto.
    Si el gato lo atrapa => valor bajo.
    """
    if raton == gato:
        return -999
    if raton == salida:
        return 999

    dist_gato = distancia(raton, gato)
    dist_salida = distancia(raton, salida)
    # Prioriza mantenerse lejos del gato, luego acercarse a la salida
    return (dist_gato * 2) - dist_salida


# --- ALGORITMO MINIMAX ---
def minimax(raton, gato, profundidad, turno_max):
    # condiciones terminales
    if profundidad == 0 or raton == gato or raton == salida:
        return evaluar(raton, gato)

    if turno_max:  # turno del ratón
        mejor_valor = -math.inf
        for dx, dy in movimientos_agil:
            nuevo_raton = (raton[0] + dx, raton[1] + dy)
            if es_valido(nuevo_raton):
                valor = minimax(nuevo_raton, gato, profundidad - 1, False)
                mejor_valor = max(mejor_valor, valor)
        return mejor_valor

    else:  # turno del gato
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

    print("🐭 El ratón evalúa sus opciones:")

    for dx, dy in movimientos_agil:
        nuevo_raton = (raton[0] + dx, raton[1] + dy)
        if es_valido(nuevo_raton):
            valor = minimax(nuevo_raton, gato, 3, False)  # profundidad = 3
            print(f" → Movimiento hacia {nuevo_raton} tiene valor {valor}")
            if valor > mejor_valor:
                mejor_valor = valor
                mejor_mov = nuevo_raton

    print(f"✅ El ratón elige moverse a {mejor_mov} (valor {mejor_valor})\n")
    return mejor_mov


# --- MOVIMIENTO DEL GATO ---
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


# --- SIMULACIÓN ---
turno = 1
while True:
    print(f"--- Turno {turno} ---")
    mostrar_laberinto(raton, gato)

    if raton == gato:
        print("🐱 ¡El gato atrapó al ratón!")
        break
    if raton == salida:
        print("🏁 ¡El ratón escapó por la salida!")
        break

    raton = mover_raton(raton, gato)
    gato = mover_gato(gato, raton)
    turno += 1

