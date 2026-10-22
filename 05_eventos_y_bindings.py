"""
05_eventos_y_bindings.py
========================
Demostración completa del sistema de eventos y vinculaciones (bindings) en Tkinter.

Conceptos cubiertos:
1. Sintaxis de vinculación: widget.bind(secuencia, callback).
2. El objeto evento de Tkinter (event.x, event.y, event.char, event.keysym, event.widget).
3. Eventos de Ratón:
   - <Button-1> (Clic izquierdo), <Button-2> (Clic central), <Button-3> (Clic derecho).
   - <Double-Button-1> (Doble clic).
   - <Motion> (Movimiento del cursor y coordenadas relativas).
   - <Enter> y <Leave> (Eventos de cursor entrando y saliendo de un widget / Hover).
   - <B1-Motion> (Arrastre con clic izquierdo sostenido).
4. Eventos de Teclado:
   - <KeyPress> y captura de teclas individuales (keysym, keycode, char).
   - Combinaciones de teclas (<Control-s>, <Control-q>, <Escape>, <Return>).
5. Eventos de Ventana y Foco:
   - <FocusIn>, <FocusOut>, y <Configure> (detección de redimensionamiento).
6. Consola integrada en tiempo real para inspeccionar el flujo de eventos.
"""

from datetime import datetime
import tkinter as tk
from tkinter import ttk


