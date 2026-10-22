"""
06_menus_y_dialogos.py
======================
Demostración de barras de menú, menús contextuales y cuadros de diálogo estándar.

Conceptos cubiertos:
1. tk.Menu:
   - Creación de barra de menú principal (menubar).
   - Menús desplegables: Archivo, Edición, Opciones, Ayuda.
   - Separadores, atajos visuales (accelerators) y submenús.
   - Ítems de tipo casilla (add_checkbutton) y radio (add_radiobutton).
   - Menú contextual emergente con clic derecho (<Button-3>).
2. Cuadros de diálogo de tkinter.messagebox:
   - showinfo, showwarning, showerror, askyesno, askokcancel.
3. Cuadros de diálogo de archivos (tkinter.filedialog):
   - askopenfilename: seleccionar archivo para abrir.
   - asksaveasfilename: guardar archivo con extensión.
   - askdirectory: seleccionar una carpeta del sistema.
4. Selector de color (tkinter.colorchooser):
   - askcolor: selección de color en paleta hexadecimal.
5. Cuadros de entrada simple (tkinter.simpledialog):
   - askstring, askinteger, askfloat.
"""

import os
import tkinter as tk
from tkinter import messagebox, filedialog, colorchooser, simpledialog


class DemoMenusYDialogos:
    def __init__(self, root):
        self.root = root
        self.root.title("06 - Menús y Cuadros de Diálogo Estándar")
        self.root.geometry("820x620")
        self.root.minsize(700, 520)

        # Variables para menús
        self.var_modo_oscuro = tk.BooleanVar(value=False)
        self.var_nivel_zoom = tk.StringVar(value="100%")

        self._crear_barra_menus()
        self._crear_menu_contextual()
        self._crear_interfaz_principal()

    def _crear_barra_menus(self):
        """Construye la barra de menú superior."""
        menubar = tk.Menu(self.root)

        # 1. Menú Archivo
        menu_archivo = tk.Menu(menubar, tearoff=0)
        menu_archivo.add_command(label="Nuevo", accelerator="Ctrl+N", command=self._nuevo_archivo)
        menu_archivo.add_command(label="Abrir archivo...", accelerator="Ctrl+O", command=self._abrir_archivo)
        menu_archivo.add_command(label="Guardar como...", accelerator="Ctrl+S", command=self._guardar_archivo)
        menu_archivo.add_command(label="Seleccionar carpeta...", command=self._seleccionar_carpeta)
        menu_archivo.add_separator()
        menu_archivo.add_command(label="Salir", accelerator="Alt+F4", command=self.root.quit)
        menubar.add_cascade(label="Archivo", menu=menu_archivo)

        # 2. Menú Edición
        menu_edicion = tk.Menu(menubar, tearoff=0)
        menu_edicion.add_command(label="Deshacer", accelerator="Ctrl+Z", command=lambda: self._log("Acción: Deshacer"))
        menu_edicion.add_command(label="Rehacer", accelerator="Ctrl+Y", command=lambda: self._log("Acción: Rehacer"))
        menu_edicion.add_separator()
        menu_edicion.add_command(label="Cortar", accelerator="Ctrl+X", command=lambda: self.txt_editor.event_generate("<<Cut>>"))
        menu_edicion.add_command(label="Copiar", accelerator="Ctrl+C", command=lambda: self.txt_editor.event_generate("<<Copy>>"))
        menu_edicion.add_command(label="Pegar", accelerator="Ctrl+V", command=lambda: self.txt_editor.event_generate("<<Paste>>"))
        menubar.add_cascade(label="Edición", menu=menu_edicion)

        # 3. Menú Ver (con Checkbutton y Radiobuttons)
        menu_ver = tk.Menu(menubar, tearoff=0)
        menu_ver.add_checkbutton(
            label="Modo Oscuro",
            variable=self.var_modo_oscuro,
            command=self._toggle_modo_oscuro
        )
        menu_ver.add_separator()

        # Submenú de Zoom
        submenu_zoom = tk.Menu(menu_ver, tearoff=0)
        for nivel in ["50%", "75%", "100%", "150%", "200%"]:
            submenu_zoom.add_radiobutton(
                label=nivel,
                value=nivel,
                variable=self.var_nivel_zoom,
                command=lambda: self._log(f"Zoom cambiado a: {self.var_nivel_zoom.get()}")
            )
        menu_ver.add_cascade(label="Nivel de Zoom", menu=submenu_zoom)
        menubar.add_cascade(label="Ver", menu=menu_ver)

        # 4. Menú Ayuda
        menu_ayuda = tk.Menu(menubar, tearoff=0)
        menu_ayuda.add_command(label="Documentación", command=lambda: messagebox.showinfo("Ayuda", "Módulo de demostración de Tkinter."))
        menu_ayuda.add_separator()
        menu_ayuda.add_command(label="Acerca de...", command=self._mostrar_acerca_de)
        menubar.add_cascade(label="Ayuda", menu=menu_ayuda)

        # Conectar menubar a la ventana principal
        self.root.config(menu=menubar)

    def _crear_menu_contextual(self):
        """Crea el menú emergente del clic derecho."""
        self.menu_popup = tk.Menu(self.root, tearoff=0)
        self.menu_popup.add_command(label="Copiar texto", command=lambda: self.txt_editor.event_generate("<<Copy>>"))
        self.menu_popup.add_command(label="Pegar texto", command=lambda: self.txt_editor.event_generate("<<Paste>>"))
        self.menu_popup.add_separator()
        self.menu_popup.add_command(label="Cambiar Color de Fondo", command=self._seleccionar_color)
        self.menu_popup.add_command(label="Limpiar Área", command=self._nuevo_archivo)

    def _crear_interfaz_principal(self):
        # Título
        tk.Label(
            self.root,
            text="Explorador de Menús y Cuadros de Diálogo Nativos",
            font=("Segoe UI", 13, "bold"),
            bg="#00695c",
            fg="white",
            pady=8
        ).pack(fill="x")

        # Contenedor dividido en 2 paneles
        body = tk.Frame(self.root, bg="#eceff1")
        body.pack(fill="both", expand=True, padx=10, pady=8)

        # Panel Izquierdo: Botonera de Diálogos
        panel_izq = tk.LabelFrame(
            body,
            text=" Probar Cuadros de Diálogo ",
            font=("Segoe UI", 10, "bold"),
            padx=10,
            pady=8,
            width=280
        )
        panel_izq.pack(side="left", fill="y", padx=(0, 6))
        panel_izq.pack_propagate(False)

        # Grupo Mensajes
        tk.Label(panel_izq, text="Mensajes Informativos:", font=("Segoe UI", 9, "bold")).pack(anchor="w", pady=(2, 2))
        tk.Button(panel_izq, text="showinfo()", anchor="w", command=lambda: messagebox.showinfo("Información", "Operación realizada con éxito.")).pack(fill="x", pady=2)
        tk.Button(panel_izq, text="showwarning()", anchor="w", command=lambda: messagebox.showwarning("Advertencia", "El archivo tiene cambios sin guardar.")).pack(fill="x", pady=2)
        tk.Button(panel_izq, text="showerror()", anchor="w", command=lambda: messagebox.showerror("Error", "No se pudo conectar con el servidor.")).pack(fill="x", pady=2)

        # Grupo Confirmaciones
        tk.Label(panel_izq, text="Confirmación de Usuario:", font=("Segoe UI", 9, "bold")).pack(anchor="w", pady=(8, 2))
        tk.Button(panel_izq, text="askyesno()", anchor="w", command=self._probar_askyesno).pack(fill="x", pady=2)
        tk.Button(panel_izq, text="askokcancel()", anchor="w", command=self._probar_askokcancel).pack(fill="x", pady=2)

        # Grupo Entradas simples
        tk.Label(panel_izq, text="Entradas Simples:", font=("Segoe UI", 9, "bold")).pack(anchor="w", pady=(8, 2))
        tk.Button(panel_izq, text="simpledialog.askstring()", anchor="w", command=self._probar_askstring).pack(fill="x", pady=2)
        tk.Button(panel_izq, text="simpledialog.askinteger()", anchor="w", command=self._probar_askinteger).pack(fill="x", pady=2)

        # Selector de color
        tk.Label(panel_izq, text="Paleta de Colores:", font=("Segoe UI", 9, "bold")).pack(anchor="w", pady=(8, 2))
        tk.Button(panel_izq, text="colorchooser.askcolor()", anchor="w", bg="#00897b", fg="white", command=self._seleccionar_color).pack(fill="x", pady=2)

        # Panel Derecho: Editor y Log de Respuestas
        panel_der = tk.Frame(body, bg="#eceff1")
        panel_der.pack(side="right", fill="both", expand=True, padx=(6, 0))

        # Editor de texto que reacciona a abrir y guardar
        f_editor = tk.LabelFrame(
            panel_der,
            text=" Área de Documento (Haz clic derecho aquí para el Menú Contextual) ",
            font=("Segoe UI", 9, "bold"),
            padx=6,
            pady=6
        )
        f_editor.pack(fill="both", expand=True)

        self.txt_editor = tk.Text(f_editor, wrap="word", font=("Segoe UI", 10), height=10)
        self.txt_editor.pack(fill="both", expand=True)
        self.txt_editor.insert(
            "1.0",
            "Bienvenido al visor de documentos.\n\n"
            "• Utiliza el menú superior 'Archivo' para Abrir o Guardar un archivo real.\n"
            "• Haz CLIC DERECHO sobre este texto para desplegar el menú contextual.\n"
            "• Prueba los botones de diálogo en el panel izquierdo."
        )

        # Vincular clic derecho al menú contextual
        self.txt_editor.bind("<Button-3>", self._mostrar_menu_contextual)

        # Registro de respuestas de diálogos
        f_log = tk.LabelFrame(panel_der, text=" Historial de Respuestas de Diálogos ", font=("Segoe UI", 9, "bold"), padx=6, pady=4)
        f_log.pack(fill="x", pady=(6, 0))

        self.lbl_log = tk.Label(f_log, text="Ningún diálogo invocado aún.", anchor="w", justify="left", font=("Consolas", 9), bg="white", relief="sunken", pady=6, padx=6)
        self.lbl_log.pack(fill="x")

    def _mostrar_menu_contextual(self, event):
        """Muestra el menú emergente en las coordenadas del cursor."""
        self.menu_popup.post(event.x_root, event.y_root)

    def _log(self, mensaje):
        """Actualiza el label de historial de resultados."""
        self.lbl_log.config(text=mensaje)

    def _nuevo_archivo(self):
        self.txt_editor.delete("1.0", tk.END)
        self._log("Acción: Documento limpiado (Nuevo).")

    def _abrir_archivo(self):
        ruta = filedialog.askopenfilename(
            title="Seleccionar archivo para abrir",
            filetypes=[("Archivos de texto", "*.txt *.py *.md *.json"), ("Todos los archivos", "*.*")]
        )
        if ruta:
            try:
                with open(ruta, "r", encoding="utf-8") as f:
                    contenido = f.read()
                self.txt_editor.delete("1.0", tk.END)
                self.txt_editor.insert("1.0", contenido)
                self._log(f"Abierto: {os.path.basename(ruta)} ({len(contenido)} caracteres)")
            except Exception as e:
                messagebox.showerror("Error de lectura", f"No se pudo leer el archivo:\n{e}")

    def _guardar_archivo(self):
        ruta = filedialog.asksaveasfilename(
            title="Guardar documento como...",
            defaultextension=".txt",
            filetypes=[("Archivo de Texto", "*.txt"), ("Script Python", "*.py"), ("Todos los archivos", "*.*")]
        )
        if ruta:
            try:
                contenido = self.txt_editor.get("1.0", tk.END)
                with open(ruta, "w", encoding="utf-8") as f:
                    f.write(contenido)
                self._log(f"Guardado exitoso: {os.path.basename(ruta)}")
                messagebox.showinfo("Guardado", f"Archivo guardado correctamente en:\n{ruta}")
            except Exception as e:
                messagebox.showerror("Error al guardar", f"No se pudo guardar:\n{e}")

    def _seleccionar_carpeta(self):
        carpeta = filedialog.askdirectory(title="Seleccionar carpeta de trabajo")
        if carpeta:
            self._log(f"Carpeta seleccionada: {carpeta}")

    def _seleccionar_color(self):
        color = colorchooser.askcolor(title="Selecciona un color de fondo para el editor")
        # color retorna una tupla: ((r, g, b), '#hex')
        if color[1]:
            self.txt_editor.config(bg=color[1])
            self._log(f"Color de fondo cambiado a: {color[1]} (RGB: {color[0]})")

    def _probar_askyesno(self):
        respuesta = messagebox.askyesno("Confirmación", "¿Deseas formatear la vista actual?")
        self._log(f"askyesno() retornó: {respuesta} (Tipo: {type(respuesta).__name__})")

    def _probar_askokcancel(self):
        respuesta = messagebox.askokcancel("Confirmación", "¿Deseas continuar con la operación en curso?")
        self._log(f"askokcancel() retornó: {respuesta} (Tipo: {type(respuesta).__name__})")

    def _probar_askstring(self):
        nombre = simpledialog.askstring("Entrada de Texto", "¿Cuál es tu lenguaje de programación favorito?")
        self._log(f"askstring() retornó: '{nombre}'")

    def _probar_askinteger(self):
        edad = simpledialog.askinteger("Entrada Numérica", "Ingresa tu edad:", minvalue=1, maxvalue=120)
        self._log(f"askinteger() retornó: {edad}")

    def _toggle_modo_oscuro(self):
        oscuro = self.var_modo_oscuro.get()
        bg = "#212121" if oscuro else "#ffffff"
        fg = "#e0e0e0" if oscuro else "#000000"
        self.txt_editor.config(bg=bg, fg=fg, insertbackground=fg)
        self._log(f"Modo Oscuro: {'Activado' if oscuro else 'Desactivado'}")

    def _mostrar_acerca_de(self):
        messagebox.showinfo(
            "Acerca de este módulo",
            "Módulo 06: Menús y Diálogos Estándar\n"
            "Desarrollado para el repositorio de demostración de Tkinter.\n"
            "Python 3 con Tkinter nativo."
        )


def main():
    root = tk.Tk()
    app = DemoMenusYDialogos(root)
    root.mainloop()


if __name__ == "__main__":
    main()
