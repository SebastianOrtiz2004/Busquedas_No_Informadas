"""
Módulo Núcleo: Clase Nodo (Árbol de Búsqueda)

Representa cada estado explorado durante la búsqueda no informada.
Almacena el puntero al nodo padre para reconstruir el camino solución,
así como la acción ejecutada, el costo del camino acumulado g(n) y la profundidad d.
"""

class Nodo:
    _contador_ids = 0

    def __init__(self, estado, padre=None, accion=None, costo=0, profundidad=0):
        Nodo._contador_ids += 1
        self.id = Nodo._contador_ids
        self.estado = estado          # Tupla (x, y)
        self.padre = padre            # Instancia de Nodo o None (si es raíz S_0)
        self.accion = accion          # Acción que llevó a este estado: "Norte", "Sur", "Este", "Oeste"
        self.costo = costo            # Costo acumulado del camino g(n)
        self.profundidad = profundidad  # Profundidad d en el árbol

    @classmethod
    def reiniciar_contador_ids(cls):
        """Reinicia el contador de IDs de nodos para una nueva búsqueda."""
        cls._contador_ids = 0

    def obtener_camino(self):
        """
        Reconstruye el camino desde el nodo raíz S_0 hasta el nodo actual.
        Devuelve una lista de tuplas: [(estado_0, None), (estado_1, accion_1), ..., (estado_n, accion_n)]
        """
        camino = []
        actual = self
        while actual is not None:
            camino.append((actual.estado, actual.accion, actual.costo, actual.profundidad, actual.id))
            actual = actual.padre
        camino.reverse()
        return camino

    def obtener_secuencia_acciones(self):
        """Devuelve únicamente la secuencia de acciones para llegar al nodo."""
        camino = self.obtener_camino()
        return [paso[1] for paso in camino if paso[1] is not None]

    def __repr__(self):
        return f"Nodo(ID={self.id}, Estado={self.estado}, Profundidad={self.profundidad}, Costo={self.costo})"

    def __eq__(self, otro):
        if isinstance(otro, Nodo):
            return self.estado == otro.estado
        return False

    def __hash__(self):
        return hash(self.estado)
