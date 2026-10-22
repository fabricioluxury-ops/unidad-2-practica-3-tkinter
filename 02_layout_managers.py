"""
02_layout_managers.py
=====================
Demostración exhaustiva de los tres administradores de geometría en Tkinter:
pack(), grid() y place().

Regla de oro de Tkinter:
Nunca mezclar pack() y grid() dentro del MISMO contenedor (Frame o Tk).
Para combinarlos, se deben utilizar Frames independientes.

Contenido:
- Pestaña 1 (pack): Apilamiento direccional (side, fill, expand, padx, pady).
- Pestaña 2 (grid): Estructura matricial basada en filas y columnas (row, column, columnspan, sticky, weight).
- Pestaña 3 (place): Posicionamiento exacto por coordenadas absolutas (x, y) y relativas (relx, rely, anchor).
"""

import tkinter as tk
from tkinter import ttk


def crear_tab_pack(notebook):
    """Crea la pestaña demostrativa de pack()."""
    tab = ttk.Frame(notebook)
    notebook.add(tab, text="1. Gestor pack()")

    # Explicación
    lbl_info = tk.Label(
        tab,
        text=(
            "pack() organiza los widgets apilándolos contra los bordes de la ventana.\n"
            "Parámetros clave: side (TOP, BOTTOM, LEFT, RIGHT), fill (X, Y, BOTH, NONE), "
            "expand (True/False)."
        ),
        font=("Segoe UI", 9),
        bg="#e8f0fe",
        fg="#1a73e8",
        relief="groove",
        padx=10,
        pady=8,
        justify="left"
    )
    lbl_info.pack(fill="x", padx=10, pady=8)

    # Contenedor para demostración visual de pack
    demo_frame = tk.LabelFrame(
        tab,
        text=" Demostración Visual de pack() ",
        font=("Segoe UI", 10, "bold"),
        padx=10,
        pady=10
    )
    demo_frame.pack(fill="both", expand=True, padx=10, pady=5)

    # Widgets empaquetados en distintas direcciones
    b1 = tk.Label(demo_frame, text="side='top', fill='x'", bg="#ef5350", fg="white", font=("Segoe UI", 9, "bold"))
    b1.pack(side="top", fill="x", pady=2)

    b2 = tk.Label(demo_frame, text="side='bottom', fill='x'", bg="#ab47bc", fg="white", font=("Segoe UI", 9, "bold"))
    b2.pack(side="bottom", fill="x", pady=2)

    b3 = tk.Label(demo_frame, text="side='left'\nfill='y'", bg="#26a69a", fg="white", font=("Segoe UI", 9, "bold"), width=12)
    b3.pack(side="left", fill="y", padx=2)

    b4 = tk.Label(demo_frame, text="side='right'\nfill='y'", bg="#ffa726", fg="white", font=("Segoe UI", 9, "bold"), width=12)
    b4.pack(side="right", fill="y", padx=2)

    b5 = tk.Label(
        demo_frame,
        text="Centro:\nfill='both', expand=True\n(Aprovecha el espacio sobrante)",
        bg="#42a5f5",
        fg="white",
        font=("Segoe UI", 9, "bold")
    )
    b5.pack(fill="both", expand=True, padx=5, pady=5)

    return tab


def crear_tab_grid(notebook):
    """Crea la pestaña demostrativa de grid()."""
    tab = ttk.Frame(notebook)
    notebook.add(tab, text="2. Gestor grid()")

    # Explicación
    lbl_info = tk.Label(
        tab,
        text=(
            "grid() organiza los widgets en una tabla bidimensional de filas y columnas.\n"
            "Parámetros clave: row, column, columnspan, rowspan, sticky ('nsew', 'w', etc.).\n"
            "Permite diseño responsivo mediante grid_columnconfigure y grid_rowconfigure."
        ),
        font=("Segoe UI", 9),
        bg="#e8f5e9",
        fg="#2e7d32",
        relief="groove",
        padx=10,
        pady=8,
        justify="left"
    )
    lbl_info.pack(fill="x", padx=10, pady=8)

    # Formulario típico usando grid
    form_frame = tk.LabelFrame(
        tab,
        text=" Ejemplo Práctico: Formulario de Registro con grid() ",
        font=("Segoe UI", 10, "bold"),
        padx=15,
        pady=15
    )
    form_frame.pack(fill="both", expand=True, padx=10, pady=5)

    # Configurar pesos de columnas para responsividad
    form_frame.grid_columnconfigure(1, weight=1)

    # Fila 0: Nombre
    tk.Label(form_frame, text="Nombre:", font=("Segoe UI", 9)).grid(row=0, column=0, sticky="w", pady=4)
    e_nombre = tk.Entry(form_frame, font=("Segoe UI", 9))
    e_nombre.grid(row=0, column=1, sticky="ew", padx=8, pady=4)

    # Fila 1: Apellido
    tk.Label(form_frame, text="Apellido:", font=("Segoe UI", 9)).grid(row=1, column=0, sticky="w", pady=4)
    e_apellido = tk.Entry(form_frame, font=("Segoe UI", 9))
    e_apellido.grid(row=1, column=1, sticky="ew", padx=8, pady=4)

    # Fila 2: Correo
    tk.Label(form_frame, text="Correo Electrónico:", font=("Segoe UI", 9)).grid(row=2, column=0, sticky="w", pady=4)
    e_email = tk.Entry(form_frame, font=("Segoe UI", 9))
    e_email.grid(row=2, column=1, sticky="ew", padx=8, pady=4)

    # Fila 3: Opciones con columnspan=2
    lbl_span = tk.Label(
        form_frame,
        text="Este bloque ocupa 2 columnas completas (columnspan=2)",
        bg="#cfd8dc",
        font=("Segoe UI", 8, "italic"),
        pady=4
    )
    lbl_span.grid(row=3, column=0, columnspan=2, sticky="ew", pady=8)

    # Fila 4: Botones alineados
    btn_box = tk.Frame(form_frame)
    btn_box.grid(row=4, column=0, columnspan=2, sticky="e", pady=8)

    tk.Button(btn_box, text="Cancelar", width=10).pack(side="left", padx=5)
    tk.Button(btn_box, text="Guardar", width=10, bg="#2e7d32", fg="white").pack(side="left")

    return tab


