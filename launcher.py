"""
launcher.py
===========
Panel de control y lanzador gráfico central del repositorio de Tkinter.

Permite:
1. Visualizar el catálogo completo de ejemplos incluidos en el repositorio.
2. Ejecutar cualquier script de demostración de forma independiente con un solo clic.
3. Filtrar y buscar módulos por nombre de widget o palabra clave.
4. Consultar un resumen descriptivo rápido de cada módulo antes de ejecutarlo.
"""

import os
import subprocess
import sys
import tkinter as tk
from tkinter import ttk, messagebox


MODULOS = [
    {
        "archivo": "01_hola_mundo_basico.py",
        "numero": "01",
        "titulo": "Hola Mundo y Fundamentos Básicos",
        "color": "#1e88e5",
        "descripcion": "Ventana raíz tk.Tk, configuración geométrica, widgets Label, Entry y Button, empaquetado con pack() y bucle mainloop().",
        "tags": ["tk.Tk", "geometry", "Label", "Entry", "Button", "pack", "mainloop"]
    },
    {
        "archivo": "02_layout_managers.py",
        "numero": "02",
        "titulo": "Administradores de Geometría (pack, grid, place)",
        "color": "#43a047",
        "descripcion": "Comparativa práctica entre pack (apilamiento direccional), grid (matrices con filas/columnas responsivas) y place (posiciones absolutas y relativas).",
        "tags": ["pack", "grid", "place", "rowconfigure", "columnspan", "sticky", "relx/rely"]
    },
    {
        "archivo": "03_widgets_interactivos.py",
        "numero": "03",
        "titulo": "Widgets Interactivos y Variables de Control",
        "color": "#3949ab",
        "descripcion": "Variables reactivas (StringVar, IntVar, BooleanVar, DoubleVar), Entry con clave oculta, Checkbutton, Radiobutton, Spinbox, Scale y Text con Scrollbar.",
        "tags": ["StringVar", "Checkbutton", "Radiobutton", "Spinbox", "Scale", "Text", "Scrollbar"]
    },
    {
        "archivo": "04_ttk_widgets_modernos.py",
        "numero": "04",
        "titulo": "Widgets Temáticos Modernos (tkinter.ttk)",
        "color": "#8e24aa",
        "descripcion": "ttk.Style y selector de temas del sistema, ttk.Combobox desplegable, ttk.Progressbar (modo determinado e indeterminado) y ttk.Treeview tabular con scroll.",
        "tags": ["ttk.Style", "Combobox", "Progressbar", "Treeview", "Temas", "Separator"]
    },
    {
        "archivo": "05_eventos_y_bindings.py",
        "numero": "05",
        "titulo": "Sistema de Eventos y Vinculaciones (Bindings)",
        "color": "#d81b60",
        "descripcion": "Manejo de clics, doble clic, coordenadas en tiempo real (<Motion>), arrastre (<B1-Motion>), atajos de teclado globales y consola de eventos integrada.",
        "tags": ["bind", "Event Object", "Motion", "KeyPress", "Atajos Ctrl+S", "Consola"]
    },
    {
        "archivo": "06_menus_y_dialogos.py",
        "numero": "06",
        "titulo": "Menús y Cuadros de Diálogo Estándar",
        "color": "#00897b",
        "descripcion": "Barra de menús desplegables con aceleradores, submenús y casillas, menú contextual con clic derecho, messagebox, filedialog, colorchooser y simpledialog.",
        "tags": ["Menu", "Context Menu", "messagebox", "filedialog", "colorchooser", "simpledialog"]
    },
    {
        "archivo": "07_lienzo_canvas_y_graficos.py",
        "numero": "07",
        "titulo": "Lienzo (Canvas), Gráficos y Animación",
        "color": "#fb8c00",
        "descripcion": "Dibujo vectorial (líneas, flechas, rectángulos, círculos, estrellas, sectores de tarta), pizarra de dibujo libre y animación en tiempo real con bucle after().",
        "tags": ["Canvas", "create_oval", "create_polygon", "Pizarra", "Animación 60FPS", "after()"]
    },
    {
        "archivo": "08_arquitectura_poo_app.py",
        "numero": "08",
        "titulo": "Arquitectura POO y Navegación Multivista",
        "color": "#37474f",
        "descripcion": "Aplicación empresarial escalable basada en POO. Menú lateral (Sidebar), intercambio dinámico de vistas con tkraise, CRUD de tareas, barra de estado y reloj vivo.",
        "tags": ["POO", "tk.Tk Heritage", "Sidebar", "Navegación SPA", "Data Store", "Status Bar"]
    }
]


