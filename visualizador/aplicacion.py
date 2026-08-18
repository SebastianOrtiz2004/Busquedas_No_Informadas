"""
Módulo Visualizer: Aplicación Gráfica Tkinter

Dashboard interactivo para el Agente de Búsquedas No Informadas:
- Pestaña 1: Cuadrícula del Aula 10x20 con animación ultra fluida sin cuelgues.
- Pestaña 2: Dibujo Gráfico del Árbol con colores de ALTO CONTRASTE y máxima distinción visual.
- Pestaña 3: Tabla de Jerarquía de Nodos.
- Pestaña 4: Análisis Complejidad y Métricas Comparativas Teóricas vs Empíricas.
"""

import sys
import os
import random
import time
import tkinter as tk
from tkinter import ttk, messagebox

from nucleo.ambiente import AmbienteCuadricula
from nucleo.nodo import Nodo
from nucleo.metricas import MetricasBusqueda

from algoritmos.anchura import BusquedaAnchura
from algoritmos.profundidad import BusquedaProfundidad
from algoritmos.profundidad_iterativa import ProfundidadIterativa
from algoritmos.bidireccional import BusquedaBidireccional

class AplicacionVisualizador:
    def __init__(self, raiz):
        self.raiz = raiz
        self.raiz.title("Agentes de Búsqueda No Informada - Aula de Clases (10x20)")
        self.raiz.geometry("1360x880")
        self.raiz.minsize(1024, 720)

        # Paleta de Colores de ALTO CONTRASTE para Distinción Visual Inmediata
        self.color_fondo = "#0f111a"
        self.color_panel = "#1a1c29"
        self.color_texto = "#ffffff"
        self.color_acento = "#00d2ff"
        
        # Colores de Nodos y Caminos súper reconocibles
        self.color_inicio = "#FF007F"       # Magenta / Rosa Neón (S_0)
        self.color_meta = "#00FF66"         # Verde Esmeralda Neón (S_g)
        self.color_camino_optimo = "#FFD700"# Dorado / Amarillo Neón (Camino Óptimo)
        self.color_camino_alt = "#FF6600"   # Naranja Neón (Caminos Alternativos)
        self.color_visitado = "#00BFFF"     # Azul Cyan (Explorado en cuadrícula)
        self.color_nodo_normal = "#1b1e2b"  # Oscuro para nodos normales del árbol

        self.raiz.configure(bg=self.color_fondo)
        self.configurar_estilos()

        self.ambiente = AmbienteCuadricula()
        self.resultado_algoritmo_actual = None
        self.animacion_en_ejecucion = False
        self.tarea_animacion = None

        self.crear_diseno()

    def configurar_estilos(self):
        estilo = ttk.Style()
        estilo.theme_use("clam")
        
        estilo.configure("TFrame", background=self.color_fondo)
        estilo.configure("Panel.TFrame", background=self.color_panel)
        estilo.configure("TLabel", background=self.color_fondo, foreground=self.color_texto, font=("Segoe UI", 10))
        estilo.configure("Header.TLabel", font=("Segoe UI", 14, "bold"), foreground=self.color_acento)
        estilo.configure("Subtitle.TLabel", font=("Segoe UI", 10, "italic"), foreground="#a0a5c0")
        
        estilo.configure("TButton", font=("Segoe UI", 10, "bold"), background="#2a2e42", foreground="#ffffff", borderwidth=0)
        estilo.map("TButton", background=[("active", "#3d4361")])

        estilo.configure("Accent.TButton", background=self.color_acento, foreground="#000000")
        estilo.map("Accent.TButton", background=[("active", "#80e5ff")])

        estilo.configure("TNotebook", background=self.color_fondo, borderwidth=0)
        estilo.configure("TNotebook.Tab", background=self.color_panel, foreground=self.color_texto, padding=[12, 6], font=("Segoe UI", 10, "bold"))
        estilo.map("TNotebook.Tab", background=[("selected", self.color_acento)], foreground=[("selected", "#000000")])

        estilo.configure("Treeview", background="#12141f", foreground=self.color_texto, fieldbackground="#12141f", rowheight=24)
        estilo.configure("Treeview.Heading", background="#222638", foreground=self.color_acento, font=("Segoe UI", 10, "bold"))

    def crear_diseno(self):
        panel_superior = ttk.Frame(self.raiz, style="Panel.TFrame", padding=15)
        panel_superior.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)

        lbl_titulo = ttk.Label(panel_superior, text="🎓 IA: Agente de Búsqueda No Informada (Aula 10x20)", style="Header.TLabel", background=self.color_panel)
        lbl_titulo.pack(side=tk.LEFT, padx=5)

        btn_aleatorio = ttk.Button(panel_superior, text="🎲 Generar S₀ Aleatorio", command=self.al_generar_s0_aleatorio)
        btn_aleatorio.pack(side=tk.LEFT, padx=10)

        ttk.Label(panel_superior, text="Estrategia:", background=self.color_panel, font=("Segoe UI", 10, "bold")).pack(side=tk.LEFT, padx=(15, 5))
        self.var_algoritmo = tk.StringVar(value="Anchura")
        combo_algo = ttk.Combobox(panel_superior, textvariable=self.var_algoritmo, state="readonly", width=22, font=("Segoe UI", 10))
        combo_algo['values'] = ("Anchura", "Profundidad", "Profundidad Iterativa", "Bidireccional")
        combo_algo.pack(side=tk.LEFT, padx=5)

        btn_ejecutar = ttk.Button(panel_superior, text="▶️ Resolver", style="Accent.TButton", command=self.al_ejecutar_seleccionado)
        btn_ejecutar.pack(side=tk.LEFT, padx=10)

        btn_comparar = ttk.Button(panel_superior, text="🚀 Comparar las 4 Estrategias", command=self.al_comparar_todos)
        btn_comparar.pack(side=tk.LEFT, padx=5)

        ttk.Label(panel_superior, text="Velocidad (ms):", background=self.color_panel).pack(side=tk.LEFT, padx=(20, 5))
        self.deslizador_velocidad = tk.Scale(panel_superior, from_=5, to=300, orient=tk.HORIZONTAL, bg=self.color_panel, fg=self.color_texto, highlightthickness=0, length=120)
        self.deslizador_velocidad.set(30)
        self.deslizador_velocidad.pack(side=tk.LEFT, padx=5)

        self.pestañas = ttk.Notebook(self.raiz)
        self.pestañas.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))

        # Pestaña 1: Cuadrícula del Aula
        self.pestana_cuadricula = ttk.Frame(self.pestañas)
        self.pestañas.add(self.pestana_cuadricula, text="🗺️ Cuadrícula del Aula (10x20)")
        self.configurar_pestana_cuadricula()

        # Pestaña 2: Dibujo Gráfico del Árbol de Búsqueda
        self.pestana_arbol_grafico = ttk.Frame(self.pestañas)
        self.pestañas.add(self.pestana_arbol_grafico, text="🌲 Dibujo Gráfico del Árbol")
        self.configurar_pestana_arbol_grafico()

        # Pestaña 3: Tabla de Jerarquía de Nodos
        self.pestana_arbol_tabla = ttk.Frame(self.pestañas)
        self.pestañas.add(self.pestana_arbol_tabla, text="📋 Jerarquía de Nodos (Tabla)")
        self.configurar_pestana_arbol_tabla()

        # Pestaña 4: Tabla Comparativa Académica
        self.pestana_metricas = ttk.Frame(self.pestañas)
        self.pestañas.add(self.pestana_metricas, text="📊 Análisis Complejidad y Métricas")
        self.configurar_pestana_metricas()

        self.actualizar_etiqueta_info()
        self.dibujar_cuadricula()

    def configurar_pestana_cuadricula(self):
        panel_izq = ttk.Frame(self.pestana_cuadricula)
        panel_izq.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)

        panel_der = ttk.Frame(self.pestana_cuadricula, style="Panel.TFrame", padding=15)
        panel_der.pack(side=tk.RIGHT, fill=tk.Y, padx=10, pady=10)

        self.tamanio_celda = 28
        ancho_lienzo = 10 * self.tamanio_celda + 40
        alto_lienzo = 20 * self.tamanio_celda + 40

        self.lienzo = tk.Canvas(panel_izq, width=ancho_lienzo, height=alto_lienzo, bg="#08090e", highlightthickness=1, highlightbackground="#2a2e42")
        self.lienzo.pack(anchor=tk.CENTER, expand=True)
        self.lienzo.bind("<Button-1>", self.al_hacer_clic_lienzo)

        ttk.Label(panel_der, text="📌 Estado Actual del Agente", style="Header.TLabel", background=self.color_panel).pack(anchor=tk.W, pady=(0, 10))
        
        self.lbl_s0_val = ttk.Label(panel_der, text="Estado Inicial (S₀): (x, y)", background=self.color_panel, font=("Segoe UI", 11, "bold"))
        self.lbl_s0_val.pack(anchor=tk.W, pady=2)

        self.lbl_sg_val = ttk.Label(panel_der, text="Estado Objetivo (S_g): (1, 10)", background=self.color_panel, font=("Segoe UI", 11, "bold"), foreground=self.color_meta)
        self.lbl_sg_val.pack(anchor=tk.W, pady=2)

        ttk.Separator(panel_der, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=10)

        self.lbl_estado = ttk.Label(panel_der, text="Métricas de la Búsqueda:", style="Header.TLabel", background=self.color_panel)
        self.lbl_estado.pack(anchor=tk.W, pady=5)

        self.lbl_res_nodos_exp = ttk.Label(panel_der, text="• Nodos Expandidos: -", background=self.color_panel)
        self.lbl_res_nodos_exp.pack(anchor=tk.W, pady=2)

        self.lbl_res_nodos_gen = ttk.Label(panel_der, text="• Nodos Generados: -", background=self.color_panel)
        self.lbl_res_nodos_gen.pack(anchor=tk.W, pady=2)

        self.lbl_res_soluciones_total = ttk.Label(panel_der, text="• Soluciones Encontradas: -", background=self.color_panel, font=("Segoe UI", 10, "bold"), foreground=self.color_meta)
        self.lbl_res_soluciones_total.pack(anchor=tk.W, pady=2)

        self.lbl_res_frontera = ttk.Label(panel_der, text="• Máx. Memoria Frontera: -", background=self.color_panel)
        self.lbl_res_frontera.pack(anchor=tk.W, pady=2)

        self.lbl_res_tiempo = ttk.Label(panel_der, text="• Tiempo de Ejecución: -", background=self.color_panel)
        self.lbl_res_tiempo.pack(anchor=tk.W, pady=2)

        self.lbl_res_largo_camino = ttk.Label(panel_der, text="• Camino Óptimo (Costo Min.): -", background=self.color_panel)
        self.lbl_res_largo_camino.pack(anchor=tk.W, pady=2)

        ttk.Separator(panel_der, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=10)

        ttk.Label(panel_der, text="Leyenda de Colores:", background=self.color_panel, font=("Segoe UI", 10, "bold")).pack(anchor=tk.W, pady=5)
        
        marco_leyenda = ttk.Frame(panel_der, style="Panel.TFrame")
        marco_leyenda.pack(anchor=tk.W)
        
        self.crear_item_leyenda(marco_leyenda, self.color_inicio, "Posición Inicial del Agente (S₀)")
        self.crear_item_leyenda(marco_leyenda, self.color_meta, "Salida / Objetivo S_g = (1, 10)")
        self.crear_item_leyenda(marco_leyenda, self.color_visitado, "Nodos Visitados / Expandidos")
        self.crear_item_leyenda(marco_leyenda, self.color_camino_optimo, "Camino Solución Óptimo")
        self.crear_item_leyenda(marco_leyenda, self.color_camino_alt, "Ramas de Soluciones Alternativas")

    def crear_item_leyenda(self, padre, color, texto):
        f = ttk.Frame(padre, style="Panel.TFrame")
        f.pack(anchor=tk.W, pady=2)
        c = tk.Canvas(f, width=16, height=16, bg=self.color_panel, highlightthickness=0)
        c.create_rectangle(1, 1, 15, 15, fill=color, outline="#ffffff")
        c.pack(side=tk.LEFT, padx=(0, 5))
        ttk.Label(f, text=texto, background=self.color_panel, font=("Segoe UI", 9)).pack(side=tk.LEFT)

    def dibujar_cuadricula(self, estados_visitados=None, estados_camino=None):
        self.lienzo.delete("all")
        estados_visitados = set(estados_visitados) if estados_visitados else set()
        estados_camino = set(estados_camino) if estados_camino else set()

        desplazamiento_x = 20
        desplazamiento_y = 20

        for x in range(1, 11):
            for y in range(1, 21):
                canvas_x1 = desplazamiento_x + (x - 1) * self.tamanio_celda
                canvas_y1 = desplazamiento_y + (20 - y) * self.tamanio_celda
                canvas_x2 = canvas_x1 + self.tamanio_celda
                canvas_y2 = canvas_y1 + self.tamanio_celda

                estado = (x, y)
                fill_color = "#12141f"
                outline_color = "#222638"

                if estado == self.ambiente.estado_inicial and estado == AmbienteCuadricula.ESTADO_OBJETIVO:
                    fill_color = "#cba6f7"
                elif estado == self.ambiente.estado_inicial:
                    fill_color = self.color_inicio
                elif estado == AmbienteCuadricula.ESTADO_OBJETIVO:
                    fill_color = self.color_meta
                elif estado in estados_camino:
                    fill_color = self.color_camino_optimo
                elif estado in estados_visitados:
                    fill_color = self.color_visitado

                self.lienzo.create_rectangle(canvas_x1, canvas_y1, canvas_x2, canvas_y2, fill=fill_color, outline=outline_color)

                if estado == AmbienteCuadricula.ESTADO_OBJETIVO:
                    self.lienzo.create_text((canvas_x1 + canvas_x2)/2, (canvas_y1 + canvas_y2)/2, text="S_g", fill="#000000", font=("Segoe UI", 9, "bold"))
                elif estado == self.ambiente.estado_inicial:
                    self.lienzo.create_text((canvas_x1 + canvas_x2)/2, (canvas_y1 + canvas_y2)/2, text="S₀", fill="#ffffff", font=("Segoe UI", 9, "bold"))

        for x in range(1, 11):
            cx = desplazamiento_x + (x - 0.5) * self.tamanio_celda
            self.lienzo.create_text(cx, desplazamiento_y + 20 * self.tamanio_celda + 10, text=str(x), fill="#a0a5c0", font=("Segoe UI", 8))

        for y in range(1, 21):
            cy = desplazamiento_y + (20 - y + 0.5) * self.tamanio_celda
            self.lienzo.create_text(desplazamiento_x - 10, cy, text=str(y), fill="#a0a5c0", font=("Segoe UI", 8))

    def al_hacer_clic_lienzo(self, evento):
        desplazamiento_x = 20
        desplazamiento_y = 20
        grid_x = int((evento.x - desplazamiento_x) // self.tamanio_celda) + 1
        grid_y = 20 - int((evento.y - desplazamiento_y) // self.tamanio_celda)

        if 1 <= grid_x <= 10 and 1 <= grid_y <= 20:
            self.ambiente.estado_inicial = (grid_x, grid_y)
            self.actualizar_etiqueta_info()
            self.dibujar_cuadricula()

    def actualizar_etiqueta_info(self):
        self.lbl_s0_val.config(text=f"Estado Inicial (S₀): {self.ambiente.estado_inicial}")

    def al_generar_s0_aleatorio(self):
        self.ambiente.estado_inicial = self.ambiente.generar_estado_inicial_aleatorio()
        self.actualizar_etiqueta_info()
        self.dibujar_cuadricula()

    # -----------------------------------------------------------------
    # Pestaña 2: Dibujo Gráfico del Árbol de Búsqueda (Alto Contraste)
    # -----------------------------------------------------------------
    def configurar_pestana_arbol_grafico(self):
        contenedor = ttk.Frame(self.pestana_arbol_grafico, padding=10)
        contenedor.pack(fill=tk.BOTH, expand=True)

        panel_top = ttk.Frame(contenedor)
        panel_top.pack(fill=tk.X, pady=(0, 5))

        ttk.Label(panel_top, text="🌲 Dibujo Gráfico del Árbol de Búsqueda (Alto Contraste Visual)", style="Header.TLabel").pack(anchor=tk.W)
        self.lbl_arbol_resumen = ttk.Label(panel_top, text="Genera una búsqueda para ver el árbol con TODAS las soluciones encontradas y la más ÓPTIMA.", style="Subtitle.TLabel")
        self.lbl_arbol_resumen.pack(anchor=tk.W, pady=(0, 5))

        frame_canvas = ttk.Frame(contenedor)
        frame_canvas.pack(fill=tk.BOTH, expand=True)

        self.lienzo_arbol = tk.Canvas(frame_canvas, bg="#08090e", highlightthickness=1, highlightbackground="#2a2e42")
        scroll_y = ttk.Scrollbar(frame_canvas, orient=tk.VERTICAL, command=self.lienzo_arbol.yview)
        scroll_x = ttk.Scrollbar(frame_canvas, orient=tk.HORIZONTAL, command=self.lienzo_arbol.xview)

        self.lienzo_arbol.configure(yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)

        scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
        scroll_x.pack(side=tk.BOTTOM, fill=tk.X)
        self.lienzo_arbol.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    def dibujar_arbol_grafico(self, nodos_arbol, resultado_dict=None):
        self.lienzo_arbol.delete("all")

        if not nodos_arbol:
            self.lbl_arbol_resumen.config(text="No hay árbol generado para mostrar.")
            return

        camino_optimo = resultado_dict.get('camino', []) if resultado_dict else []
        nodos_solucion = resultado_dict.get('nodos_solucion', []) if resultado_dict else []
        todos_caminos = resultado_dict.get('todos_caminos', []) if resultado_dict else []

        ids_camino_optimo = {paso[4] for paso in camino_optimo} if camino_optimo else set()
        
        ids_todos_caminos = set()
        for c in todos_caminos:
            for paso in c:
                ids_todos_caminos.add(paso[4])

        costo_optimo = camino_optimo[-1][2] if camino_optimo else 0
        largo_optimo = len(camino_optimo) - 1 if camino_optimo else 0

        info_soluciones = f"Total Nodos: {len(nodos_arbol)} | Soluciones Encontradas: {len(nodos_solucion)} | "
        if nodos_solucion:
            costos_sol = [f"Sol#{i+1}: {n.costo} pasos" for i, n in enumerate(nodos_solucion)]
            info_soluciones += f"Óptima (Dorado): {largo_optimo} pasos | Alternativas (Naranja): [{', '.join(costos_sol)}]"
        else:
            info_soluciones += "No se alcanzó el objetivo en esta búsqueda."

        self.lbl_arbol_resumen.config(text=info_soluciones)

        # Organizar por niveles de profundidad
        niveles = {}
        for nodo in nodos_arbol:
            d = nodo.profundidad
            if d not in niveles:
                niveles[d] = []
            niveles[d].append(nodo)

        posiciones = {}
        distancia_y = 80
        separacion_x = 85

        max_nodos_nivel = max(len(nodos_nivel) for nodos_nivel in niveles.values())
        ancho_total = max(1400, max_nodos_nivel * separacion_x + 160)

        for d in sorted(niveles.keys()):
            nodos_en_nivel = niveles[d]
            cantidad = len(nodos_en_nivel)
            pos_y = 50 + d * distancia_y
            ancho_nivel = (cantidad - 1) * separacion_x
            inicio_x = (ancho_total - ancho_nivel) / 2.0

            for i, nodo in enumerate(nodos_en_nivel):
                pos_x = inicio_x + i * separacion_x
                posiciones[nodo.id] = (pos_x, pos_y)

        # -----------------------------------------------------------------
        # Dibujar Aristas / Ramas con Colores Vivos de Alto Contraste
        # -----------------------------------------------------------------
        for nodo in nodos_arbol:
            if nodo.padre and nodo.padre.id in posiciones and nodo.id in posiciones:
                px, py = posiciones[nodo.padre.id]
                cx, cy = posiciones[nodo.id]

                if nodo.id in ids_camino_optimo and nodo.padre.id in ids_camino_optimo:
                    linea_color = self.color_camino_optimo # DORADO NEÓN BRRILLANTE
                    ancho_linea = 5
                elif nodo.id in ids_todos_caminos and nodo.padre.id in ids_todos_caminos:
                    linea_color = self.color_camino_alt    # NARANJA NEÓN
                    ancho_linea = 3
                else:
                    linea_color = "#252a3b"                 # Oscuro para ramas secundarias
                    ancho_linea = 1

                self.lienzo_arbol.create_line(px, py, cx, cy, fill=linea_color, width=ancho_linea)

        # -----------------------------------------------------------------
        # Dibujar Nodos con Alto Contraste Visual y Texto Legible
        # -----------------------------------------------------------------
        radio = 22
        for nodo in nodos_arbol:
            if nodo.id not in posiciones:
                continue

            cx, cy = posiciones[nodo.id]
            texto_color = "#ffffff"

            if nodo.estado == self.ambiente.estado_inicial:
                color_relleno = self.color_inicio          # PINK / MAGENTA NEÓN (S_0)
                color_borde = "#ffffff"
                texto_color = "#ffffff"
                ancho_borde = 3
            elif nodo.estado == AmbienteCuadricula.ESTADO_OBJETIVO:
                color_relleno = self.color_meta            # VERDE ESMERALDA NEÓN (S_g Metas)
                color_borde = "#ffffff"
                texto_color = "#000000"
                ancho_borde = 4
            elif nodo.id in ids_camino_optimo:
                color_relleno = self.color_camino_optimo   # DORADO NEÓN (Camino Óptimo)
                color_borde = "#ffffff"
                texto_color = "#000000"
                ancho_borde = 3
            elif nodo.id in ids_todos_caminos:
                color_relleno = self.color_camino_alt      # NARANJA NEÓN (Caminos Alt.)
                color_borde = "#ffffff"
                texto_color = "#ffffff"
                ancho_borde = 2
            else:
                color_relleno = self.color_nodo_normal     # OSCURO CHARCOAL (Explorado)
                color_borde = "#3a405a"
                texto_color = "#b0b8db"
                ancho_borde = 1

            self.lienzo_arbol.create_oval(
                cx - radio, cy - radio, cx + radio, cy + radio,
                fill=color_relleno, outline=color_borde, width=ancho_borde
            )

            texto_id = f"N{nodo.id}"
            texto_estado = f"{nodo.estado[0]},{nodo.estado[1]}"

            self.lienzo_arbol.create_text(cx, cy - 4, text=texto_id, fill=texto_color, font=("Segoe UI", 8, "bold"))
            self.lienzo_arbol.create_text(cx, cy + 7, text=texto_estado, fill=texto_color, font=("Segoe UI", 7, "bold"))

        self.lienzo_arbol.config(scrollregion=self.lienzo_arbol.bbox("all"))

    # -----------------------------------------------------------------
    # Pestaña 3: Jerarquía de Nodos (Tabla)
    # -----------------------------------------------------------------
    def configurar_pestana_arbol_tabla(self):
        contenedor = ttk.Frame(self.pestana_arbol_tabla, padding=10)
        contenedor.pack(fill=tk.BOTH, expand=True)

        ttk.Label(contenedor, text="📋 Tabla Jerárquica de Nodos Generados", style="Header.TLabel").pack(anchor=tk.W, pady=(0, 5))
        ttk.Label(contenedor, text="Muestra cada instancia de la clase Nodo con su Puntero al Padre, Acción, Profundidad d y Costo acumulado g(n).", style="Subtitle.TLabel").pack(anchor=tk.W, pady=(0, 10))

        columnas = ("id", "estado", "padre_id", "accion", "costo", "profundidad")
        self.vista_arbol = ttk.Treeview(contenedor, columns=columnas, show="headings", selectmode="browse")

        self.vista_arbol.heading("id", text="ID Nodo")
        self.vista_arbol.heading("estado", text="Estado (x, y)")
        self.vista_arbol.heading("padre_id", text="ID Padre")
        self.vista_arbol.heading("accion", text="Acción Ejecutada")
        self.vista_arbol.heading("costo", text="Costo g(n)")
        self.vista_arbol.heading("profundidad", text="Profundidad d")

        self.vista_arbol.column("id", width=80, anchor=tk.CENTER)
        self.vista_arbol.column("estado", width=120, anchor=tk.CENTER)
        self.vista_arbol.column("padre_id", width=100, anchor=tk.CENTER)
        self.vista_arbol.column("accion", width=120, anchor=tk.CENTER)
        self.vista_arbol.column("costo", width=100, anchor=tk.CENTER)
        self.vista_arbol.column("profundidad", width=100, anchor=tk.CENTER)

        barra_desplazamiento = ttk.Scrollbar(contenedor, orient=tk.VERTICAL, command=self.vista_arbol.yview)
        self.vista_arbol.configure(yscrollcommand=barra_desplazamiento.set)

        self.vista_arbol.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        barra_desplazamiento.pack(side=tk.RIGHT, fill=tk.Y)

    def poblar_vista_arbol(self, nodos_arbol, nodos_camino=None):
        for item in self.vista_arbol.get_children():
            self.vista_arbol.delete(item)

        if not nodos_arbol:
            return

        for nodo in nodos_arbol:
            padre_id_str = str(nodo.padre.id) if nodo.padre else "None (Raíz)"
            accion_str = nodo.accion if nodo.accion else "S₀ (Inicio)"
            
            self.vista_arbol.insert(
                "",
                tk.END,
                values=(nodo.id, str(nodo.estado), padre_id_str, accion_str, nodo.costo, nodo.profundidad)
            )

    # -----------------------------------------------------------------
    # Pestaña 4: Métricas y Análisis Complejidad
    # -----------------------------------------------------------------
    def configurar_pestana_metricas(self):
        contenedor = ttk.Frame(self.pestana_metricas, padding=10)
        contenedor.pack(fill=tk.BOTH, expand=True)

        ttk.Label(contenedor, text="📊 Análisis Complejidad Computacional Asintótica y Exacta", style="Header.TLabel").pack(anchor=tk.W, pady=(0, 5))
        ttk.Label(contenedor, text="Comparación teórica formal requerida en el deber contra los resultados empíricos obtenidos en la cuadrícula.", style="Subtitle.TLabel").pack(anchor=tk.W, pady=(0, 10))

        columnas = ("estrategia", "formula", "tiempo", "espacio", "nodos_exp", "nodos_gen", "max_mem", "largo_camino", "tiempo_ms")
        self.tabla_metricas = ttk.Treeview(contenedor, columns=columnas, show="headings")

        self.tabla_metricas.heading("estrategia", text="Estrategia de Búsqueda")
        self.tabla_metricas.heading("formula", text="Cálculo Matemático Exacto")
        self.tabla_metricas.heading("tiempo", text="Tiempo O(·)")
        self.tabla_metricas.heading("espacio", text="Espacio O(·)")
        self.tabla_metricas.heading("nodos_exp", text="Nodos Exp.")
        self.tabla_metricas.heading("nodos_gen", text="Nodos Gen.")
        self.tabla_metricas.heading("max_mem", text="Máx. Frontera")
        self.tabla_metricas.heading("largo_camino", text="Camino Óptimo")
        self.tabla_metricas.heading("tiempo_ms", text="Tiempo (ms)")

        self.tabla_metricas.column("estrategia", width=160, anchor=tk.W)
        self.tabla_metricas.column("formula", width=220, anchor=tk.W)
        self.tabla_metricas.column("tiempo", width=90, anchor=tk.CENTER)
        self.tabla_metricas.column("espacio", width=90, anchor=tk.CENTER)
        self.tabla_metricas.column("nodos_exp", width=90, anchor=tk.CENTER)
        self.tabla_metricas.column("nodos_gen", width=90, anchor=tk.CENTER)
        self.tabla_metricas.column("max_mem", width=100, anchor=tk.CENTER)
        self.tabla_metricas.column("largo_camino", width=100, anchor=tk.CENTER)
        self.tabla_metricas.column("tiempo_ms", width=100, anchor=tk.CENTER)

        barra = ttk.Scrollbar(contenedor, orient=tk.VERTICAL, command=self.tabla_metricas.yview)
        self.tabla_metricas.configure(yscrollcommand=barra.set)

        self.tabla_metricas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        barra.pack(side=tk.RIGHT, fill=tk.Y)

        self.cargar_tabla_metricas_defecto()

    def cargar_tabla_metricas_defecto(self):
        for item in self.tabla_metricas.get_children():
            self.tabla_metricas.delete(item)

        datos_teoricos = MetricasBusqueda.obtener_tabla_resumen_teorica()
        for fila in datos_teoricos:
            self.tabla_metricas.insert(
                "",
                tk.END,
                values=(
                    fila["estrategia"],
                    fila["formula_exacta"],
                    fila["tiempo"],
                    fila["espacio"],
                    "-", "-", "-", "-", "-"
                )
            )

    # -----------------------------------------------------------------
    # Lógica de Ejecución y Animación Rápida Adaptativa
    # -----------------------------------------------------------------
    def al_ejecutar_seleccionado(self):
        nombre_algo = self.var_algoritmo.get()
        s0 = self.ambiente.estado_inicial

        if nombre_algo == "Anchura":
            resultado = BusquedaAnchura.resolver(s0)
        elif nombre_algo == "Profundidad":
            resultado = BusquedaProfundidad.resolver(s0)
        elif nombre_algo == "Profundidad Iterativa":
            resultado = ProfundidadIterativa.resolver(s0)
        elif nombre_algo == "Bidireccional":
            resultado = BusquedaBidireccional.resolver(s0)
        else:
            return

        self.resultado_algoritmo_actual = resultado
        self.actualizar_ui_resultado(nombre_algo, resultado)
        self.animar_busqueda(resultado)

    def actualizar_ui_resultado(self, nombre_algo, resultado):
        self.lbl_res_nodos_exp.config(text=f"• Nodos Expandidos: {resultado['nodos_expandidos']}")
        self.lbl_res_nodos_gen.config(text=f"• Nodos Generados: {resultado['nodos_generados']}")
        
        cant_sol = len(resultado.get('nodos_solucion', []))
        self.lbl_res_soluciones_total.config(text=f"• Soluciones Encontradas: {cant_sol}")
        self.lbl_res_frontera.config(text=f"• Máx. Memoria Frontera: {resultado['tamanio_maximo_frontera']}")
        self.lbl_res_tiempo.config(text=f"• Tiempo de Ejecución: {resultado['tiempo_ejecucion_ms']:.2f} ms")
        
        largo_camino = len(resultado['camino']) - 1 if resultado['camino'] else 0
        self.lbl_res_largo_camino.config(text=f"• Camino Óptimo (Costo Min.): {largo_camino}")

        self.poblar_vista_arbol(resultado['nodos_arbol'], resultado['camino'])
        self.dibujar_arbol_grafico(resultado['nodos_arbol'], resultado)

    def animar_busqueda(self, resultado):
        if self.tarea_animacion:
            self.raiz.after_cancel(self.tarea_animacion)

        historial = resultado.get('historial_exploracion', [])
        estados_camino = {paso[0] for paso in resultado['camino']} if resultado['camino'] else set()
        
        retardo_ms = self.deslizador_velocidad.get()
        visitados_acumulados = []

        # Paso adaptativo para no congelar la pantalla cuando hay miles de nodos
        pasos_por_tick = max(1, len(historial) // 50)

        def paso_animacion(idx):
            if idx < len(historial):
                siguiente_idx = min(idx + pasos_por_tick, len(historial))
                for i in range(idx, siguiente_idx):
                    visitados_acumulados.append(historial[i])
                
                self.dibujar_cuadricula(estados_visitados=visitados_acumulados)
                self.tarea_animacion = self.raiz.after(retardo_ms, paso_animacion, siguiente_idx)
            else:
                self.dibujar_cuadricula(estados_visitados=visitados_acumulados, estados_camino=estados_camino)

        paso_animacion(0)

    def al_comparar_todos(self):
        s0 = self.ambiente.estado_inicial

        res_bfs = BusquedaAnchura.resolver(s0)
        res_dfs = BusquedaProfundidad.resolver(s0)
        res_iddfs = ProfundidadIterativa.resolver(s0)
        res_bi = BusquedaBidireccional.resolver(s0)

        for item in self.tabla_metricas.get_children():
            self.tabla_metricas.delete(item)

        datos = [
            ("🏦 Anchura", "b + b² + ... + b^d + (b^(d+1) - b)", "O(b^(d+1))", "O(b^(d+1))", res_bfs),
            ("🥞 Profundidad", "Depende de rama (máx. b^m)", "O(b^m)", "O(b × m)", res_dfs),
            ("🔄 Profundidad Iterativa", "(d)b + (d-1)b² + ... + (1)b^d", "O(b^d)", "O(b × d)", res_iddfs),
            ("↔️ Bidireccional", "2 × b^(d/2)", "O(b^(d/2))", "O(b^(d/2))", res_bi)
        ]

        for titulo, formula, tiempo_o, espacio_o, res in datos:
            largo_camino = len(res['camino']) - 1 if res['camino'] else 0
            self.tabla_metricas.insert(
                "",
                tk.END,
                values=(
                    titulo,
                    formula,
                    tiempo_o,
                    espacio_o,
                    res['nodos_expandidos'],
                    res['nodos_generados'],
                    res['tamanio_maximo_frontera'],
                    f"{largo_camino} (de {len(res.get('nodos_solucion',[]))} encontradas)",
                    f"{res['tiempo_ejecucion_ms']:.2f}"
                )
            )

        self.pestañas.select(self.pestana_metricas)
        messagebox.showinfo("Comparación Completada", f"Se ejecutaron con éxito las 4 estrategias desde S₀ = {s0}.\nRevisa la pestaña de Métricas.")