def crear_tab_place(notebook):
    """Crea la pestaña demostrativa de place()."""
    tab = ttk.Frame(notebook)
    notebook.add(tab, text="3. Gestor place()")

    # Explicación
    lbl_info = tk.Label(
        tab,
        text=(
            "place() posiciona widgets de forma explícita mediante coordenadas X e Y.\n"
            "Coordenadas absolutas: x=50, y=100 (píxeles fijos).\n"
            "Coordenadas relativas: relx=0.5, rely=0.5 (fracción de 0.0 a 1.0 del tamaño padre)."
        ),
        font=("Segoe UI", 9),
        bg="#fff3e0",
        fg="#e65100",
        relief="groove",
        padx=10,
        pady=8,
        justify="left"
    )
    lbl_info.pack(fill="x", padx=10, pady=8)

    # Área del lienzo libre para place()
    area = tk.Frame(tab, bg="#263238")
    area.pack(fill="both", expand=True, padx=10, pady=5)

    # Elemento fijo en esquina superior izquierda (absoluto)
    lbl_fijo = tk.Label(area, text="Posición Absoluta:\nx=15, y=15", bg="#ff5722", fg="white", font=("Segoe UI", 8))
    lbl_fijo.place(x=15, y=15, width=130, height=45)

    # Elemento en esquina superior derecha
    lbl_der = tk.Label(area, text="relx=0.95, rely=0.1\nanchor='ne'", bg="#00bcd4", fg="black", font=("Segoe UI", 8))
    lbl_der.place(relx=0.95, rely=0.05, anchor="ne", width=130, height=45)

    # Elemento en el centro exacto (relativo)
    lbl_centro = tk.Label(
        area,
        text="Centro Exacto:\nrelx=0.5, rely=0.5\nanchor='center'",
        bg="#4caf50",
        fg="white",
        font=("Segoe UI", 9, "bold"),
        relief="raised",
        bd=3
    )
    lbl_centro.place(relx=0.5, rely=0.5, anchor="center", width=220, height=70)

    # Barra flotante inferior relativa
    lbl_inferior = tk.Label(
        area,
        text="Barra Inferior Relativa: relwidth=0.9, relx=0.05, rely=0.88",
        bg="#ffca28",
        fg="#212121",
        font=("Segoe UI", 8, "bold")
    )
    lbl_inferior.place(relx=0.05, rely=0.85, relwidth=0.9, height=30)

    return tab


def main():
    root = tk.Tk()
    root.title("02 - Administradores de Geometría: pack, grid y place")
    root.geometry("620x520")
    root.minsize(550, 450)

    # Encabezado
    tk.Label(
        root,
        text="Comparativa de Gestores de Geometría en Tkinter",
        font=("Segoe UI", 14, "bold"),
        bg="#37474f",
        fg="#ffffff",
        pady=8
    ).pack(fill="x")

    # Contenedor de pestañas (ttk.Notebook)
    notebook = ttk.Notebook(root)
    notebook.pack(fill="both", expand=True, padx=10, pady=10)

    # Creación de cada pestaña
    crear_tab_pack(notebook)
    crear_tab_grid(notebook)
    crear_tab_place(notebook)

    # Pie de página informativo
    tk.Label(
        root,
        text="Consejo: Utiliza grid() para formularios y vistas estructuradas, y pack() para paneles sencillos.",
        font=("Segoe UI", 8, "italic"),
        fg="#616161",
        pady=5
    ).pack(side="bottom")

    root.mainloop()


if __name__ == "__main__":
    main()
