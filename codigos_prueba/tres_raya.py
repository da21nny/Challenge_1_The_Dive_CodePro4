import math

# ==========================================
# TRES EN RAYA CON MINIMAX
# ==========================================

def imprimir_tablero(tablero):
    """Muestra el tablero de forma visual"""
    print("\n")
    for i in range(3):
        print(" " + " | ".join(tablero[i*3:(i+1)*3]))
        if i < 2:
            print("-----------")
    print("\n")

def verificar_ganador(tablero, jugador):
    """Verifica si un jugador ha ganado"""
    # Combinaciones ganadoras
    ganadas = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Filas
        [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Columnas
        [0, 4, 8], [2, 4, 6]               # Diagonales
    ]
    
    for combo in ganadas:
        if all(tablero[i] == jugador for i in combo):
            return True
    return False

def tablero_lleno(tablero):
    """Verifica si el tablero está lleno"""
    return ' ' not in tablero

def obtener_movimientos_disponibles(tablero):
    """Retorna lista de posiciones vacías"""
    return [i for i in range(9) if tablero[i] == ' ']

def evaluar_tablero(tablero):
    """
    Evalúa el estado del tablero:
    +10 si gana X (MAX)
    -10 si gana O (MIN)
    0 si empate
    """
    if verificar_ganador(tablero, 'X'):
        return 10
    elif verificar_ganador(tablero, 'O'):
        return -10
    else:
        return 0

def minimax(tablero, profundidad, es_maximizador):
    """
    Algoritmo Minimax recursivo
    
    Parámetros:
    - tablero: estado actual del juego
    - profundidad: nivel de recursión (para optimizar)
    - es_maximizador: True si es turno de MAX, False si es MIN
    
    Retorna: mejor puntuación posible
    """
    # Caso base: verificar si el juego terminó
    puntuacion = evaluar_tablero(tablero)
    
    # Si hay ganador, retornar la puntuación ajustada por profundidad
    if puntuacion == 10:
        return puntuacion - profundidad  # Preferir ganar rápido
    if puntuacion == -10:
        return puntuacion + profundidad  # Preferir perder tarde
    
    # Si empate
    if tablero_lleno(tablero):
        return 0
    
    # Turno del Maximizador (X)
    if es_maximizador:
        mejor_valor = -math.inf
        
        for movimiento in obtener_movimientos_disponibles(tablero):
            # Hacer el movimiento
            tablero[movimiento] = 'X'
            
            # Llamada recursiva
            valor = minimax(tablero, profundidad + 1, False)
            
            # Deshacer el movimiento
            tablero[movimiento] = ' '
            
            # Actualizar mejor valor
            mejor_valor = max(mejor_valor, valor)
        
        return mejor_valor
    
    # Turno del Minimizador (O)
    else:
        mejor_valor = math.inf
        
        for movimiento in obtener_movimientos_disponibles(tablero):
            # Hacer el movimiento
            tablero[movimiento] = 'O'
            
            # Llamada recursiva
            valor = minimax(tablero, profundidad + 1, True)
            
            # Deshacer el movimiento
            tablero[movimiento] = ' '
            
            # Actualizar mejor valor
            mejor_valor = min(mejor_valor, valor)
        
        return mejor_valor

def encontrar_mejor_movimiento(tablero):
    """
    Encuentra el mejor movimiento para X usando Minimax
    Retorna la posición óptima
    """
    mejor_valor = -math.inf
    mejor_movimiento = -1
    
    print("🤔 IA pensando...")
    
    for movimiento in obtener_movimientos_disponibles(tablero):
        # Hacer el movimiento
        tablero[movimiento] = 'X'
        
        # Calcular valor con minimax
        valor_movimiento = minimax(tablero, 0, False)
        
        # Deshacer el movimiento
        tablero[movimiento] = ' '
        
        print(f"   Posición {movimiento}: valor = {valor_movimiento}")
        
        # Actualizar mejor movimiento
        if valor_movimiento > mejor_valor:
            mejor_movimiento = movimiento
            mejor_valor = valor_movimiento
    
    print(f"✅ Mejor movimiento: posición {mejor_movimiento} (valor: {mejor_valor})\n")
    return mejor_movimiento

