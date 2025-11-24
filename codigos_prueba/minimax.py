def evaluar_estado(laberinto, raton, gato, salida):
    dist_raton_salida = distancia_real(laberinto,raton, salida)
    dist_gato_salida = distancia_real(laberinto,gato, salida)
    dist_raton_gato = distancia_real(laberinto, raton, gato)
    valor = (dist_raton_gato * 3) - (dist_raton_salida * 4)

    #Condicion que penaliza si el gato bloquea salida al raton
    if dist_gato_salida < dist_raton_salida:
        valor =-10
    if raton == gato:
        return -100
    elif raton == salida:
        return 100
    return valor


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