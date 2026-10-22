"""
08_arquitectura_poo_app.py
==========================
Demostración de Arquitectura Profesional en Tkinter utilizando
Programación Orientada a Objetos (POO), navegación multivista y separación de responsabilidades.

Conceptos cubiertos:
1. Clase Principal encapsulada:
   - Hereda de tk.Tk o gestiona la ventana raíz con control total del ciclo de vida.
   - Manejo del protocolo de cierre de ventana ('WM_DELETE_WINDOW').
2. Sistema de Navegación Multivista (Single Page Application - SPA en escritorio):
   - Contenedor apilado donde las vistas heredan de ttk.Frame y se intercambian con tkraise().
   - Barra lateral (Sidebar) de navegación con botones interactivos y estado activo.
3. Separación de Modelo, Vista y Estado:
   - Capa de datos desacoplada que gestiona la lógica (repositorio de tareas).
   - Vistas independientes:
     * VistaDashboard: métricas y resumen general.
     * VistaTareas: CRUD interactivo con Treeview, filtros y acciones.
     * VistaAjustes: opciones de configuración de usuario.
4. Barra de Estado Dinámica (Status Bar):
   - Muestra mensajes informativos, contador de elementos y reloj en tiempo real mediante .after().
"""

from datetime import datetime
import tkinter as tk
from tkinter import ttk, messagebox


# =====================================================================
# 1. MODELO / CAPA DE DATOS (DATA STORE)
# =====================================================================
class GestorTareasDatos:
    """Gestiona la memoria y lógica de negocio para las tareas."""

    def __init__(self):
        self.tareas = [
            {"id": 1, "titulo": "Aprender fundamentos de Tkinter", "prioridad": "Alta", "completada": True},
            {"id": 2, "titulo": "Dominar los gestores de geometría (pack, grid, place)", "prioridad": "Alta", "completada": True},
            {"id": 3, "titulo": "Construir interfaz moderna con ttk y POO", "prioridad": "Media", "completada": False},
            {"id": 4, "titulo": "Publicar repositorio educativo en GitHub", "prioridad": "Baja", "completada": False},
        ]
        self._siguiente_id = 5

    def obtener_todas(self, filtro="Todas"):
        if filtro == "Pendientes":
            return [t for t in self.tareas if not t["completada"]]
        elif filtro == "Completadas":
            return [t for t in self.tareas if t["completada"]]
        return list(self.tareas)

    def agregar(self, titulo, prioridad):
        tarea = {
            "id": self._siguiente_id,
            "titulo": titulo,
            "prioridad": prioridad,
            "completada": False
        }
        self.tareas.append(tarea)
        self._siguiente_id += 1
        return tarea

    def alternar_estado(self, tarea_id):
        for t in self.tareas:
            if t["id"] == tarea_id:
                t["completada"] = not t["completada"]
                return t
        return None

    def eliminar(self, tarea_id):
        self.tareas = [t for t in self.tareas if t["id"] != tarea_id]

    def metricas(self):
        total = len(self.tareas)
        completadas = sum(1 for t in self.tareas if t["completada"])
        pendientes = total - completadas
        pct = (completadas / total * 100) if total > 0 else 0
        return total, completadas, pendientes, pct


