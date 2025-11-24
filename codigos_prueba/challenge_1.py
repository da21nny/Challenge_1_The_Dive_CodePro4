import random
import math
import time
from collections import deque
MAX_PROFUNDIDAD = 3

movimientos = [(1,0), (-1,0), (0,1), (0,-1)] # Variable Globar: Abajo, Arriba, Derecha, Izquierda

# --- GENERACIÓN DEL LABERINTO ---
def crear_laberinto(ancho, alto):
    if ancho % 2 == 0: ancho += 1
    if alto % 2 == 0: alto += 1
    
    # Crear una matriz llena de paredes
    laberinto = [[1 for _ in range(ancho)] for _ in range(alto)]

    # Función recursiva para generar el laberinto
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

    cantidad = (ancho * alto) // 15   # Número de paredes a romper aleatoriamente en porcentaje  
    for _ in range(cantidad):
        x = random.randint(1, ancho - 2)
        y = random.randint(1, alto - 2)
        # Solo romper si es una pared
        if laberinto[y][x] == 1:
            # Contar cuántos lados libres hay alrededor
            libres = 0
            for dx, dy in movimientos:
                nx, ny = x + dx, y + dy
                if laberinto[ny][nx] == 0:
                    libres += 1
            # Si tiene 1 o 2 caminos cerca, romperlo crea rutas interesantes
            if 1 <= libres <= 2:
                laberinto[y][x] = 0
    return laberinto # Retorna el laberinto generado

# Generar laberinto de tamaño fijo
laberinto = crear_laberinto(15, 10)

# --- Funcion de Movimientos Validos ---
def movimientos_validos(posicion, laberinto):
    validos = []
    # Ciclo para verificar cada movimiento posible
    for dx, dy in movimientos:
        nx = posicion[0] + dx
        ny = posicion[1] + dy
        # Verificar si la nueva posición está dentro de los límites y es un camino (0)
        if 0 <= nx < len(laberinto) and 0 <= ny < len(laberinto[0]):
            if laberinto[nx][ny] == 0:
                validos.append((nx, ny))
    return validos #retorna lista de movimientos validos

# --- FUNCIONES DE POSICIONAMIENTO ---
def posicion_libre_laberinto(laberinto):
    filas = len(laberinto)
    columnas = len(laberinto[0])
    while True:
        x = random.randint(0, filas - 1)
        y = random.randint(0, columnas - 1)
        if laberinto[x][y] == 0: #Celda Libre
            return(x,y)

# --- FUNCIONES DE DISTANCIA Y CAMINO ---  
def distancia_real(laberinto, inicio, objetivo):
    if inicio == objetivo:
        return 0
    cola = deque([(inicio, 0)])
    visitados = {inicio}
    while cola:
        (x, y), distancia = cola.popleft()
        for nx, ny in movimientos_validos((x,y),laberinto):
            if (nx, ny) == objetivo:
                return distancia + 1
            if (nx, ny) not in visitados:
                visitados.add((nx, ny))
                cola.append(((nx, ny), distancia + 1)) 
    return math.inf


def calcular_distancia(dist_a, dist_b):
    return abs(dist_a[0] - dist_b[0]) + abs(dist_a[1] - dist_b[1])

#-- Búsqueda de camino usando BFS ---
def existe_camino_bfs(laberinto, inicio, fin):
    queue = deque([inicio])
    visitados = {inicio}
    while queue:
        x, y = queue.popleft()
        if (x, y) == fin:
            return True
        for dx, dy in movimientos:
            nx, ny = x + dx, y + dy
            if 0 <=nx < len(laberinto) and 0 <= ny < len(laberinto[0]):
                if laberinto[nx][ny] == 0 and (nx, ny) not in visitados:
                    visitados.add((nx, ny))
                    queue.append((nx, ny))
    return False

#--- POSICIONAMIENTO DEL RATÓN, GATO ---
def posicionar_gato_raton(laberinto, min_dist):
    while True:
        raton = posicion_libre_laberinto(laberinto)
        gato = posicion_libre_laberinto(laberinto)
        # Asegurar distancia mínima entre ratón y gato
        if calcular_distancia(raton, gato) < min_dist:
            continue

        if not existe_camino_bfs(laberinto, raton, gato):
            continue

        return(raton, gato)

#--- POSICIONAMIENTO DE LA SALIDA ---    
def posicionar_salida(laberinto, raton, gato, min_distancia):
    while True:
        salida = posicion_libre_laberinto(laberinto)
        if calcular_distancia(salida, raton) < min_distancia:
            continue
        if calcular_distancia(salida, gato) < min_distancia:
            continue
        if not existe_camino_bfs(laberinto, raton, salida):
            continue
        if not existe_camino_bfs(laberinto, gato, salida):
            continue
        return salida  

#--- INICIALIZACIÓN DEL JUEGO ---
raton, gato = posicionar_gato_raton(laberinto, 10)
salida = posicionar_salida(laberinto, raton, gato, 10)

