"""
03_widgets_interactivos.py
==========================
Demostración de los widgets interactivos y variables de control en Tkinter.

Conceptos cubiertos:
1. Variables de control reactivas:
   - tk.StringVar, tk.IntVar, tk.BooleanVar, tk.DoubleVar.
   - Observación reactiva con .trace_add("write", callback).
2. Widgets de entrada y selección:
   - tk.Entry: entrada de texto y contraseña con ocultamiento (show='*').
   - tk.Checkbutton: casillas de verificación para valores booleanos.
   - tk.Radiobutton: botones de opción excluyente en grupo.
   - tk.Scale: deslizadores para rangos numéricos continuos.
   - tk.Spinbox: selector numérico por pasos discretos.
   - tk.Text: área de texto multilínea asociada a un Scrollbar vertical.
3. Panel de previsualización que muestra el estado de las variables en tiempo real.
"""

import tkinter as tk
from tkinter import ttk


class DemoWidgetsInteractivos:
    def __init__(self, root):
        self.root = root
        self.root.title("03 - Widgets Interactivos y Variables de Control")
        self.root.geometry("780x640")
        self.root.minsize(700, 580)
        self.root.configure(bg="#f5f7fa")

        # ---------------------------------------------------------
        # Variables de control de Tkinter
        # ---------------------------------------------------------
        self.var_usuario = tk.StringVar(value="DevPython")
        self.var_clave = tk.StringVar(value="Tkinter2026")
        self.var_mostrar_clave = tk.BooleanVar(value=False)
        self.var_nivel = tk.StringVar(value="Intermedio")
        self.var_suscrito = tk.BooleanVar(value=True)
        self.var_notificaciones = tk.BooleanVar(value=False)
        self.var_volumen = tk.DoubleVar(value=65.0)
        self.var_edad = tk.IntVar(value=25)

        # Configurar observación de cambios (listeners)
        for var in [self.var_usuario, self.var_clave, self.var_nivel,
                    self.var_suscrito, self.var_notificaciones,
                    self.var_volumen, self.var_edad]:
            var.trace_add("write", self.actualizar_resumen)

        self._crear_interfaz()
        self.actualizar_resumen()

    def _crear_interfaz(self):
        # Título
        tk.Label(
            self.root,
            text="Widgets Interactivos y Enlace de Datos (Data Binding)",
            font=("Segoe UI", 14, "bold"),
            bg="#283593",
            fg="white",
            pady=8
        ).pack(fill="x")

        # Contenedor principal en 2 columnas: izquierda (widgets) y derecha (resumen)
        main_frame = tk.Frame(self.root, bg="#f5f7fa")
        main_frame.pack(fill="both", expand=True, padx=12, pady=10)

        # ------------------ COLUMNA IZQUIERDA ------------------
        col_izq = tk.Frame(main_frame, bg="#f5f7fa")
        col_izq.pack(side="left", fill="both", expand=True, padx=(0, 6))

        # 1. Grupo: Entradas de texto (Entry)
        g_entry = tk.LabelFrame(col_izq, text=" 1. Entradas (Entry) ", font=("Segoe UI", 9, "bold"), padx=10, pady=8)
        g_entry.pack(fill="x", pady=4)

        tk.Label(g_entry, text="Usuario:").grid(row=0, column=0, sticky="w", pady=2)
        tk.Entry(g_entry, textvariable=self.var_usuario, width=22).grid(row=0, column=1, sticky="w", padx=6, pady=2)

        tk.Label(g_entry, text="Contraseña:").grid(row=1, column=0, sticky="w", pady=2)
        self.entry_clave = tk.Entry(g_entry, textvariable=self.var_clave, show="*", width=22)
        self.entry_clave.grid(row=1, column=1, sticky="w", padx=6, pady=2)

        chk_ver_clave = tk.Checkbutton(
            g_entry,
            text="Mostrar",
            variable=self.var_mostrar_clave,
            command=self._toggle_ver_clave,
            font=("Segoe UI", 8)
        )
        chk_ver_clave.grid(row=1, column=2, padx=4)

        # 2. Grupo: Radiobuttons (Selección Única)
        g_radio = tk.LabelFrame(col_izq, text=" 2. Botones de Opción (Radiobutton) ", font=("Segoe UI", 9, "bold"), padx=10, pady=8)
        g_radio.pack(fill="x", pady=4)

        tk.Label(g_radio, text="Nivel de Experiencia:").pack(anchor="w")
        niveles_frame = tk.Frame(g_radio)
        niveles_frame.pack(fill="x", pady=2)
        for nivel in ["Principiante", "Intermedio", "Avanzado"]:
            tk.Radiobutton(
                niveles_frame,
                text=nivel,
                value=nivel,
                variable=self.var_nivel
            ).pack(side="left", padx=5)

        # 3. Grupo: Checkbuttons (Casillas Múltiples)
        g_check = tk.LabelFrame(col_izq, text=" 3. Casillas de Verificación (Checkbutton) ", font=("Segoe UI", 9, "bold"), padx=10, pady=8)
        g_check.pack(fill="x", pady=4)

        tk.Checkbutton(g_check, text="Suscribirse al boletín de noticias", variable=self.var_suscrito).pack(anchor="w")
        tk.Checkbutton(g_check, text="Activar notificaciones de escritorio", variable=self.var_notificaciones).pack(anchor="w")

        # 4. Grupo: Scale y Spinbox
        g_numericos = tk.LabelFrame(col_izq, text=" 4. Controles Numéricos (Scale & Spinbox) ", font=("Segoe UI", 9, "bold"), padx=10, pady=8)
        g_numericos.pack(fill="x", pady=4)

        tk.Label(g_numericos, text="Edad (Spinbox):").grid(row=0, column=0, sticky="w", pady=4)
        tk.Spinbox(g_numericos, from_=10, to=100, textvariable=self.var_edad, width=8).grid(row=0, column=1, sticky="w", padx=6)

        tk.Label(g_numericos, text="Volumen (Scale):").grid(row=1, column=0, sticky="w", pady=4)
        tk.Scale(
            g_numericos,
            from_=0,
            to=100,
            orient="horizontal",
            variable=self.var_volumen,
            length=180
        ).grid(row=1, column=1, sticky="w", padx=6)

        # ------------------ COLUMNA DERECHA ------------------
        col_der = tk.Frame(main_frame, bg="#f5f7fa")
        col_der.pack(side="right", fill="both", expand=True, padx=(6, 0))

        # 5. Grupo: Área de Texto con Scrollbar
        g_text = tk.LabelFrame(col_der, text=" 5. Texto Multilínea con Scrollbar (Text) ", font=("Segoe UI", 9, "bold"), padx=8, pady=8)
        g_text.pack(fill="both", expand=True, pady=4)

        text_scroll_frame = tk.Frame(g_text)
        text_scroll_frame.pack(fill="both", expand=True)

        scrollbar = tk.Scrollbar(text_scroll_frame)
        scrollbar.pack(side="right", fill="y")

        self.txt_comentario = tk.Text(text_scroll_frame, wrap="word", yscrollcommand=scrollbar.set, height=6)
        self.txt_comentario.pack(side="left", fill="both", expand=True)
        scrollbar.config(command=self.txt_comentario.yview)

        self.txt_comentario.insert("1.0", "Este es un widget Text con scrollbar.\nPuedes escribir comentarios largos aquí.")
        self.txt_comentario.bind("<KeyRelease>", lambda e: self.actualizar_resumen())

        # 6. Panel de Resumen Reactivo
        g_resumen = tk.LabelFrame(
            col_der,
            text=" Estado Reactivo en Tiempo Real ",
            font=("Segoe UI", 9, "bold"),
            fg="#0d47a1",
            padx=10,
            pady=10
        )
        g_resumen.pack(fill="both", expand=True, pady=4)

        self.lbl_estado = tk.Label(
            g_resumen,
            text="",
            font=("Consolas", 9),
            justify="left",
            anchor="nw",
            bg="#ffffff",
            relief="sunken",
            bd=1,
            padx=8,
            pady=8
        )
        self.lbl_estado.pack(fill="both", expand=True)

    def _toggle_ver_clave(self):
        """Muestra u oculta los caracteres del campo contraseña."""
        if self.var_mostrar_clave.get():
            self.entry_clave.config(show="")
        else:
            self.entry_clave.config(show="*")

    def actualizar_resumen(self, *args):
        """Refresca la tarjeta de estado con los valores de todas las variables."""
        try:
            comentario_len = len(self.txt_comentario.get("1.0", tk.END).strip())
        except Exception:
            comentario_len = 0

        resumen = (
            f"• Usuario:          {self.var_usuario.get()}\n"
            f"• Clave (len):      {len(self.var_clave.get())} caracteres\n"
            f"• Nivel:            {self.var_nivel.get()}\n"
            f"• Suscripción:      {'Sí' if self.var_suscrito.get() else 'No'}\n"
            f"• Notificaciones:   {'Activadas' if self.var_notificaciones.get() else 'Desactivadas'}\n"
            f"• Edad:             {self.var_edad.get()} años\n"
            f"• Nivel de Volumen: {self.var_volumen.get():.1f}%\n"
            f"• Longitud Texto:   {comentario_len} caracteres"
        )
        self.lbl_estado.config(text=resumen)


def main():
    root = tk.Tk()
    app = DemoWidgetsInteractivos(root)
    root.mainloop()


if __name__ == "__main__":
    main()