# =====================================================================
# 2. VISTAS MODULARES (FRAMES HEREDADOS)
# =====================================================================
class VistaDashboard(ttk.Frame):
    """Vista de estadísticas y resumen general de la aplicación."""

    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self._construir_ui()

    def _construir_ui(self):
        # Título
        tk.Label(
            self,
            text="Panel de Control (Dashboard)",
            font=("Segoe UI", 16, "bold"),
            fg="#1a237e"
        ).pack(anchor="w", padx=20, pady=(20, 10))

        tk.Label(
            self,
            text="Resumen en tiempo real del progreso de tus objetivos:",
            font=("Segoe UI", 10),
            fg="#616161"
        ).pack(anchor="w", padx=20, pady=(0, 20))

        # Tarjetas de Métricas
        cards_frame = tk.Frame(self)
        cards_frame.pack(fill="x", padx=20, pady=10)

        self.card_total = self._crear_tarjeta(cards_frame, "Total Tareas", "0", "#1976d2", 0)
        self.card_comp = self._crear_tarjeta(cards_frame, "Completadas", "0", "#388e3c", 1)
        self.card_pend = self._crear_tarjeta(cards_frame, "Pendientes", "0", "#f57c00", 2)

        # Barra de progreso general
        prog_frame = tk.LabelFrame(self, text=" Progreso Global ", font=("Segoe UI", 10, "bold"), padx=15, pady=15)
        prog_frame.pack(fill="x", padx=20, pady=25)

        self.lbl_pct = tk.Label(prog_frame, text="0% completado", font=("Segoe UI", 11, "bold"), fg="#2e7d32")
        self.lbl_pct.pack(anchor="w", pady=(0, 5))

        self.bar_progreso = ttk.Progressbar(prog_frame, mode="determinate")
        self.bar_progreso.pack(fill="x", pady=5)

    def _crear_tarjeta(self, parent, titulo, valor_inicial, color, col_index):
        card = tk.Frame(parent, bg=color, padx=20, pady=15, relief="raised", bd=1)
        card.grid(row=0, column=col_index, sticky="nsew", padx=6)
        parent.grid_columnconfigure(col_index, weight=1)

        tk.Label(card, text=titulo, font=("Segoe UI", 10, "bold"), bg=color, fg="white").pack(anchor="w")
        lbl_val = tk.Label(card, text=valor_inicial, font=("Segoe UI", 24, "bold"), bg=color, fg="white")
        lbl_val.pack(anchor="e", pady=(5, 0))
        return lbl_val

    def actualizar(self):
        """Refresca las tarjetas y la barra de progreso."""
        total, completadas, pendientes, pct = self.controller.datos.metricas()
        self.card_total.config(text=str(total))
        self.card_comp.config(text=str(completadas))
        self.card_pend.config(text=str(pendientes))
        self.lbl_pct.config(text=f"{pct:.1f}% del total completado")
        self.bar_progreso["value"] = pct