#--- FUNCION PARA MOSTRAR EL LABERINTO CON POSICIONES ---
def mostrar_laberinto(raton, gato, raton_visible):
    for i in range(len(laberinto)):
        fila = ""
        for j in range(len(laberinto[0])):
            if (i, j) == raton and raton_visible:
                fila += "🐭"
            elif (i, j) == gato:
                fila += "🐱"
            elif (i, j) == salida:
                fila += "🚪"
            elif laberinto[i][j] == 1:
                fila += "⬜️"
            else:
                fila += "  "
        print(fila)
    print()

def evaluar_estado(laberinto, raton, gato, salida):
    dist_raton_salida = distancia_real(laberinto,raton, salida)
    dist_gato_salida = distancia_real(laberinto,gato, salida)
    dist_raton_gato = distancia_real(laberinto, raton, gato)
    valor = (dist_raton_gato * 3) - (dist_raton_salida * 4)

    #Condicion que penaliza si el gato bloquea salida al raton
    # if dist_gato_salida < dist_raton_salida:
    #     valor =-5
    if raton == gato:
        return -1000
    elif raton == salida:
        return 1000
    desempate = random.random() / 10
    return valor + desempate 


def miniMax(laberinto, raton, gato, salida, profundidad, es_turno_raton):
    if profundidad == 0 or raton == gato or raton == salida:
        return evaluar_estado(laberinto, raton, gato, salida)
    
    if es_turno_raton:
        mejor_valor = -math.inf 
        for mov in movimientos_validos(raton, laberinto):
            valor = miniMax(laberinto, mov, gato, salida, profundidad - 1, False)
            mejor_valor = max(valor, mejor_valor)
        return mejor_valor
    else:
        peor_valor = +math.inf
        for mov in movimientos_validos(gato, laberinto):
            valor = miniMax(laberinto, raton, mov, salida, profundidad - 1, True)
            peor_valor = min(valor, peor_valor)
        return peor_valor

# Mejor Movimiento Raton (MAX)
def mejor_movimiento_raton(laberinto, raton, gato, salida):
    movimientos = movimientos_validos(raton, laberinto)
    mejor_valor = -math.inf
    mejor_mov = raton
    for mov in movimientos:
        valor = miniMax(laberinto, mov, gato, salida, MAX_PROFUNDIDAD, False)
        if valor > mejor_valor:
            mejor_valor = valor
            mejor_mov = mov
    return mejor_mov, mejor_valor

# Mejor Movimiento Gato (MIN)
def mejor_movimiento_gato(laberinto, raton, gato, salida):
    movimientos = movimientos_validos(gato, laberinto)
    mejor_valor = math.inf
    mejor_mov = gato
    for mov in movimientos:
        valor = miniMax(laberinto, raton, mov, salida, MAX_PROFUNDIDAD, True)
        if valor < mejor_valor:
            mejor_valor = valor
            mejor_mov = mov
    return mejor_mov, mejor_valor


contador_turno = 1 #Una variable para contar los turnos dentro del ciclo while
es_turno_raton = True #para que el ciclo while no termine hasta un break en una condicion
while True:
    print(f"Turno: {contador_turno} - {'Raton' if es_turno_raton else 'Gato'}")
    mostrar_laberinto(raton, gato, raton_visible = True)
    time.sleep(0.5)    

    if raton == gato:
        mostrar_laberinto(raton, gato, raton_visible = False)
        print("El gato atrapo al raton")
        break
    if raton == salida:
        mostrar_laberinto(raton, gato, raton_visible = False)
        print("El Raton logró escapar")
        break

    if es_turno_raton:
        #utilizamos un guion (_) para guardar valores que no necesitamos al llamar a la
        #funcion mejor_movimiento, es una convencion en python creando una variable
        #que no utilizaremos
        nuevo_raton, _ = mejor_movimiento_raton(laberinto, raton, gato, salida)
        raton = nuevo_raton
        print(f"Raton se movio a: {raton}")
        if raton == gato:
            mostrar_laberinto(raton, gato, raton_visible = False)
            print("El gato atrapo al raton")
            break
        if raton == salida:
            mostrar_laberinto(raton, gato, raton_visible = False)
            print("El Raton logró escapar")
            break
                
    else:
        #utilizamos un guion (_) para guardar valores que no necesitamos al llamar a la
        #funcion mejor_movimiento, es una convencion en python creando una variable
        #que no utilizaremos
        nuevo_gato, _ = mejor_movimiento_gato(laberinto, raton, gato, salida)
        gato = nuevo_gato
        print(f"Gato se movio a: {gato}")
        if gato == raton:
            mostrar_laberinto(raton, gato, raton_visible = False)
            print("El gato atrapo al raton")
            break

    if contador_turno > 150:
        print("Fin de los turnos, Gato y raton se pusieron a bailar sin parar")
        break

    contador_turno += 1
    es_turno_raton = not es_turno_raton