class LanzadorTkinter:
    def __init__(self, root):
        self.root = root
        self.root.title("Lanzador Central - Ejemplos de Tkinter en Python")
        self.root.geometry("880x720")
        self.root.minsize(780, 600)
        self.root.configure(bg="#0f172a")

        self.filtro_busqueda = tk.StringVar()
        self.filtro_busqueda.trace_add("write", lambda *args: self._filtrar_tarjetas())

        self.procesos_activos = []

        self._crear_interfaz()
        self._renderizar_tarjetas(MODULOS)

    def _crear_interfaz(self):
        # ------------------ ENCABEZADO SUPERIOR ------------------
        header = tk.Frame(self.root, bg="#1e293b", pady=18, padx=20)
        header.pack(fill="x")

        tk.Label(
            header,
            text="Python Tkinter Showcase",
            font=("Segoe UI", 18, "bold"),
            bg="#1e293b",
            fg="#38bdf8"
        ).pack(anchor="w")

        tk.Label(
            header,
            text="Colección completa de ejemplos prácticos y funcionalidades de la librería GUI estándar de Python.",
            font=("Segoe UI", 10),
            bg="#1e293b",
            fg="#94a3b8"
        ).pack(anchor="w", pady=(2, 10))

        # Barra de búsqueda integrada en encabezado
        f_search = tk.Frame(header, bg="#1e293b")
        f_search.pack(fill="x")

        tk.Label(
            f_search,
            text="Buscar módulo o widget:",
            font=("Segoe UI", 9, "bold"),
            bg="#1e293b",
            fg="#e2e8f0"
        ).pack(side="left", padx=(0, 8))

        entry_buscar = tk.Entry(
            f_search,
            textvariable=self.filtro_busqueda,
            font=("Segoe UI", 10),
            width=35,
            relief="flat",
            bg="#0f172a",
            fg="#f8fafc",
            insertbackground="white"
        )
        entry_buscar.pack(side="left", padx=4, ipady=4)

        btn_limpiar = tk.Button(
            f_search,
            text="Limpiar",
            font=("Segoe UI", 8),
            bg="#334155",
            fg="white",
            bd=0,
            padx=10,
            command=lambda: self.filtro_busqueda.set("")
        )
        btn_limpiar.pack(side="left", padx=6)

        # ------------------ ÁREA CON SCROLL PARA TARJETAS ------------------
        container = tk.Frame(self.root, bg="#0f172a")
        container.pack(fill="both", expand=True, padx=16, pady=12)

        self.canvas = tk.Canvas(container, bg="#0f172a", highlightthickness=0)
        scrollbar = ttk.Scrollbar(container, orient="vertical", command=self.canvas.yview)

        self.frame_tarjetas = tk.Frame(self.canvas, bg="#0f172a")
        self.frame_tarjetas.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.window_id = self.canvas.create_window((0, 0), window=self.frame_tarjetas, anchor="nw")
        self.canvas.configure(yscrollcommand=scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Ajustar ancho del frame de tarjetas al redimensionar canvas
        self.canvas.bind(
            "<Configure>",
            lambda e: self.canvas.itemconfig(self.window_id, width=e.width)
        )

        # Habilitar scroll con rueda del ratón
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)

        # ------------------ PIE DE PÁGINA INFORMATIVO ------------------
        footer = tk.Frame(self.root, bg="#1e293b", pady=8, padx=16)
        footer.pack(fill="x", side="bottom")

        tk.Label(
            footer,
            text="Tip: Puedes ejecutar varios módulos en paralelo. Cada uno corre en su propio proceso independiente.",
            font=("Segoe UI", 8, "italic"),
            bg="#1e293b",
            fg="#94a3b8"
        ).pack(side="left")

        btn_cerrar = tk.Button(
            footer,
            text="Cerrar Todo",
            font=("Segoe UI", 8),
            bg="#dc2626",
            fg="white",
            bd=0,
            padx=12,
            pady=3,
            cursor="hand2",
            command=self._cerrar_todo
        )
        btn_cerrar.pack(side="right")

    def _on_mousewheel(self, event):
        """Maneja el desplazamiento vertical con la rueda del ratón en Windows/Linux."""
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def _renderizar_tarjetas(self, lista_modulos):
        """Genera visualmente las tarjetas para cada módulo proporcionado."""
        for widget in self.frame_tarjetas.winfo_children():
            widget.destroy()

        if not lista_modulos:
            lbl_vacio = tk.Label(
                self.frame_tarjetas,
                text="No se encontraron módulos con el criterio de búsqueda especificado.",
                font=("Segoe UI", 11, "italic"),
                bg="#0f172a",
                fg="#64748b",
                pady=40
            )
            lbl_vacio.pack(fill="x")
            return

        for mod in lista_modulos:
            card = tk.Frame(self.frame_tarjetas, bg="#1e293b", relief="flat", bd=0, padx=16, pady=12)
            card.pack(fill="x", pady=6, padx=4)

            # Fila Superior: Badge Número + Título + Botón de Ejecutar
            f_titulo = tk.Frame(card, bg="#1e293b")
            f_titulo.pack(fill="x")

            # Badge con número
            lbl_badge = tk.Label(
                f_titulo,
                text=f" {mod['numero']} ",
                font=("Segoe UI", 10, "bold"),
                bg=mod["color"],
                fg="white",
                padx=6,
                pady=2
            )
            lbl_badge.pack(side="left", padx=(0, 10))

            # Título y nombre de archivo
            lbl_nom = tk.Label(
                f_titulo,
                text=f"{mod['titulo']}  ({mod['archivo']})",
                font=("Segoe UI", 11, "bold"),
                bg="#1e293b",
                fg="#f8fafc"
            )
            lbl_nom.pack(side="left", anchor="w")

            # Botón de Ejecutar
            btn_run = tk.Button(
                f_titulo,
                text="▶  Ejecutar Módulo",
                font=("Segoe UI", 9, "bold"),
                bg=mod["color"],
                fg="white",
                activebackground="#0284c7",
                activeforeground="white",
                bd=0,
                padx=14,
                pady=5,
                cursor="hand2",
                command=lambda archivo=mod["archivo"]: self._ejecutar_script(archivo)
            )
            btn_run.pack(side="right")

            # Descripción
            lbl_desc = tk.Label(
                card,
                text=mod["descripcion"],
                font=("Segoe UI", 9),
                bg="#1e293b",
                fg="#cbd5e1",
                wraplength=760,
                justify="left"
            )
            lbl_desc.pack(anchor="w", pady=(6, 8))

            # Etiquetas (Tags)
            f_tags = tk.Frame(card, bg="#1e293b")
            f_tags.pack(fill="x")

            for tag in mod["tags"]:
                tk.Label(
                    f_tags,
                    text=f"#{tag}",
                    font=("Segoe UI", 8),
                    bg="#334155",
                    fg="#93c5fd",
                    padx=6,
                    pady=1
                ).pack(side="left", padx=(0, 6))

    def _filtrar_tarjetas(self):
        """Filtra la lista de módulos en función del término ingresado."""
        query = self.filtro_busqueda.get().strip().lower()
        if not query:
            self._renderizar_tarjetas(MODULOS)
            return

        filtrados = []
        for mod in MODULOS:
            cadena_busqueda = (
                mod["titulo"].lower() + " " +
                mod["archivo"].lower() + " " +
                mod["descripcion"].lower() + " " +
                " ".join(mod["tags"]).lower()
            )
            if query in cadena_busqueda:
                filtrados.append(mod)

        self._renderizar_tarjetas(filtrados)

    def _ejecutar_script(self, nombre_archivo):
        """Lanza el script seleccionado como un subproceso independiente."""
        directorio_actual = os.path.dirname(os.path.abspath(__file__))
        ruta_script = os.path.join(directorio_actual, nombre_archivo)

        if not os.path.exists(ruta_script):
            messagebox.showerror("Archivo No Encontrado", f"No se encontró el script:\n{ruta_script}")
            return

        try:
            proceso = subprocess.Popen([sys.executable, ruta_script], cwd=directorio_actual)
            self.procesos_activos.append(proceso)
        except Exception as e:
            messagebox.showerror("Error al Ejecutar", f"No se pudo iniciar el proceso:\n{e}")

    def _cerrar_todo(self):
        """Termina todos los subprocesos abiertos y cierra el lanzador."""
        for p in self.procesos_activos:
            try:
                p.terminate()
            except Exception:
                pass
        self.root.destroy()


def main():
    root = tk.Tk()
    app = LanzadorTkinter(root)
    root.mainloop()


if __name__ == "__main__":
    main()