class VistaTareas(ttk.Frame):
    """Vista de gestión de tareas con operaciones CRUD completas."""

    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self._construir_ui()

    def _construir_ui(self):
        # Encabezado con barra de creación rápida
        f_top = tk.Frame(self, padx=15, pady=10)
        f_top.pack(fill="x")

        tk.Label(f_top, text="Nueva Tarea:", font=("Segoe UI", 9, "bold")).pack(side="left", padx=(0, 6))
        self.entry_nueva = ttk.Entry(f_top, width=35)
        self.entry_nueva.pack(side="left", padx=4)
        self.entry_nueva.bind("<Return>", lambda e: self._agregar_tarea())

        tk.Label(f_top, text="Prioridad:").pack(side="left", padx=(10, 4))
        self.combo_prio = ttk.Combobox(f_top, values=["Alta", "Media", "Baja"], state="readonly", width=8)
        self.combo_prio.set("Media")
        self.combo_prio.pack(side="left", padx=4)

        ttk.Button(f_top, text="Agregar", command=self._agregar_tarea).pack(side="left", padx=8)

        # Filtro
        f_filtro = tk.Frame(self, padx=15, pady=4)
        f_filtro.pack(fill="x")

        tk.Label(f_filtro, text="Filtrar por:").pack(side="left", padx=(0, 6))
        self.filtro_var = tk.StringVar(value="Todas")
        for f in ["Todas", "Pendientes", "Completadas"]:
            ttk.Radiobutton(f_filtro, text=f, value=f, variable=self.filtro_var, command=self.actualizar).pack(side="left", padx=4)

        # Tabla Treeview
        f_tree = tk.Frame(self, padx=15, pady=6)
        f_tree.pack(fill="both", expand=True)

        cols = ("id", "titulo", "prioridad", "estado")
        self.tree = ttk.Treeview(f_tree, columns=cols, show="headings", selectmode="browse")
        self.tree.heading("id", text="ID")
        self.tree.heading("titulo", text="Título de la Tarea")
        self.tree.heading("prioridad", text="Prioridad")
        self.tree.heading("estado", text="Estado")

        self.tree.column("id", width=45, anchor="center")
        self.tree.column("titulo", width=340, anchor="w")
        self.tree.column("prioridad", width=90, anchor="center")
        self.tree.column("estado", width=110, anchor="center")

        scroll = ttk.Scrollbar(f_tree, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scroll.set)

        self.tree.pack(side="left", fill="both", expand=True)
        scroll.pack(side="right", fill="y")

        # Botones de acción inferiores
        f_acciones = tk.Frame(self, padx=15, pady=8)
        f_acciones.pack(fill="x")

        ttk.Button(f_acciones, text="Alternar Estado (Hecho/Pendiente)", command=self._alternar_tarea).pack(side="left", padx=4)
        ttk.Button(f_acciones, text="Eliminar Tarea", command=self._eliminar_tarea).pack(side="left", padx=4)

    def _agregar_tarea(self):
        txt = self.entry_nueva.get().strip()
        if not txt:
            messagebox.showwarning("Campo Vacío", "Por favor ingresa un título para la tarea.")
            return
        prio = self.combo_prio.get()
        self.controller.datos.agregar(txt, prio)
        self.entry_nueva.delete(0, tk.END)
        self.actualizar()
        self.controller.establecer_estado(f"Tarea añadida: '{txt}'")

    def _alternar_tarea(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("Selección Requerida", "Selecciona una tarea de la lista.")
            return
        item = self.tree.item(sel[0])
        tarea_id = item["values"][0]
        tarea = self.controller.datos.alternar_estado(tarea_id)
        self.actualizar()
        if tarea:
            estado_txt = "completada" if tarea["completada"] else "marcada como pendiente"
            self.controller.establecer_estado(f"Tarea #{tarea_id} {estado_txt}.")

    def _eliminar_tarea(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("Selección Requerida", "Selecciona una tarea de la lista.")
            return
        item = self.tree.item(sel[0])
        tarea_id = item["values"][0]
        if messagebox.askyesno("Confirmar", f"¿Deseas eliminar la tarea #{tarea_id}?"):
            self.controller.datos.eliminar(tarea_id)
            self.actualizar()
            self.controller.establecer_estado(f"Tarea #{tarea_id} eliminada.")

    def actualizar(self):
        """Puebla el Treeview con la lista filtrada."""
        for item in self.tree.get_children():
            self.tree.delete(item)

        filtro = self.filtro_var.get()
        tareas = self.controller.datos.obtener_todas(filtro)
        for t in tareas:
            estado_label = "✔ Hecha" if t["completada"] else "⏳ Pendiente"
            self.tree.insert("", "end", values=(t["id"], t["titulo"], t["prioridad"], estado_label))


class VistaAjustes(ttk.Frame):
    """Vista de configuración y créditos del sistema."""

    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self._construir_ui()

    def _construir_ui(self):
        tk.Label(
            self,
            text="Ajustes y Arquitectura de la Aplicación",
            font=("Segoe UI", 16, "bold"),
            fg="#1a237e"
        ).pack(anchor="w", padx=20, pady=(20, 10))

        info_box = tk.Label(
            self,
            text=(
                "Principios de Diseño aplicados en este módulo:\n\n"
                "1. Encapsulamiento en Clases:\n"
                "   Toda la interfaz y lógica se modela en clases independientes, evitando variables globales.\n\n"
                "2. Jerarquía de Vistas (ttk.Frame):\n"
                "   Cada pantalla hereda de Frame y se gestiona en un contenedor principal con .tkraise().\n\n"
                "3. Inversión y Paso de Dependencias:\n"
                "   Cada vista recibe la referencia a 'controller', permitiendo comunicarse con la barra de\n"
                "   estado y el modelo sin acoplamientos rígidos.\n\n"
                "4. Gestión Segura de Ciclo de Vida:\n"
                "   Protocolo WM_DELETE_WINDOW para confirmación y limpieza antes de cerrar."
            ),
            font=("Segoe UI", 10),
            bg="#f1f3f4",
            relief="groove",
            justify="left",
            padx=16,
            pady=16
        )
        info_box.pack(fill="x", padx=20, pady=10)


# =====================================================================
# 3. VENTANA PRINCIPAL / CONTROLADOR (APLICACIÓN POO)
# =====================================================================
class AppGestorTareas(tk.Tk):
    """Controlador principal de la aplicación. Administra el ciclo de vida, navegación y barra de estado."""

    def __init__(self):
        super().__init__()
        self.title("08 - Arquitectura POO y Navegación Multivista")
        self.geometry("900x640")
        self.minsize(800, 560)

        # Capa de datos compartida
        self.datos = GestorTareasDatos()

        # Interceptación de protocolo de cierre de ventana
        self.protocol("WM_DELETE_WINDOW", self.al_cerrar)

        self._crear_layout_base()
        self._inicializar_vistas()
        self._iniciar_reloj_statusbar()

        # Mostrar vista inicial
        self.mostrar_vista("VistaDashboard")

    def _crear_layout_base(self):
        # 1. Barra de Navegación Lateral (Sidebar)
        self.sidebar = tk.Frame(self, bg="#1e293b", width=200)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        # Título en Sidebar
        tk.Label(
            self.sidebar,
            text="TASKFLOW",
            font=("Segoe UI", 13, "bold"),
            bg="#1e293b",
            fg="#38bdf8",
            pady=15
        ).pack(fill="x")

        # Botones de navegación
        self.botones_nav = {}
        items_nav = [
            ("VistaDashboard", "📊 Dashboard"),
            ("VistaTareas", "📝 Mis Tareas"),
            ("VistaAjustes", "⚙ Ajustes"),
        ]

        for vista_key, label in items_nav:
            btn = tk.Button(
                self.sidebar,
                text=label,
                font=("Segoe UI", 10),
                bg="#1e293b",
                fg="#e2e8f0",
                activebackground="#334155",
                activeforeground="white",
                bd=0,
                padx=16,
                pady=10,
                anchor="w",
                cursor="hand2",
                command=lambda v=vista_key: self.mostrar_vista(v)
            )
            btn.pack(fill="x", pady=2)
            self.botones_nav[vista_key] = btn

        # Botón Salir en la base del Sidebar
        btn_salir = tk.Button(
            self.sidebar,
            text="🚪 Salir",
            font=("Segoe UI", 9),
            bg="#0f172a",
            fg="#94a3b8",
            activebackground="#dc2626",
            activeforeground="white",
            bd=0,
            pady=8,
            cursor="hand2",
            command=self.al_cerrar
        )
        btn_salir.pack(side="bottom", fill="x", pady=10, padx=10)

        # 2. Barra de Estado Inferior (Status Bar)
        self.statusbar = tk.Frame(self, bg="#e2e8f0", height=26, relief="sunken", bd=1)
        self.statusbar.pack(side="bottom", fill="x")

        self.lbl_status = tk.Label(
            self.statusbar,
            text="Sistema iniciado correctamente.",
            font=("Segoe UI", 8),
            bg="#e2e8f0",
            fg="#334155"
        )
        self.lbl_status.pack(side="left", padx=10)

        self.lbl_reloj = tk.Label(
            self.statusbar,
            text="",
            font=("Segoe UI", 8, "bold"),
            bg="#e2e8f0",
            fg="#334155"
        )
        self.lbl_reloj.pack(side="right", padx=10)

        # 3. Contenedor de Pantallas Dinámicas
        self.container = ttk.Frame(self)
        self.container.pack(side="right", fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

    def _inicializar_vistas(self):
        """Instancia y apila las distintas vistas en el contenedor central."""
        self.vistas = {}
        for ClsVista in (VistaDashboard, VistaTareas, VistaAjustes):
            nombre = ClsVista.__name__
            frame = ClsVista(parent=self.container, controller=self)
            self.vistas[nombre] = frame
            # Apilar cada vista en la misma celda de la rejilla
            frame.grid(row=0, column=0, sticky="nsew")

    def mostrar_vista(self, nombre_vista):
        """Eleva a primer plano la vista seleccionada y resalta su botón."""
        frame = self.vistas.get(nombre_vista)
        if frame:
            if hasattr(frame, "actualizar"):
                frame.actualizar()
            frame.tkraise()

            # Actualizar estilos visuales del menú lateral
            for key, btn in self.botones_nav.items():
                if key == nombre_vista:
                    btn.config(bg="#334155", fg="#38bdf8", font=("Segoe UI", 10, "bold"))
                else:
                    btn.config(bg="#1e293b", fg="#e2e8f0", font=("Segoe UI", 10))

            self.establecer_estado(f"Vista activa: {nombre_vista.replace('Vista', '')}")

    def establecer_estado(self, mensaje):
        """Actualiza el texto informativo en la barra inferior."""
        self.lbl_status.config(text=mensaje)

    def _iniciar_reloj_statusbar(self):
        """Actualiza el reloj en tiempo real mediante .after()."""
        ahora = datetime.now().strftime("%Y-%m-%d  %H:%M:%S")
        self.lbl_reloj.config(text=ahora)
        self.after(1000, self._iniciar_reloj_statusbar)

    def al_cerrar(self):
        """Manejador seguro de salida de la aplicación."""
        if messagebox.askokcancel("Salir de TaskFlow", "¿Seguro que deseas cerrar la aplicación?"):
            self.destroy()


def main():
    app = AppGestorTareas()
    app.mainloop()


if __name__ == "__main__":
    main()
