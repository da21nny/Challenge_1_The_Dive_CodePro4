import copy
import time
import random
import math
from collections import deque

def crear_laberinto(ancho, alto):
    if ancho % 2 == 0: ancho += 1
    if alto % 2 == 0: alto += 1

    laberinto = [[1 for _ in range(ancho)] for _ in range(alto)]

    def generar(x,y):
        laberinto[y][x] = 0
        direccion = [(0,2), (0,-2), (2,0), (-2,0)]
        random.shuffle(direccion)

        for dx, dy in direccion:
            nx = x + dx
            ny = y + dy
            if 1 <= nx < ancho-1 and 1 <= ny < alto-1:
                if laberinto[ny][nx] == 1:
                    laberinto[y + dy//2][x + dx//2] = 0
                    generar(nx,ny)

    inicio_x, inicio_y = 1, 1
    generar(inicio_x, inicio_y)

    # Aumenta la cantidad de caminos alternativos para más rutas
    cantidad = (ancho * alto) // 25  # Número de paredes a romper aleatoriamente en porcentaje  
    for _ in range(cantidad):
        x = random.randint(1, ancho - 2)
        y = random.randint(1, alto - 2)
        # Solo romper si es una pared
        if laberinto[y][x] == 1:
            # Contar cuántos lados libres hay alrededor
            libres = 0
            for dx, dy in [(1,0),(-1,0),(0,1),(0,-1)]:
                nx, ny = x + dx, y + dy
                if laberinto[ny][nx] == 0:
                    libres += 1
            # Si tiene 1 o 2 caminos cerca, romperlo crea rutas interesantes
            if 1 <= libres <= 2:
                laberinto[y][x] = 0

    return laberinto

laberinto = crear_laberinto(20, 10)

tamanho = len(laberinto)
ancho_lab = len(laberinto[0])

# Posición fija de la salida (esquina inferior derecha)
salida = (tamanho-2, ancho_lab-2)
laberinto[salida[0]][salida[1]] = 0  # asegurar salida como camino

# --- Generar 3 quesos aleatorios en posiciones válidas ---
quesos = []
def generar_quesos(cantidad=3):
    global quesos
    quesos = []
    posiciones_ocupadas = {salida}
    
    for _ in range(cantidad):
        while True:
            x = random.randrange(1, tamanho-1)
            y = random.randrange(1, ancho_lab-1)
            pos = (x, y)
            if laberinto[x][y] == 0 and pos not in posiciones_ocupadas:
                quesos.append(pos)
                posiciones_ocupadas.add(pos)
                break

generar_quesos(3)

def mostrar_laberinto(raton, gato):
    for i in range(len(laberinto)):
        fila = ""
        for j in range(len(laberinto[0])):
            if (i, j) == raton:
                fila += "🐭"
            elif (i, j) == gato:
                fila += "🐱"
            elif (i, j) == salida:
                fila += "🚪"
            elif (i, j) in quesos:
                fila += "🧀"
            elif laberinto[i][j] == 1:
                fila += "⬜️"
            else:
                fila += "  "
        print(fila)
    print()

MAX_PROFUNDIDAD = 3

# --- Obtener movimientos válidos (4 direcciones, sin atravesar muros) ---
def movimientos_validos(laberinto, pos):
    direcciones = [(1,0), (-1,0), (0,1), (0,-1)]
    validos = []
    for dx, dy in direcciones:
        nx, ny = pos[0] + dx, pos[1] + dy
        if 0 <= nx < len(laberinto) and 0 <= ny < len(laberinto[0]):
            if laberinto[nx][ny] == 0:
                validos.append((nx, ny))
    return validos

# --- Distancia real (BFS) que respeta paredes ---
def distancia_real(laberinto, inicio, objetivo):
    if inicio == objetivo:
        return 0
    cola = deque([(inicio, 0)]) 
    visitados = {inicio}
    while cola:
        (x, y), dist = cola.popleft()
        for nx, ny in movimientos_validos(laberinto, (x, y)):
            if (nx, ny) == objetivo:
                return dist + 1
            if (nx, ny) not in visitados:
                visitados.add((nx, ny))
                cola.append(((nx, ny), dist + 1))
    return math.inf

def elegir_posiciones_randomizadas(laberinto, salida, prefer_equal_distance=True):
    celdas = []
    for i in range(len(laberinto)):
        for j in range(len(laberinto[0])):
            if laberinto[i][j] == 0 and (i, j) != salida and (i, j) not in quesos:
                d = distancia_real(laberinto, (i, j), salida)
                if d != math.inf:
                    celdas.append(((i, j), d))

    if not celdas:
        return (1,1), (tamanho-2,1)

    if prefer_equal_distance:
        grupos = {}
        for pos, d in celdas:
            grupos.setdefault(d, []).append(pos)
        keys = list(grupos.keys())
        keys.sort(reverse=True)
        for d in keys:
            grupo = grupos[d]
            if len(grupo) >= 2:
                max_attempts = 50
                max_dim = max(len(laberinto), len(laberinto[0]))
                threshold = random.randint(2, max(2, max_dim//3))
                for _ in range(max_attempts):
                    a, b = random.sample(grupo, 2)
                    manh = abs(a[0]-b[0]) + abs(a[1]-b[1])
                    if manh >= threshold:
                        return a, b
                return tuple(random.sample(grupo, 2))

    posiciones = [p for p, _ in celdas]
    max_attempts = 200
    max_dim = max(len(laberinto), len(laberinto[0]))
    min_separacion = random.randint(2, max(2, max_dim//4))
    for _ in range(max_attempts):
        a, b = random.sample(posiciones, 2)
        if abs(a[0]-b[0]) + abs(a[1]-b[1]) >= min_separacion:
            return a, b

    return tuple(random.sample(posiciones, 2))

raton, gato = elegir_posiciones_randomizadas(laberinto, salida, prefer_equal_distance=True)
laberinto[raton[0]][raton[1]] = 0
laberinto[gato[0]][gato[1]] = 0

# --- Evaluar un estado desde el punto de vista del ratón ---
def evaluar_estado(laberinto, raton, gato, salida):
    dist_raton_salida = distancia_real(laberinto, raton, salida)
    dist_raton_gato = distancia_real(laberinto, raton, gato)
    dist_gato_salida = distancia_real(laberinto, gato, salida)

    # Base: cuanto más lejos del gato y más cerca de la salida, mejor
    valor = (dist_raton_gato * 3) - (dist_raton_salida * 4)

    # Bonus por quesos cercanos
    queso_cercano = float('inf')
    for queso in quesos:
        d = distancia_real(laberinto, raton, queso)
        if d != math.inf:
            queso_cercano = min(queso_cercano, d)
    
    if queso_cercano != float('inf'):
        valor += (5 - queso_cercano) * 2  # Bonificación por estar cerca de quesos

    # Penalización si el gato bloquea la salida
    if dist_gato_salida < dist_raton_salida:
        valor -= 10

    if raton == gato:
        return -1000
    if raton == salida:
        return 1000

    return valor

# --- Minimax genérico ---
def minimax(laberinto, raton, gato, salida, profundidad, es_turno_raton):
    if profundidad == 0 or raton == gato or raton == salida:
        return evaluar_estado(laberinto, raton, gato, salida)

    if es_turno_raton:
        mejor = -math.inf
        for mov in movimientos_validos(laberinto, raton):
            valor = minimax(laberinto, mov, gato, salida, profundidad - 1, False)
            mejor = max(mejor, valor)
        return mejor
    else:
        peor = math.inf
        for mov in movimientos_validos(laberinto, gato):
            valor = minimax(laberinto, raton, mov, salida, profundidad - 1, True)
            peor = min(peor, valor)
        return peor

# --- Ratón (MAX) ---
def mejor_movimiento_raton(laberinto, raton, gato, salida):
    movimientos = movimientos_validos(laberinto, raton)
    mejor_valor = -math.inf
    mejor_mov = raton

    for mov in movimientos:
        valor = minimax(laberinto, mov, gato, salida, MAX_PROFUNDIDAD, False)
        if valor > mejor_valor:
            mejor_valor = valor
            mejor_mov = mov
    return mejor_mov, mejor_valor

# --- Gato (MIN) ---
def mejor_movimiento_gato(laberinto, raton, gato, salida):
    movimientos = movimientos_validos(laberinto, gato)
    mejor_valor = math.inf
    mejor_mov = gato

    for mov in movimientos:
        valor = minimax(laberinto, raton, mov, salida, MAX_PROFUNDIDAD, True)
        if valor < mejor_valor:
            mejor_valor = valor
            mejor_mov = mov
    return mejor_mov, mejor_valor

# --- Bucle principal de turnos ---
print("\n--- Simulación de turnos con Quesos ---\n")

turno = 1
es_turno_raton = True
quesos_comidos = 0
turno_extra_raton = False  # Bandera para turno extra

while True:
    print(f"Turno {turno} - {'Ratón' if es_turno_raton else 'Gato'} | Quesos comidos: {quesos_comidos}")
    mostrar_laberinto(raton, gato)
    time.sleep(0.5)

    # Estados terminales
    if raton == gato:
        print("🐱 El gato atrapó al ratón.")
        break
    if raton == salida:
        print("🐭 El ratón escapó por la salida.")
        break

    if es_turno_raton:
        nuevo_raton, _ = mejor_movimiento_raton(laberinto, raton, gato, salida)
        raton = nuevo_raton
        print(f"Ratón se movió a {raton}")
        
        # Verificar si el ratón comió un queso
        if raton in quesos:
            quesos.remove(raton)
            quesos_comidos += 1
            turno_extra_raton = True
            print(f"🧀 ¡Ratón comió un queso! Obtiene un turno extra.")
        
        # Verificar condiciones después del movimiento
        if raton == gato:
            print("🐱 El gato atrapó al ratón.")
            break
        if raton == salida:
            print("🐭 El ratón escapó por la salida.")
            break
        
        # Si el ratón tiene turno extra, le damos otro turno
        if turno_extra_raton:
            turno_extra_raton = False
            print("⭐ Ratón tiene un turno extra.")
            continue  # Salta al siguiente turno sin cambiar es_turno_raton
    else:
        nuevo_gato, _ = mejor_movimiento_gato(laberinto, raton, gato, salida)
        gato = nuevo_gato
        print(f"Gato se movió a {gato}")
        
        # Verificar condiciones después del movimiento
        if raton == gato:
            print("🐱 El gato atrapó al ratón.")
            break

    turno += 1
    es_turno_raton = not es_turno_raton

    if turno > 150:
        print("⏳ Empate por tiempo.")
        break

mostrar_laberinto(raton, gato)
print(f"Quesos comidos: {quesos_comidos}")
