"""
Módulo Núcleo: Estructuras de Datos Propias (Sin Librerías)

Implementación directa desde cero de las estructuras de datos fundamentales:
- Cola (FIFO - First-In, First-Out) para Búsqueda en Anchura y Bidireccional.
- Pila (LIFO - Last-In, First-Out) para Búsqueda en Profundidad y Profundidad Iterativa.
"""

class Cola:
    """
    Estructura de Datos Cola (FIFO - First-In, First-Out).
    El primer elemento en entrar es el primer elemento en salir.
    """
    def __init__(self, elementos_iniciales=None):
        self._elementos = list(elementos_iniciales) if elementos_iniciales else []

    def encolar(self, elemento):
        """Agrega un elemento al final de la cola."""
        self._elementos.append(elemento)

    def desencolar(self):
        """Extrae y retorna el primer elemento de la cola (extremo frontal)."""
        if self.esta_vacia():
            raise IndexError("Intento de desencolar desde una cola vacía.")
        return self._elementos.pop(0)

    def esta_vacia(self):
        """Verifica si la cola no contiene elementos."""
        return len(self._elementos) == 0

    def obtener_tamanio(self):
        """Retorna la cantidad actual de elementos en la cola."""
        return len(self._elementos)

    def __len__(self):
        return len(self._elementos)

    def __bool__(self):
        return not self.esta_vacia()

    def __repr__(self):
        return f"Cola({self._elementos})"


class Pila:
    """
    Estructura de Datos Pila (LIFO - Last-In, First-Out).
    El último elemento en entrar es el primer elemento en salir.
    """
    def __init__(self, elementos_iniciales=None):
        self._elementos = list(elementos_iniciales) if elementos_iniciales else []

    def apilar(self, elemento):
        """Inserta un elemento en el tope de la pila."""
        self._elementos.append(elemento)

    def desapilar(self):
        """Extrae y retorna el elemento del tope de la pila."""
        if self.esta_vacia():
            raise IndexError("Intento de desapilar desde una pila vacía.")
        return self._elementos.pop()

    def esta_vacia(self):
        """Verifica si la pila no contiene elementos."""
        return len(self._elementos) == 0

    def obtener_tamanio(self):
        """Retorna la cantidad actual de elementos en la pila."""
        return len(self._elementos)

    def __len__(self):
        return len(self._elementos)

    def __bool__(self):
        return not self.esta_vacia()

    def __repr__(self):
        return f"Pila({self._elementos})"