class DemoEventosBindings:
    def __init__(self, root):
        self.root = root
        self.root.title("05 - Sistema de Eventos y Bindings en Tkinter")
        self.root.geometry("860x680")
        self.root.minsize(780, 580)
        self.root.configure(bg="#f8f9fa")

        self._crear_interfaz()
        self._configurar_bindings_globales()

    def _crear_interfaz(self):
        # Título superior
        tk.Label(
            self.root,
            text="Controlador y Monitor de Eventos en Tiempo Real",
            font=("Segoe UI", 13, "bold"),
            bg="#303f9f",
            fg="white",
            pady=8
        ).pack(fill="x")

        # Contenedor dividido en 2 columnas: izquierda (zonas interactivas), derecha (consola)
        body = tk.Frame(self.root, bg="#f8f9fa")
        body.pack(fill="both", expand=True, padx=12, pady=10)

        # ------------------ COLUMNA IZQUIERDA: ZONAS INTERACTIVAS ------------------
        col_izq = tk.Frame(body, bg="#f8f9fa")
        col_izq.pack(side="left", fill="both", expand=True, padx=(0, 6))

        # 1. Zona de Pruebas de Ratón
        f_mouse = tk.LabelFrame(
            col_izq,
            text=" 1. Área Interactiva de Ratón ",
            font=("Segoe UI", 10, "bold"),
            padx=10,
            pady=10
        )
        f_mouse.pack(fill="both", expand=True, pady=4)

        self.canvas_interactivo = tk.Canvas(
            f_mouse,
            bg="#e3f2fd",
            height=160,
            cursor="crosshair",
            relief="ridge",
            bd=2
        )
        self.canvas_interactivo.pack(fill="both", expand=True)

        self.canvas_interactivo.create_text(
            180, 80,
            text="¡Interactúa aquí!\n• Haz Clic (Izq, Der, Centro)\n• Haz Doble Clic\n• Mueve el ratón o arrastra",
            fill="#1565c0",
            font=("Segoe UI", 9, "bold"),
            justify="center",
            tags="texto_guia"
        )

        # Asociar eventos de ratón al canvas
        self.canvas_interactivo.bind("<Button-1>", lambda e: self._registrar_evento("Clic Izquierdo (<Button-1>)", e))
        self.canvas_interactivo.bind("<Button-2>", lambda e: self._registrar_evento("Clic Central (<Button-2>)", e))
        self.canvas_interactivo.bind("<Button-3>", lambda e: self._registrar_evento("Clic Derecho (<Button-3>)", e))
        self.canvas_interactivo.bind("<Double-Button-1>", lambda e: self._registrar_evento("Doble Clic (<Double-Button-1>)", e))
        self.canvas_interactivo.bind("<Motion>", self._on_mouse_motion)
        self.canvas_interactivo.bind("<B1-Motion>", self._on_b1_drag)
        self.canvas_interactivo.bind("<Enter>", lambda e: self._on_hover(True))
        self.canvas_interactivo.bind("<Leave>", lambda e: self._on_hover(False))

        self.lbl_coords = tk.Label(
            f_mouse,
            text="Coordenadas del cursor: X=0, Y=0",
            font=("Segoe UI", 9),
            fg="#455a64"
        )
        self.lbl_coords.pack(anchor="w", pady=(4, 0))

        # 2. Zona de Pruebas de Teclado
        f_teclado = tk.LabelFrame(
            col_izq,
            text=" 2. Área Interactiva de Teclado ",
            font=("Segoe UI", 10, "bold"),
            padx=10,
            pady=10
        )
        f_teclado.pack(fill="x", pady=6)

        tk.Label(
            f_teclado,
            text="Haz foco en este campo y escribe cualquier tecla o atajo:",
            font=("Segoe UI", 9)
        ).pack(anchor="w")

        self.entry_teclas = tk.Entry(f_teclado, font=("Segoe UI", 11), bg="#ffffff", relief="groove", bd=2)
        self.entry_teclas.pack(fill="x", pady=6)
        self.entry_teclas.bind("<KeyPress>", self._on_key_press)
        self.entry_teclas.bind("<FocusIn>", lambda e: self._registrar_evento("Foco Recibido (<FocusIn>)", e))
        self.entry_teclas.bind("<FocusOut>", lambda e: self._registrar_evento("Foco Perdido (<FocusOut>)", e))

        # Indicador de atajos globales
        lbl_atajos = tk.Label(
            f_teclado,
            text="Atajos activos en la ventana:\n• Ctrl+S: Guardar simulado\n• Ctrl+L: Limpiar consola\n• Esc: Desenfocar",
            font=("Segoe UI", 8, "italic"),
            fg="#546e7a",
            justify="left"
        )
        lbl_atajos.pack(anchor="w")

        # ------------------ COLUMNA DERECHA: CONSOLA DE EVENTOS ------------------
        col_der = tk.Frame(body, bg="#f8f9fa")
        col_der.pack(side="right", fill="both", expand=True, padx=(6, 0))

        f_consola = tk.LabelFrame(
            col_der,
            text=" Consola de Inspección de Eventos ",
            font=("Segoe UI", 10, "bold"),
            padx=8,
            pady=8
        )
        f_consola.pack(fill="both", expand=True, pady=4)

        # Área de texto tipo consola
        console_frame = tk.Frame(f_consola)
        console_frame.pack(fill="both", expand=True)

        scroll_consola = tk.Scrollbar(console_frame)
        scroll_consola.pack(side="right", fill="y")

        self.txt_consola = tk.Text(
            console_frame,
            wrap="word",
            bg="#1e1e1e",
            fg="#00e676",
            insertbackground="white",
            font=("Consolas", 8),
            yscrollcommand=scroll_consola.set
        )
        self.txt_consola.pack(side="left", fill="both", expand=True)
        scroll_consola.config(command=self.txt_consola.yview)

        # Barra de botones para consola
        btn_bar = tk.Frame(f_consola)
        btn_bar.pack(fill="x", pady=(6, 0))

        tk.Button(
            btn_bar,
            text="Limpiar Consola",
            font=("Segoe UI", 8),
            command=self.limpiar_consola
        ).pack(side="left")

        self.lbl_contador_eventos = tk.Label(
            btn_bar,
            text="Eventos capturados: 0",
            font=("Segoe UI", 8),
            fg="#616161"
        )
        self.lbl_contador_eventos.pack(side="right")
        self.contador_eventos = 0

    def _configurar_bindings_globales(self):
        """Asocia atajos de teclado a toda la ventana."""
        self.root.bind("<Control-s>", self._atajo_guardar)
        self.root.bind("<Control-S>", self._atajo_guardar)
        self.root.bind("<Control-l>", lambda e: self.limpiar_consola())
        self.root.bind("<Control-L>", lambda e: self.limpiar_consola())
        self.root.bind("<Escape>", lambda e: self.root.focus_set())

        # Evento de cambio de tamaño de la ventana
        self.root.bind("<Configure>", self._on_window_configure)

    def _registrar_evento(self, tipo, event):
        """Añade una línea de diagnóstico en la consola para cualquier evento."""
        self.contador_eventos += 1
        hora = datetime.now().strftime("%H:%M:%S.%f")[:-3]
        pos = f"x={getattr(event, 'x', '?')}, y={getattr(event, 'y', '?')}"
        linea = f"[{hora}] #{self.contador_eventos:04d} -> {tipo} | {pos}\n"

        self.txt_consola.insert(tk.END, linea)
        self.txt_consola.see(tk.END)
        self.lbl_contador_eventos.config(text=f"Eventos capturados: {self.contador_eventos}")

    def _on_mouse_motion(self, event):
        """Rastreo en vivo de la posición del ratón."""
        self.lbl_coords.config(text=f"Coordenadas del cursor: X={event.x}, Y={event.y}")

    def _on_b1_drag(self, event):
        """Dibuja un pequeño punto durante el arrastre con el botón izquierdo presionado."""
        r = 3
        self.canvas_interactivo.create_oval(
            event.x - r, event.y - r, event.x + r, event.y + r,
            fill="#d81b60", outline=""
        )
        self._registrar_evento("Arrastre (<B1-Motion>)", event)

    def _on_hover(self, entrando):
        """Efecto visual al entrar o salir del área."""
        if entrando:
            self.canvas_interactivo.config(bg="#bbdefb")
        else:
            self.canvas_interactivo.config(bg="#e3f2fd")

    def _on_key_press(self, event):
        """Captura información detallada de la tecla pulsada."""
        info = f"Tecla '{event.char}' (keysym={event.keysym}, keycode={event.keycode})"
        self._registrar_evento(f"<KeyPress>: {info}", event)

    def _atajo_guardar(self, event):
        """Manejador para el atajo Ctrl+S."""
        self._registrar_evento("★ ATAJO: <Control-s> (Guardado Simulado)", event)
        return "break"  # Evita que el evento continúe propagándose

    def _on_window_configure(self, event):
        """Manejador de redimensionamiento de ventana (solo cuando el origen es la ventana principal)."""
        if event.widget == self.root:
            pass  # Se puede inspeccionar event.width y event.height

    def limpiar_consola(self):
        """Borra el contenido del área de consola."""
        self.txt_consola.delete("1.0", tk.END)
        self.contador_eventos = 0
        self.lbl_contador_eventos.config(text="Eventos capturados: 0")


def main():
    root = tk.Tk()
    app = DemoEventosBindings(root)
    root.mainloop()


if __name__ == "__main__":
    main()
