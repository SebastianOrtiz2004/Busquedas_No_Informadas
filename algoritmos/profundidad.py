"""
Algoritmo 2: Búsqueda en Profundidad (Múltiples Soluciones)

Estructura de Datos de la Frontera: PILA (LIFO) - Lista / Stack
Explora el árbol buscando múltiples caminos hacia S_g = (1, 10).
"""

import time
from nucleo.nodo import Nodo
from nucleo.ambiente import AmbienteCuadricula

class BusquedaProfundidad:
    @classmethod
    def resolver(cls, estado_inicial, max_soluciones=5):
        Nodo.reiniciar_contador_ids()
        tiempo_inicio = time.perf_counter()

        raiz = Nodo(estado=estado_inicial, padre=None, accion=None, costo=0, profundidad=0)
        
        if AmbienteCuadricula.es_objetivo(raiz.estado):
            tiempo_fin = time.perf_counter()
            return {
                "exito": True,
                "nodo_solucion": raiz,
                "nodos_solucion": [raiz],
                "camino": raiz.obtener_camino(),
                "todos_caminos": [raiz.obtener_camino()],
                "acciones": [],
                "nodos_expandidos": 0,
                "nodos_generados": 1,
                "tamanio_maximo_frontera": 1,
                "tiempo_ejecucion_ms": (tiempo_fin - tiempo_inicio) * 1000,
                "historial_exploracion": [raiz.estado],
                "nodos_arbol": [raiz]
            }

        frontera = [raiz]
        visitados = set()

        nodos_expandidos = 0
        nodos_generados = 1
        tamanio_maximo_frontera = 1
        historial_exploracion = []
        nodos_arbol = [raiz]
        nodos_solucion = []

        while frontera and len(nodos_solucion) < max_soluciones:
            tamanio_maximo_frontera = max(tamanio_maximo_frontera, len(frontera))
            nodo_actual = frontera.pop()
            
            if nodo_actual.estado in visitados and not AmbienteCuadricula.es_objetivo(nodo_actual.estado):
                continue

            if not AmbienteCuadricula.es_objetivo(nodo_actual.estado):
                visitados.add(nodo_actual.estado)

            nodos_expandidos += 1
            historial_exploracion.append(nodo_actual.estado)

            if AmbienteCuadricula.es_objetivo(nodo_actual.estado):
                nodos_solucion.append(nodo_actual)
                continue

            sucesores = AmbienteCuadricula.obtener_sucesores(nodo_actual.estado)
            for nuevo_estado, accion in sucesores:
                es_meta = AmbienteCuadricula.es_objetivo(nuevo_estado)
                if es_meta or nuevo_estado not in visitados:
                    nodo_hijo = Nodo(
                        estado=nuevo_estado,
                        padre=nodo_actual,
                        accion=accion,
                        costo=nodo_actual.costo + 1,
                        profundidad=nodo_actual.profundidad + 1
                    )
                    nodos_generados += 1
                    nodos_arbol.append(nodo_hijo)
                    frontera.append(nodo_hijo)

        tiempo_fin = time.perf_counter()

        nodo_optimo = min(nodos_solucion, key=lambda n: n.costo) if nodos_solucion else None
        todos_caminos = [n.obtener_camino() for n in nodos_solucion]

        return {
            "exito": len(nodos_solucion) > 0,
            "nodo_solucion": nodo_optimo,
            "nodos_solucion": nodos_solucion,
            "camino": nodo_optimo.obtener_camino() if nodo_optimo else [],
            "todos_caminos": todos_caminos,
            "acciones": nodo_optimo.obtener_secuencia_acciones() if nodo_optimo else [],
            "nodos_expandidos": nodos_expandidos,
            "nodos_generados": nodos_generados,
            "tamanio_maximo_frontera": tamanio_maximo_frontera,
            "tiempo_ejecucion_ms": (tiempo_fin - tiempo_inicio) * 1000,
            "historial_exploracion": historial_exploracion,
            "nodos_arbol": nodos_arbol
        }
