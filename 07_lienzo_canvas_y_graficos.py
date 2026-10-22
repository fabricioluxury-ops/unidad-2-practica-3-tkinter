"""
07_lienzo_canvas_y_graficos.py
==============================
Demostración del widget Canvas para gráficos vectoriales, interactividad y animación.

Conceptos cubiertos:
1. Métodos primitivos de dibujo en Canvas:
   - create_line: líneas rectas, flechas y estilos punteados.
   - create_rectangle: rectángulos y cuadrados con bordes y relleno.
   - create_oval: círculos y elipses.
   - create_polygon: formas poligonales complejas (triángulos, estrellas).
   - create_arc: arcos circulares y sectores circulares (gráficas de pastel).
   - create_text: textos vectoriales en coordenadas arbitrarias.
2. Modo Pizarra de Dibujo Libre:
   - Captura de trazos con el ratón en tiempo real.
   - Selección de color y grosor de pincel.
3. Animación en tiempo real (Bucle con root.after):
   - Simulación física de pelota rebotando contra los límites del lienzo.
   - Control de reproducción (Play / Pause / Reiniciar) con canvas.move() y canvas.coords().
4. Arrastre de objetos (Drag & Drop) dentro del Canvas usando identificadores y tags.
"""

import math
import random
import tkinter as tk
from tkinter import ttk, colorchooser


