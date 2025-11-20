import random

# -------------------------
# Generador de laberintos
# -------------------------
def crear_laberinto_sin_paredes_exteriores(ancho, alto, semilla=None):
    """
    Genera un laberinto con el algoritmo DFS recursivo.
    A diferencia del generador clásico, al final se *abren las paredes exteriores*
    para que no haya bordes totalmente cerrados.
    - ancho, alto: recomendados impares (se ajustan si no lo son)
    - devuelve una matriz lab[y][x] con 0 = camino, 1 = pared
    """
    if semilla is not None:
        random.seed(semilla)

    # Asegurar dimensiones impares (hace más simple DFS de celdas de 2 en 2)
    if ancho % 2 == 0:
        ancho += 1
    if alto % 2 == 0:
        alto += 1

    # Inicializar todas las celdas como paredes (1)
    lab = [[1 for _ in range(ancho)] for _ in range(alto)]

    # DFS recursivo: trabajamos sobre celdas "impares" para dejar paredes intermedias
    def generar(x, y):
        lab[y][x] = 0  # marcar como camino
        direcciones = [(0,2),(0,-2),(2,0),(-2,0)]
        random.shuffle(direcciones)
        for dx, dy in direcciones:
            nx, ny = x + dx, y + dy
            # comprobar límites interiores (dejamos 0..ancho-1, 0..alto-1)
            if 0 < nx < ancho and 0 < ny < alto and lab[ny][nx] == 1:
                # romper la pared intermedia
                lab[y + dy//2][x + dx//2] = 0
                generar(nx, ny)

    # Empezar desde una celda impar interior (1,1)
    generar(1, 1)

    # ---- Abrir las paredes exteriores ----
    # Convertimos toda la fila superior, inferior y columnas laterales en caminos (0)
    # para que no existan muros exteriores.
    for x in range(ancho):
        lab[0][x] = 0        # fila superior
        lab[alto-1][x] = 0   # fila inferior
    for y in range(alto):
        lab[y][0] = 0        # col izquierda
        lab[y][ancho-1] = 0  # col derecha

    return lab


# -------------------------
# Utilidades: mostrar y colocar entidades
# -------------------------
def mostrar_laberinto(lab, raton=None, gato=None, salida=None):
    simbolos = {1: "█", 0: "."}
    for y in range(len(lab)):
        fila = ""
        for x in range(len(lab[0])):
            pos = (y, x)
            if raton is not None and pos == raton:
                fila += "R "
            elif gato is not None and pos == gato:
                fila += "G "
            elif salida is not None and pos == salida:
                fila += "S "
            else:
                fila += simbolos[lab[y][x]] + " "
        print(fila)
    print()


def celdas_libres(lab):
    libres = []
    for y in range(len(lab)):
        for x in range(len(lab[0])):
            if lab[y][x] == 0:
                libres.append((y, x))
    return libres


def colocar_entidades_aleatorio(lab, semilla=None):
    """
    Coloca raton, gato y salida en celdas libres distintas.
    Devuelve tuplas (raton, gato, salida) en formato (fila, columna).
    """
    if semilla is not None:
        random.seed(semilla)

    libres = celdas_libres(lab)
    if len(libres) < 3:
        raise ValueError("No hay suficientes celdas libres para colocar entidades")

    raton = random.choice(libres)
    libres.remove(raton)
    gato = random.choice(libres)
    libres.remove(gato)

    # Colocar la salida preferentemente en el borde si hay libres, sino en cualquier libre
    bordes = [c for c in libres if c[0] in (0, len(lab)-1) or c[1] in (0, len(lab[0])-1)]
    if bordes:
        salida = random.choice(bordes)
    else:
        salida = random.choice(libres)

    return raton, gato, salida


# -------------------------
# EJEMPLO DE USO
# -------------------------
if __name__ == "__main__":
    WIDTH = 21   # ancho (columnas)
    HEIGHT = 15  # alto (filas)

    lab = crear_laberinto_sin_paredes_exteriores(WIDTH, HEIGHT, semilla=42)
    raton, gato, salida = colocar_entidades_aleatorio(lab, semilla=123)

    print("Laberinto generado (sin paredes exteriores):\n")
    mostrar_laberinto(lab, raton=raton, gato=gato, salida=salida)
