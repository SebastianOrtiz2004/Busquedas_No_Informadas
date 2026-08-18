"""
Módulo Núcleo: Ambiente del Aula de Clases (Cuadrícula 10x20)

Define el espacio de estados S (10 x 20 = 200 estados),
el Estado Inicial S_0 (aleatorio o personalizado),
el Estado Objetivo S_g (1, 10) fijo,
y la Función Sucesora Succ(s, a) sin condicionales de solución.
"""

import random

class AmbienteCuadricula:
    # Dimensiones fijas de la cuadrícula (Aula de Clases)
    MAX_X = 10  # Ancho (1 a 10)
    MAX_Y = 20  # Largo (1 a 20)
    
    # Estado Objetivo Fijo (Salida del aula)
    ESTADO_OBJETIVO = (1, 10)

    # Definición formal de las Acciones A = {Norte, Sur, Este, Oeste}
    ACCIONES = {
        "Norte": (0, 1),   # Mover Arriba: y + 1
        "Sur":   (0, -1),  # Mover Abajo:  y - 1
        "Este":  (1, 0),   # Mover Derecha: x + 1
        "Oeste": (-1, 0)   # Mover Izquierda: x - 1
    }

    def __init__(self, estado_inicial=None):
        """
        Inicializa el ambiente. Si no se pasa estado_inicial, 
        se genera una posición aleatoria S_0 válida en el rango [1..10] x [1..20].
        """
        if estado_inicial is not None:
            self.validar_estado(estado_inicial)
            self.estado_inicial = estado_inicial
        else:
            self.estado_inicial = self.generar_estado_inicial_aleatorio()

    def generar_estado_inicial_aleatorio(self):
        """Genera un estado S_0 aleatorio (x_0, y_0) dentro de la cuadrícula."""
        x = random.randint(1, self.MAX_X)
        y = random.randint(1, self.MAX_Y)
        return (x, y)

    @classmethod
    def validar_estado(cls, estado):
        """Verifica si un estado (x, y) está dentro de los límites del aula."""
        x, y = estado
        if not (1 <= x <= cls.MAX_X and 1 <= y <= cls.MAX_Y):
            raise ValueError(f"Estado {estado} fuera de los límites de la cuadrícula (1..10, 1..20).")

    @classmethod
    def es_objetivo(cls, estado):
        """
        Test Objetivo (GoalTest):
        Devuelve True si el estado percibido coincide exactamente con S_g (1, 10).
        """
        return estado == cls.ESTADO_OBJETIVO

    @classmethod
    def obtener_sucesores(cls, estado):
        """
        Función Sucesora Formal Succ(s, a):
        Retorna la lista de tuplas (nuevo_estado, accion) para todas las acciones válidas A.
        IMPORTANTE: No utiliza condicionales para resolver el problema ni atajos,
        sólo aplica la física de fronteras del espacio artesiano:
          ARRIBA:    (X, Y+1) si Y < 20
          ABAJO:     (X, Y-1) si Y > 1
          DERECHA:   (X+1, Y) si X < 10
          IZQUIERDA: (X-1, Y) si X > 1
        """
        x, y = estado
        sucesores = []

        # Acción Norte (Arriba)
        if y < cls.MAX_Y:
            sucesores.append(((x, y + 1), "Norte"))

        # Acción Sur (Abajo)
        if y > 1:
            sucesores.append(((x, y - 1), "Sur"))

        # Acción Este (Derecha)
        if x < cls.MAX_X:
            sucesores.append(((x + 1, y), "Este"))

        # Acción Oeste (Izquierda)
        if x > 1:
            sucesores.append(((x - 1, y), "Oeste"))

        return sucesores
