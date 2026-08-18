"""
Algoritmo 4: Búsqueda Bidireccional

Estructura de Datos: DOS COLAS FIFO (deque) - Búsqueda en anchura simultánea.
- Árbol Hacia Adelante (Forward): Desde el Estado Inicial S_0 hacia S_g.
- Árbol Hacia Atrás (Backward): Desde el Estado Objetivo S_g (1, 10) hacia S_0.
Punto de Encuentro: Ocurre cuando un estado generado en una frontera ya fue explorado por la frontera opuesta.
Completitud: Sí.
Optimidad: Sí (para costo unitario c = 1).
Complejidad: Reducción drástica a O(b^(d/2)) en tiempo y memoria.
"""

import time
from collections import deque
from nucleo.nodo import Nodo
from nucleo.ambiente import AmbienteCuadricula

class BusquedaBidireccional:
    @staticmethod
    def resolver(estado_inicial):
        """
        Ejecuta la Búsqueda Bidireccional desde S_0 y S_g = (1, 10).
        """
        Nodo.reiniciar_contador_ids()
        tiempo_inicio = time.perf_counter()

        estado_objetivo = AmbienteCuadricula.ESTADO_OBJETIVO

        # Verificación directa de S_0 == S_g
        if estado_inicial == estado_objetivo:
            raiz = Nodo(estado=estado_inicial, padre=None, accion=None, costo=0, profundidad=0)
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
                "historial_exploracion": [estado_inicial],
                "nodos_arbol": [raiz]
            }

        # Raíz Hacia Adelante (Forward) desde S_0
        nodo_adelante_raiz = Nodo(estado=estado_inicial, padre=None, accion=None, costo=0, profundidad=0)
        frontera_adelante = deque([nodo_adelante_raiz])
        visitados_adelante = {estado_inicial: nodo_adelante_raiz}

        # Raíz Hacia Atrás (Backward) desde S_g = (1, 10)
        nodo_atras_raiz = Nodo(estado=estado_objetivo, padre=None, accion=None, costo=0, profundidad=0)
        frontera_atras = deque([nodo_atras_raiz])
        visitados_atras = {estado_objetivo: nodo_atras_raiz}

        nodos_expandidos = 0
        nodos_generados = 2
        tamanio_maximo_frontera = 2
        historial_exploracion = []
        todos_nodos_arbol = [nodo_adelante_raiz, nodo_atras_raiz]

        estado_interseccion = None
        nodo_interseccion_adelante = None
        nodo_interseccion_atras = None

        while frontera_adelante and frontera_atras:
            tamanio_frontera_actual = len(frontera_adelante) + len(frontera_atras)
            tamanio_maximo_frontera = max(tamanio_maximo_frontera, tamanio_frontera_actual)

            # -------------------------------------------------------------
            # Paso 1: Expansión Hacia Adelante
            # -------------------------------------------------------------
            if frontera_adelante:
                curr_a = frontera_adelante.popleft()
                nodos_expandidos += 1
                historial_exploracion.append(curr_a.estado)

                for nuevo_estado, accion in AmbienteCuadricula.obtener_sucesores(curr_a.estado):
                    if nuevo_estado not in visitados_adelante:
                        hijo_a = Nodo(
                            estado=nuevo_estado,
                            padre=curr_a,
                            accion=accion,
                            costo=curr_a.costo + 1,
                            profundidad=curr_a.profundidad + 1
                        )
                        visitados_adelante[nuevo_estado] = hijo_a
                        nodos_generados += 1
                        todos_nodos_arbol.append(hijo_a)
                        frontera_adelante.append(hijo_a)

                        # ¿Se interseca con el árbol Hacia Atrás?
                        if nuevo_estado in visitados_atras:
                            estado_interseccion = nuevo_estado
                            nodo_interseccion_adelante = hijo_a
                            nodo_interseccion_atras = visitados_atras[nuevo_estado]
                            break

            if estado_interseccion is not None:
                break

            # -------------------------------------------------------------
            # Paso 2: Expansión Hacia Atrás
            # -------------------------------------------------------------
            if frontera_atras:
                curr_t = frontera_atras.popleft()
                nodos_expandidos += 1
                historial_exploracion.append(curr_t.estado)

                mapa_acciones_inversas = {"Norte": "Sur", "Sur": "Norte", "Este": "Oeste", "Oeste": "Este"}

                for estado_previo, accion in AmbienteCuadricula.obtener_sucesores(curr_t.estado):
                    if estado_previo not in visitados_atras:
                        hijo_t = Nodo(
                            estado=estado_previo,
                            padre=curr_t,
                            accion=mapa_acciones_inversas[accion],
                            costo=curr_t.costo + 1,
                            profundidad=curr_t.profundidad + 1
                        )
                        visitados_atras[estado_previo] = hijo_t
                        nodos_generados += 1
                        todos_nodos_arbol.append(hijo_t)
                        frontera_atras.append(hijo_t)

                        # ¿Se interseca con el árbol Hacia Adelante?
                        if estado_previo in visitados_adelante:
                            estado_interseccion = estado_previo
                            nodo_interseccion_adelante = visitados_adelante[estado_previo]
                            nodo_interseccion_atras = hijo_t
                            break

            if estado_interseccion is not None:
                break

        # Reconstrucción del Camino Combinado
        camino_completo = []
        secuencia_acciones = []

        if estado_interseccion is not None:
            # 1. Camino desde S_0 hasta el punto de intersección
            camino_adelante = nodo_interseccion_adelante.obtener_camino()
            camino_completo.extend(camino_adelante)

            # 2. Camino desde el punto de intersección hasta S_g = (1, 10)
            atras_actual = nodo_interseccion_atras
            costo_actual = nodo_interseccion_adelante.costo
            profundidad_actual = nodo_interseccion_adelante.profundidad

            while atras_actual.padre is not None:
                accion_siguiente = atras_actual.accion
                siguiente_estado = atras_actual.padre.estado
                costo_actual += 1
                profundidad_actual += 1
                node_id = atras_actual.padre.id
                camino_completo.append((siguiente_estado, accion_siguiente, costo_actual, profundidad_actual, node_id))
                atras_actual = atras_actual.padre

            secuencia_acciones = [paso[1] for paso in camino_completo if paso[1] is not None]

        tiempo_fin = time.perf_counter()

        nodos_solucion = [nodo_interseccion_adelante] if nodo_interseccion_adelante else []
        todos_caminos = [camino_completo] if camino_completo else []

        return {
            "exito": estado_interseccion is not None,
            "nodo_solucion": nodo_interseccion_adelante,
            "nodos_solucion": nodos_solucion,
            "camino": camino_completo,
            "todos_caminos": todos_caminos,
            "acciones": secuencia_acciones,
            "estado_interseccion": estado_interseccion,
            "nodos_expandidos": nodos_expandidos,
            "nodos_generados": nodos_generados,
            "tamanio_maximo_frontera": tamanio_maximo_frontera,
            "tiempo_ejecucion_ms": (tiempo_fin - tiempo_inicio) * 1000,
            "historial_exploracion": historial_exploracion,
            "nodos_arbol": todos_nodos_arbol
        }
