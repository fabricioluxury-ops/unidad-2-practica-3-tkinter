"""
01_hola_mundo_basico.py
=======================
Demostración de los fundamentos esenciales de Tkinter en Python.

Conceptos cubiertos:
1. Creación e inicialización de la ventana principal (tk.Tk).
2. Configuración de propiedades de la ventana: título, dimensiones, tamaño mínimo y redimensionamiento.
3. Creación y empaquetado de widgets básicos:
   - tk.Label: etiquetas para mostrar texto estático y dinámico.
   - tk.Entry: campo para captura de texto ingresado por el usuario.
   - tk.Button: botones con eventos asociados (comandos).
4. El gestor de geometría pack() con opciones de espaciado (padx, pady).
5. Modificación dinámica de propiedades de widgets en tiempo de ejecución (.config()).
6. Inicio del bucle principal de eventos (root.mainloop()).
"""

import tkinter as tk


def saludar():
    """Obtiene el texto del campo de entrada y actualiza la etiqueta de saludo."""
    nombre = entrada_nombre.get().strip()
    if nombre:
        lbl_saludo.config(
            text=f"¡Hola, {nombre}! Bienvenido al mundo de Tkinter.",
            fg="#1b5e20"  # Verde oscuro
        )
    else:
        lbl_saludo.config(
            text="Por favor, escribe tu nombre antes de presionar el botón.",
            fg="#b71c1c"  # Rojo oscuro
        )


def limpiar():
    """Restaura los valores iniciales de la interfaz."""
    entrada_nombre.delete(0, tk.END)
    lbl_saludo.config(
        text="Escribe tu nombre arriba y haz clic en 'Saludar'.",
        fg="#555555"
    )
    entrada_nombre.focus()  # Devuelve el foco al campo de texto


def main():
    # -------------------------------------------------------------
    # 1. Ventana Principal
    # -------------------------------------------------------------
    global entrada_nombre, lbl_saludo

    root = tk.Tk()
    root.title("01 - Hola Mundo y Fundamentos Básicos")
    root.geometry("500x380")
    root.minsize(400, 320)
    root.configure(bg="#f4f6f9")

    # -------------------------------------------------------------
    # 2. Encabezado
    # -------------------------------------------------------------
    lbl_titulo = tk.Label(
        root,
        text="Fundamentos de Tkinter",
        font=("Segoe UI", 16, "bold"),
        bg="#1e88e5",
        fg="#ffffff",
        pady=10
    )
    # fill="x" hace que la etiqueta ocupe todo el ancho disponible
    lbl_titulo.pack(fill="x", pady=(0, 15))

    lbl_instruccion = tk.Label(
        root,
        text="Introduce tu nombre para interactuar:",
        font=("Segoe UI", 10),
        bg="#f4f6f9",
        fg="#333333"
    )
    lbl_instruccion.pack(pady=(5, 5))

    # -------------------------------------------------------------
    # 3. Campo de Entrada (Entry)
    # -------------------------------------------------------------
    entrada_nombre = tk.Entry(
        root,
        font=("Segoe UI", 11),
        width=30,
        relief="groove",
        bd=2,
        justify="center"
    )
    entrada_nombre.pack(pady=5)
    entrada_nombre.focus()  # Pone el cursor en este campo al iniciar

    # Permitir presionar la tecla Enter para saludar
    entrada_nombre.bind("<Return>", lambda event: saludar())

    # -------------------------------------------------------------
    # 4. Contenedor de Botones (Frame)
    # -------------------------------------------------------------
    frame_botones = tk.Frame(root, bg="#f4f6f9")
    frame_botones.pack(pady=15)

    btn_saludar = tk.Button(
        frame_botones,
        text="Saludar",
        font=("Segoe UI", 10, "bold"),
        bg="#2e7d32",
        fg="#ffffff",
        activebackground="#1b5e20",
        activeforeground="#ffffff",
        padx=15,
        pady=5,
        relief="raised",
        cursor="hand2",
        command=saludar
    )
    btn_saludar.pack(side="left", padx=5)

    btn_limpiar = tk.Button(
        frame_botones,
        text="Limpiar",
        font=("Segoe UI", 10),
        bg="#e0e0e0",
        fg="#212121",
        activebackground="#bdbdbd",
        padx=12,
        pady=5,
        cursor="hand2",
        command=limpiar
    )
    btn_limpiar.pack(side="left", padx=5)

    # -------------------------------------------------------------
    # 5. Etiqueta para Resultados Dinámicos
    # -------------------------------------------------------------
    lbl_saludo = tk.Label(
        root,
        text="Escribe tu nombre arriba y haz clic en 'Saludar'.",
        font=("Segoe UI", 10, "italic"),
        bg="#ffffff",
        fg="#555555",
        relief="solid",
        bd=1,
        padx=12,
        pady=10,
        wraplength=420
    )
    lbl_saludo.pack(pady=10, padx=20, fill="x")

    # -------------------------------------------------------------
    # 6. Botón de Salir
    # -------------------------------------------------------------
    btn_salir = tk.Button(
        root,
        text="Cerrar Ventana",
        font=("Segoe UI", 9),
        bg="#c62828",
        fg="#ffffff",
        activebackground="#8e0000",
        activeforeground="#ffffff",
        cursor="hand2",
        command=root.destroy
    )
    btn_salir.pack(side="bottom", pady=15)

    # Iniciar el bucle de eventos
    root.mainloop()


if __name__ == "__main__":
    main()