def jugar():
    """Función principal del juego"""
    tablero = [' '] * 9
    
    print("=" * 40)
    print("    TRES EN RAYA - MINIMAX")
    print("=" * 40)
    print("\nPosiciones del tablero:")
    print("\n 0 | 1 | 2")
    print("-----------")
    print(" 3 | 4 | 5")
    print("-----------")
    print(" 6 | 7 | 8\n")
    print("Tú eres O, la IA es X")
    
    input("Presiona Enter para comenzar...")
    
    turno_jugador = True  # Jugador humano empieza
    
    while True:
        imprimir_tablero(tablero)
        
        # Verificar ganador
        if verificar_ganador(tablero, 'O'):
            print("🎉 ¡Ganaste! (Esto no debería pasar con Minimax perfecto)")
            break
        elif verificar_ganador(tablero, 'X'):
            print("🤖 La IA ganó. Minimax es imbatible!")
            break
        elif tablero_lleno(tablero):
            print("🤝 ¡Empate! Bien jugado.")
            break
        
        if turno_jugador:
            # Turno del humano
            try:
                movimiento = int(input("Tu movimiento (0-8): "))
                if movimiento < 0 or movimiento > 8 or tablero[movimiento] != ' ':
                    print("❌ Movimiento inválido. Intenta de nuevo.")
                    continue
                tablero[movimiento] = 'O'
                turno_jugador = False
            except:
                print("❌ Entrada inválida. Usa números del 0 al 8.")
        else:
            # Turno de la IA con Minimax
            movimiento = encontrar_mejor_movimiento(tablero)
            tablero[movimiento] = 'X'
            print(f"🤖 IA juega en posición {movimiento}")
            turno_jugador = True
    
    imprimir_tablero(tablero)
    
    jugar_de_nuevo = input("\n¿Jugar de nuevo? (S/N): ").strip().upper()
    if jugar_de_nuevo == 'S':
        jugar()

# ==========================================
# EJEMPLO SIMPLE DE MINIMAX
# ==========================================

def ejemplo_simple_minimax():
    """
    Ejemplo simplificado para entender Minimax
    Árbol de decisión con valores predefinidos
    """
    print("\n" + "=" * 50)
    print("EJEMPLO SIMPLE: ÁRBOL DE DECISIÓN MINIMAX")
    print("=" * 50)
    
    # Árbol de ejemplo (valores de las hojas)
    print("\nÁrbol de juego:")
    print("                   MAX")
    print("              /     |     \\")
    print("            /       |       \\")
    print("          A         B         C")
    print("        / | \\     / | \\     / | \\")
    print("       3  5  2   8  1  4   6  7  9  <- Valores")
    print("       MIN       MIN       MIN\n")
    
    # Simulación del algoritmo
    valores_a = [3, 5, 2]
    valores_b = [8, 1, 4]
    valores_c = [6, 7, 9]
    
    # MIN elige el mínimo en cada rama
    min_a = min(valores_a)
    min_b = min(valores_b)
    min_c = min(valores_c)
    
    print("Paso 1 - MIN elige el mínimo en cada rama:")
    print(f"  Rama A: min({valores_a}) = {min_a}")
    print(f"  Rama B: min({valores_b}) = {min_b}")
    print(f"  Rama C: min({valores_c}) = {min_c}\n")
    
    # MAX elige el máximo
    opciones = [min_a, min_b, min_c]
    mejor = max(opciones)
    
    print("Paso 2 - MAX elige el máximo:")
    print(f"  Opciones: {opciones}")
    print(f"  MAX elige: {mejor}")
    print(f"  ✅ Por lo tanto, MAX debe elegir la rama {'ABC'[opciones.index(mejor)]}\n")
    print("=" * 50)

# Ejecutar
if __name__ == "__main__":
    # Mostrar ejemplo simple primero
    ejemplo_simple_minimax()
    
    input("\nPresiona Enter para jugar Tres en Raya con Minimax...")
    
    # Jugar tres en raya
    jugar()