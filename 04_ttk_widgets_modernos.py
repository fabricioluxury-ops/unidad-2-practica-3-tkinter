"""
04_ttk_widgets_modernos.py
==========================
Demostración de los widgets temáticos modernos con tkinter.ttk y ttk.Style.

Conceptos cubiertos:
1. ttk.Style:
   - Inspección y cambio de temas disponibles (clam, alt, default, classic, etc.).
   - Personalización estética de componentes ttk (colores, fuentes, bordes).
2. ttk.Combobox:
   - Menús desplegables con valores predeterminados y captura de selección con <<ComboboxSelected>>.
3. ttk.Progressbar:
   - Modos 'determinate' (barra cuantificable con porcentaje) e 'indeterminate' (animación infinita).
4. ttk.Treeview:
   - Tablas avanzadas con múltiples columnas, encabezados, alineaciones y scrollbars.
   - Inserción dinámica de datos, selección de filas y eliminación.
5. ttk.Separator:
   - Divisores visuales limpios y adaptables.
"""

import tkinter as tk
from tkinter import ttk, messagebox


class DemoTtkModerno:
    def __init__(self, root):
        self.root = root
        self.root.title("04 - Widgets Temáticos Modernos (tkinter.ttk)")
        self.root.geometry("820x680")
        self.root.minsize(750, 600)

        # Inicialización del gestor de estilos
        self.style = ttk.Style()
        self.temas_disponibles = self.style.theme_names()

        self._crear_interfaz()

    def _crear_interfaz(self):
        # ---------------------------------------------------------
        # Encabezado con selector de Tema TTK
        # ---------------------------------------------------------
        top_bar = tk.Frame(self.root, bg="#263238", pady=10, padx=15)
        top_bar.pack(fill="x")

        tk.Label(
            top_bar,
            text="Explorador de Widgets ttk",
            font=("Segoe UI", 13, "bold"),
            bg="#263238",
            fg="white"
        ).pack(side="left")

        tk.Label(
            top_bar,
            text="Tema actual:",
            font=("Segoe UI", 9),
            bg="#263238",
            fg="#cfd8dc"
        ).pack(side="left", padx=(30, 8))

        self.combo_tema = ttk.Combobox(
            top_bar,
            values=list(self.temas_disponibles),
            state="readonly",
            width=14
        )
        self.combo_tema.set(self.style.theme_use())
        self.combo_tema.pack(side="left")
        self.combo_tema.bind("<<ComboboxSelected>>", self._cambiar_tema)

        # Contenedor central
        container = ttk.Frame(self.root, padding=12)
        container.pack(fill="both", expand=True)

        # ---------------------------------------------------------
        # Sección 1: Combobox y Controles Simples
        # ---------------------------------------------------------
        f_superior = ttk.LabelFrame(container, text=" 1. ttk.Combobox y Selección ", padding=10)
        f_superior.pack(fill="x", pady=6)

        f_sup_grid = ttk.Frame(f_superior)
        f_sup_grid.pack(fill="x")

        ttk.Label(f_sup_grid, text="Lenguaje preferido:").grid(row=0, column=0, sticky="w", padx=5, pady=4)
        self.combo_lang = ttk.Combobox(
            f_sup_grid,
            values=["Python", "JavaScript", "C++", "Rust", "Go", "Kotlin"],
            state="readonly",
            width=18
        )
        self.combo_lang.current(0)
        self.combo_lang.grid(row=0, column=1, sticky="w", padx=5, pady=4)
        self.combo_lang.bind("<<ComboboxSelected>>", self._on_lang_selected)

        self.lbl_lang_info = ttk.Label(f_sup_grid, text="Seleccionado: Python", font=("Segoe UI", 9, "italic"))
        self.lbl_lang_info.grid(row=0, column=2, sticky="w", padx=15, pady=4)

        # ---------------------------------------------------------
        # Sección 2: Barras de Progreso (Determinate & Indeterminate)
        # ---------------------------------------------------------
        f_progress = ttk.LabelFrame(container, text=" 2. ttk.Progressbar (Progreso Determinado e Indeterminado) ", padding=10)
        f_progress.pack(fill="x", pady=6)

        # Barra Determinada
        p1_frame = ttk.Frame(f_progress)
        p1_frame.pack(fill="x", pady=4)

        ttk.Label(p1_frame, text="Progreso Determinado (0% - 100%):", width=32).pack(side="left")
        self.prog_determinado = ttk.Progressbar(p1_frame, orient="horizontal", mode="determinate", length=220)
        self.prog_determinado.pack(side="left", padx=8)

        self.lbl_pct = ttk.Label(p1_frame, text="0%", width=6)
        self.lbl_pct.pack(side="left")

        ttk.Button(p1_frame, text="+10%", width=6, command=lambda: self._avanzar_progreso(10)).pack(side="left", padx=3)
        ttk.Button(p1_frame, text="Reset", width=6, command=self._reset_progreso).pack(side="left", padx=3)

        # Barra Indeterminada (Carga sin fin)
        p2_frame = ttk.Frame(f_progress)
        p2_frame.pack(fill="x", pady=4)

        ttk.Label(p2_frame, text="Progreso Indeterminado (Spinner / Busy):", width=32).pack(side="left")
        self.prog_indeterminado = ttk.Progressbar(p2_frame, orient="horizontal", mode="indeterminate", length=220)
        self.prog_indeterminado.pack(side="left", padx=8)

        ttk.Button(p2_frame, text="Iniciar", width=8, command=self.prog_indeterminado.start).pack(side="left", padx=3)
        ttk.Button(p2_frame, text="Detener", width=8, command=self.prog_indeterminado.stop).pack(side="left", padx=3)

        # ---------------------------------------------------------
        # Sección 3: ttk.Treeview (Tabla de Datos Completa)
        # ---------------------------------------------------------
        f_tree = ttk.LabelFrame(container, text=" 3. ttk.Treeview (Tabla de Datos con Scrollbar) ", padding=10)
        f_tree.pack(fill="both", expand=True, pady=6)

        # Frame para tabla y scrollbars
        tree_container = ttk.Frame(f_tree)
        tree_container.pack(fill="both", expand=True)

        columnas = ("id", "producto", "categoria", "precio", "stock")
        self.tree = ttk.Treeview(tree_container, columns=columnas, show="headings", height=8)

        # Configurar encabezados y anchos
        self.tree.heading("id", text="ID")
        self.tree.heading("producto", text="Producto")
        self.tree.heading("categoria", text="Categoría")
        self.tree.heading("precio", text="Precio ($)")
        self.tree.heading("stock", text="Stock")

        self.tree.column("id", width=50, anchor="center")
        self.tree.column("producto", width=180, anchor="w")
        self.tree.column("categoria", width=130, anchor="w")
        self.tree.column("precio", width=90, anchor="e")
        self.tree.column("stock", width=70, anchor="center")

        # Scrollbar vertical
        tree_scroll = ttk.Scrollbar(tree_container, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=tree_scroll.set)

        self.tree.pack(side="left", fill="both", expand=True)
        tree_scroll.pack(side="right", fill="y")

        # Botones de acción para la tabla
        btn_bar = ttk.Frame(f_tree)
        btn_bar.pack(fill="x", pady=(8, 0))

        ttk.Button(btn_bar, text="Agregar Elemento Demo", command=self._agregar_item_demo).pack(side="left", padx=4)
        ttk.Button(btn_bar, text="Eliminar Seleccionado", command=self._eliminar_seleccionado).pack(side="left", padx=4)
        ttk.Button(btn_bar, text="Vaciar Tabla", command=self._vaciar_tabla).pack(side="left", padx=4)

        # Cargar datos iniciales en la tabla
        self._cargar_datos_iniciales()

    def _cambiar_tema(self, event=None):
        """Aplica el tema seleccionado en el combobox."""
        nuevo_tema = self.combo_tema.get()
        try:
            self.style.theme_use(nuevo_tema)
        except Exception as e:
            messagebox.showerror("Error de Tema", f"No se pudo aplicar el tema {nuevo_tema}: {e}")

    def _on_lang_selected(self, event=None):
        """Actualiza la etiqueta cuando cambia el combobox de lenguajes."""
        sel = self.combo_lang.get()
        self.lbl_lang_info.config(text=f"Seleccionado: {sel}")

    def _avanzar_progreso(self, incremento):
        """Incrementa el valor de la barra determinada."""
        valor_actual = self.prog_determinado["value"]
        nuevo_valor = min(100, valor_actual + incremento)
        self.prog_determinado["value"] = nuevo_valor
        self.lbl_pct.config(text=f"{int(nuevo_valor)}%")

    def _reset_progreso(self):
        """Reinicia la barra de progreso a 0%."""
        self.prog_determinado["value"] = 0
        self.lbl_pct.config(text="0%")

    def _cargar_datos_iniciales(self):
        """Puebla la tabla con datos de ejemplo."""
        datos = [
            (101, "Teclado Mecánico RGB", "Periféricos", "59.99", 24),
            (102, "Monitor IPS 27'' 144Hz", "Pantallas", "249.50", 12),
            (103, "Ratón Ergonómico Óptico", "Periféricos", "34.00", 45),
            (104, "Auriculares Inalámbricos", "Audio", "89.90", 18),
            (105, "Disco SSD NVMe 1TB", "Almacenamiento", "75.20", 30),
        ]
        for row in datos:
            self.tree.insert("", "end", values=row)

    def _agregar_item_demo(self):
        """Inserta una nueva fila de prueba en el Treeview."""
        nuevo_id = len(self.tree.get_children()) + 101
        self.tree.insert("", "end", values=(nuevo_id, f"Producto Nuevo #{nuevo_id}", "Varios", "19.99", 10))

    def _eliminar_seleccionado(self):
        """Elimina el elemento seleccionado en la tabla."""
        seleccion = self.tree.selection()
        if not seleccion:
            messagebox.showwarning("Atención", "Por favor, selecciona una fila de la tabla para eliminar.")
            return
        for item in seleccion:
            self.tree.delete(item)

    def _vaciar_tabla(self):
        """Limpia todos los elementos de la tabla."""
        for item in self.tree.get_children():
            self.tree.delete(item)


def main():
    root = tk.Tk()
    app = DemoTtkModerno(root)
    root.mainloop()


if __name__ == "__main__":
    main()
