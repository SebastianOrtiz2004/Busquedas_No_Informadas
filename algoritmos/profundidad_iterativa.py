"""
Algoritmo 3: Profundidad Iterativa (Optimizado y Múltiples Soluciones)

Estructura de Datos de la Frontera: PILA (LIFO) con Límite L creciente.
Optimizado para registrar únicamente estados únicos en la animación y evitar cuelgues.
"""

import time
from nucleo.nodo import Nodo
from nucleo.ambiente import AmbienteCuadricula

class ProfundidadIterativa:
    @staticmethod
    def _tiene_ciclo(nodo, estado):
        actual = nodo
        while actual:
            if actual.estado == estado:
                return True
            actual = actual.padre
        return False

    @classmethod
    def resolver(cls, estado_inicial, limite_profundidad_maximo=200, max_soluciones=5):
        Nodo.reiniciar_contador_ids()
        tiempo_inicio = time.perf_counter()

        total_nodos_expandidos = 0
        total_nodos_generados = 0
        maxima_frontera_global = 1
        todos_nodos_arbol = []
        nodos_solucion = []

        # Usar conjunto para registrar el historial de exploración único sin duplicados por iteraciones
        historial_set = set()
        historial_exploracion = []

        for limite_profundidad in range(limite_profundidad_maximo + 1):
            raiz = Nodo(estado=estado_inicial, padre=None, accion=None, costo=0, profundidad=0)
            todos_nodos_arbol.append(raiz)
            total_nodos_generados += 1

            if raiz.estado not in historial_set:
                historial_set.add(raiz.estado)
                historial_exploracion.append(raiz.estado)

            frontera = [raiz]
            visitados_iteracion = set()

            while frontera and len(nodos_solucion) < max_soluciones:
                maxima_frontera_global = max(maxima_frontera_global, len(frontera))
                nodo_actual = frontera.pop()

                if nodo_actual.estado in visitados_iteracion and not AmbienteCuadricula.es_objetivo(nodo_actual.estado):
                    continue

                if not AmbienteCuadricula.es_objetivo(nodo_actual.estado):
                    visitados_iteracion.add(nodo_actual.estado)

                total_nodos_expandidos += 1
                
                if nodo_actual.estado not in historial_set:
                    historial_set.add(nodo_actual.estado)
                    historial_exploracion.append(nodo_actual.estado)

                if AmbienteCuadricula.es_objetivo(nodo_actual.estado):
                    # Solo agregar si este camino objetivo es único o diferente
                    if not any(s.estado == nodo_actual.estado and s.costo == nodo_actual.costo for s in nodos_solucion):
                        nodos_solucion.append(nodo_actual)
                    continue

                if nodo_actual.profundidad < limite_profundidad:
                    for nuevo_estado, accion in AmbienteCuadricula.obtener_sucesores(nodo_actual.estado):
                        es_meta = AmbienteCuadricula.es_objetivo(nuevo_estado)
                        if es_meta or nuevo_estado not in visitados_iteracion:
                            nodo_hijo = Nodo(
                                estado=nuevo_estado,
                                padre=nodo_actual,
                                accion=accion,
                                costo=nodo_actual.costo + 1,
                                profundidad=nodo_actual.profundidad + 1
                            )
                            total_nodos_generados += 1
                            todos_nodos_arbol.append(nodo_hijo)
                            frontera.append(nodo_hijo)

            if len(nodos_solucion) >= max_soluciones:
                break

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
            "nodos_expandidos": total_nodos_expandidos,
            "nodos_generados": total_nodos_generados,
            "tamanio_maximo_frontera": maxima_frontera_global,
            "tiempo_ejecucion_ms": (tiempo_fin - tiempo_inicio) * 1000,
            "historial_exploracion": historial_exploracion,
            "nodos_arbol": todos_nodos_arbol
        }