class DemoCanvasGraficos:
    def __init__(self, root):
        self.root = root
        self.root.title("07 - Gráficos, Lienzo (Canvas) y Animaciones")
        self.root.geometry("860x680")
        self.root.minsize(800, 600)

        # Variables de control
        self.color_pincel = "#d81b60"
        self.grosor_pincel = tk.IntVar(value=4)
        self.animacion_activa = False
        self.balon_id = None
        self.vel_x = 4
        self.vel_y = 3

        # Variables de arrastre
        self.item_arrastrado = None
        self.drag_start_x = 0
        self.drag_start_y = 0

        self._crear_interfaz()

    def _crear_interfaz(self):
        # Título
        tk.Label(
            self.root,
            text="Explorador de Gráficos y Animación con Canvas",
            font=("Segoe UI", 13, "bold"),
            bg="#00796b",
            fg="white",
            pady=8
        ).pack(fill="x")

        # Pestañas para cada modalidad
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill="both", expand=True, padx=10, pady=8)

        # Tab 1: Formas y Primitivas
        tab_formas = ttk.Frame(notebook)
        notebook.add(tab_formas, text="1. Figuras Primitivas y Arrastre")
        self._construir_tab_formas(tab_formas)

        # Tab 2: Pizarra de Dibujo Libre
        tab_pizarra = ttk.Frame(notebook)
        notebook.add(tab_pizarra, text="2. Pizarra de Dibujo Libre")
        self._construir_tab_pizarra(tab_pizarra)

        # Tab 3: Animación en Tiempo Real
        tab_animacion = ttk.Frame(notebook)
        notebook.add(tab_animacion, text="3. Animación y Física (after)")
        self._construir_tab_animacion(tab_animacion)

    # -------------------------------------------------------------
    # PESTAÑA 1: FIGURAS PRIMITIVAS
    # -------------------------------------------------------------
    def _construir_tab_formas(self, parent):
        top_info = tk.Label(
            parent,
            text="Muestra de métodos create_*(). ¡Haz clic y arrastra cualquier figura para moverla!",
            font=("Segoe UI", 9, "italic"),
            bg="#e0f2f1",
            fg="#004d40",
            pady=6
        )
        top_info.pack(fill="x", padx=6, pady=4)

        self.canvas_formas = tk.Canvas(parent, bg="#ffffff", relief="sunken", bd=2)
        self.canvas_formas.pack(fill="both", expand=True, padx=8, pady=6)

        # Dibujar primitivas con tag 'movible' para arrastre
        # 1. Líneas y flechas
        self.canvas_formas.create_line(30, 40, 160, 40, width=3, fill="#3949ab", arrow=tk.LAST, tags="movible")
        self.canvas_formas.create_text(95, 25, text="create_line (flecha)", font=("Segoe UI", 8), tags="movible")

        # 2. Rectángulo
        self.canvas_formas.create_rectangle(30, 80, 160, 170, fill="#ffb74d", outline="#e65100", width=2, tags="movible")
        self.canvas_formas.create_text(95, 125, text="create_rectangle", font=("Segoe UI", 8, "bold"), tags="movible")

        # 3. Óvalo / Círculo
        self.canvas_formas.create_oval(200, 70, 310, 180, fill="#4db6ac", outline="#004d40", width=2, tags="movible")
        self.canvas_formas.create_text(255, 125, text="create_oval\n(Círculo)", font=("Segoe UI", 8, "bold"), justify="center", tags="movible")

        # 4. Polígono (Estrella de 5 puntas)
        puntos_estrella = self._calcular_puntos_estrella(420, 125, 5, 55, 25)
        self.canvas_formas.create_polygon(puntos_estrella, fill="#ba68c8", outline="#4a148c", width=2, tags="movible")
        self.canvas_formas.create_text(420, 195, text="create_polygon", font=("Segoe UI", 8, "bold"), tags="movible")

        # 5. Arcos circulares (Sector de tarta)
        self.canvas_formas.create_arc(530, 60, 660, 190, start=30, extent=120, fill="#f06292", outline="#880e4f", width=2, tags="movible")
        self.canvas_formas.create_arc(530, 60, 660, 190, start=160, extent=200, fill="#64b5f6", outline="#0d47a1", width=2, tags="movible")
        self.canvas_formas.create_text(595, 205, text="create_arc (Gráfico Pastel)", font=("Segoe UI", 8, "bold"), tags="movible")

        # Vinculación de eventos para arrastrar objetos
        self.canvas_formas.tag_bind("movible", "<Button-1>", self._iniciar_arrastre)
        self.canvas_formas.tag_bind("movible", "<B1-Motion>", self._mover_arrastre)

    def _calcular_puntos_estrella(self, cx, cy, puntas, r_ext, r_int):
        """Genera las coordenadas (x, y) de una estrella regular."""
        pts = []
        paso = math.pi / puntas
        for i in range(2 * puntas):
            r = r_ext if i % 2 == 0 else r_int
            angulo = i * paso - math.pi / 2
            pts.append(cx + r * math.cos(angulo))
            pts.append(cy + r * math.sin(angulo))
        return pts

    def _iniciar_arrastre(self, event):
        """Identifica el objeto sobre el que se hizo clic."""
        self.item_arrastrado = self.canvas_formas.find_closest(event.x, event.y)[0]
        self.drag_start_x = event.x
        self.drag_start_y = event.y

    def _mover_arrastre(self, event):
        """Desplaza el objeto seleccionado según el desplazamiento del ratón."""
        if self.item_arrastrado:
            dx = event.x - self.drag_start_x
            dy = event.y - self.drag_start_y
            self.canvas_formas.move(self.item_arrastrado, dx, dy)
            self.drag_start_x = event.x
            self.drag_start_y = event.y

    # -------------------------------------------------------------
    # PESTAÑA 2: PIZARRA DE DIBUJO LIBRE
    # -------------------------------------------------------------
    def _construir_tab_pizarra(self, parent):
        toolbar = tk.Frame(parent, bg="#eeeeee", pady=6, padx=8)
        toolbar.pack(fill="x")

        # Botón para color
        self.btn_color = tk.Button(
            toolbar,
            text=" Color Pincel ",
            bg=self.color_pincel,
            fg="white",
            font=("Segoe UI", 9, "bold"),
            command=self._elegir_color_pincel
        )
        self.btn_color.pack(side="left", padx=4)

        # Control de grosor
        tk.Label(toolbar, text="Grosor:", bg="#eeeeee", font=("Segoe UI", 9)).pack(side="left", padx=(10, 4))
        tk.Spinbox(toolbar, from_=1, to=30, textvariable=self.grosor_pincel, width=5).pack(side="left")

        # Limpiar pizarra
        tk.Button(toolbar, text="Limpiar Pizarra", command=self._limpiar_pizarra).pack(side="right", padx=4)

        self.canvas_pizarra = tk.Canvas(parent, bg="#ffffff", cursor="pencil")
        self.canvas_pizarra.pack(fill="both", expand=True, padx=8, pady=6)

        # Trazo libre mediante seguimiento de líneas consecutivas
        self.ultimo_x = None
        self.ultimo_y = None
        self.canvas_pizarra.bind("<Button-1>", self._iniciar_trazo)
        self.canvas_pizarra.bind("<B1-Motion>", self._dibujar_trazo)
        self.canvas_pizarra.bind("<ButtonRelease-1>", self._soltar_trazo)

    def _elegir_color_pincel(self):
        c = colorchooser.askcolor(color=self.color_pincel, title="Elegir Color de Trazo")
        if c[1]:
            self.color_pincel = c[1]
            self.btn_color.config(bg=self.color_pincel)

    def _iniciar_trazo(self, event):
        self.ultimo_x = event.x
        self.ultimo_y = event.y

    def _dibujar_trazo(self, event):
        if self.ultimo_x is not None and self.ultimo_y is not None:
            self.canvas_pizarra.create_line(
                self.ultimo_x, self.ultimo_y, event.x, event.y,
                width=self.grosor_pincel.get(),
                fill=self.color_pincel,
                capstyle=tk.ROUND,
                smooth=True
            )
            self.ultimo_x = event.x
            self.ultimo_y = event.y

    def _soltar_trazo(self, event):
        self.ultimo_x = None
        self.ultimo_y = None

    def _limpiar_pizarra(self):
        self.canvas_pizarra.delete("all")

    # -------------------------------------------------------------
    # PESTAÑA 3: ANIMACIÓN EN TIEMPO REAL
    # -------------------------------------------------------------
    def _construir_tab_animacion(self, parent):
        ctrl_bar = tk.Frame(parent, bg="#f5f5f5", pady=6, padx=8)
        ctrl_bar.pack(fill="x")

        self.btn_toggle_anim = tk.Button(
            ctrl_bar,
            text=" Iniciar Animación ",
            bg="#2e7d32",
            fg="white",
            font=("Segoe UI", 9, "bold"),
            command=self._toggle_animacion
        )
        self.btn_toggle_anim.pack(side="left", padx=4)

        tk.Button(ctrl_bar, text="Reiniciar Posición", command=self._reiniciar_pelota).pack(side="left", padx=4)

        self.lbl_info_anim = tk.Label(
            ctrl_bar,
            text="Estado: En pausa",
            font=("Segoe UI", 9),
            bg="#f5f5f5"
        )
        self.lbl_info_anim.pack(side="left", padx=15)

        self.canvas_anim = tk.Canvas(parent, bg="#1a1a2e")
        self.canvas_anim.pack(fill="both", expand=True, padx=8, pady=6)

        # Crear pelota
        self._reiniciar_pelota()

    def _reiniciar_pelota(self):
        if self.balon_id:
            self.canvas_anim.delete(self.balon_id)
        # Dibujar pelota en posición inicial
        radio = 18
        x0, y0 = 100, 100
        self.balon_id = self.canvas_anim.create_oval(
            x0 - radio, y0 - radio, x0 + radio, y0 + radio,
            fill="#e94560", outline="#ffffff", width=2
        )
        self.vel_x = 5
        self.vel_y = 4

    def _toggle_animacion(self):
        self.animacion_activa = not self.animacion_activa
        if self.animacion_activa:
            self.btn_toggle_anim.config(text=" Pausar Animación ", bg="#c62828")
            self.lbl_info_anim.config(text="Estado: Reproduciendo (Bucle .after())")
            self._paso_animacion()
        else:
            self.btn_toggle_anim.config(text=" Reanudar Animación ", bg="#2e7d32")
            self.lbl_info_anim.config(text="Estado: En pausa")

    def _paso_animacion(self):
        """Bucle de refresco que calcula la física y mueve la pelota."""
        if not self.animacion_activa:
            return

        coords = self.canvas_anim.coords(self.balon_id)
        if not coords:
            return

        x1, y1, x2, y2 = coords
        ancho_lienzo = self.canvas_anim.winfo_width()
        alto_lienzo = self.canvas_anim.winfo_height()

        # Rebotar contra paredes laterales
        if x2 + self.vel_x >= ancho_lienzo or x1 + self.vel_x <= 0:
            self.vel_x = -self.vel_x

        # Rebotar contra techo y suelo
        if y2 + self.vel_y >= alto_lienzo or y1 + self.vel_y <= 0:
            self.vel_y = -self.vel_y

        self.canvas_anim.move(self.balon_id, self.vel_x, self.vel_y)

        # Programar siguiente fotograma en 16ms (~60 FPS)
        self.root.after(16, self._paso_animacion)


def main():
    root = tk.Tk()
    app = DemoCanvasGraficos(root)
    root.mainloop()


if __name__ == "__main__":
    main()
