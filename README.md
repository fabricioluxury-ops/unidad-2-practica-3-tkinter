# 🐍 Python Tkinter Showcase & Learning Suite

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg?logo=python&logoColor=white)](https://www.python.org/)
[![GUI](https://img.shields.io/badge/GUI-Tkinter%20%2F%20ttk-green.svg)](https://docs.python.org/3/library/tkinter.html)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey.svg)](#requisitos-e-instalación)

Repositorio educativo y guía de referencia práctica con múltiples archivos de código en **Python**, diseñados paso a paso para explorar y dominar las funcionalidades de la librería estándar de interfaces gráficas **Tkinter** y su subsistema temático moderno **ttk**.

---

## 📋 Tabla de Contenidos

- [Características Principales](#-características-principales)
- [Requisitos e Instalación](#-requisitos-e-instalación)
- [Inicio Rápido y Lanzador Central](#-inicio-rápido-y-lanzador-central)
- [Catálogo Detallado de Archivos y Módulos](#-catálogo-detallado-de-archivos-y-módulos)
  - [01. Hola Mundo y Fundamentos Básicos](#01_hola_mundo_basicopy)
  - [02. Administradores de Geometría](#02_layout_managerspy)
  - [03. Widgets Interactivos y Variables de Control](#03_widgets_interactivospy)
  - [04. Widgets Temáticos Modernos (ttk)](#04_ttk_widgets_modernospy)
  - [05. Sistema de Eventos y Bindings](#05_eventos_y_bindingspy)
  - [06. Menús y Cuadros de Diálogo Estándar](#06_menus_y_dialogospy)
  - [07. Lienzo (Canvas), Gráficos y Animación](#07_lienzo_canvas_y_graficospy)
  - [08. Arquitectura POO y Navegación Multivista](#08_arquitectura_poo_apppy)
  - [Lanzador Gráfico Central (launcher.py)](#launcherpy)
- [Estructura del Proyecto](#-estructura-del-proyecto)
- [Comparativa de Administradores de Geometría](#-comparativa-de-administradores-de-geometría)
- [Buenas Prácticas en Tkinter](#-buenas-prácticas-en-tkinter)
- [Licencia](#-licencia)

---

## ✨ Características Principales

- **Progresión Pedagógica:** Desde un "Hola Mundo" limpio hasta una aplicación SPA de escritorio profesional orientada a objetos (POO).
- **Código Documentado en Español:** Cada archivo contiene docstrings detallados, comentarios en cada bloque de código y variables autoexplicativas.
- **Sin Dependencias Externas:** Todos los scripts funcionan utilizando exclusivamente la biblioteca estándar de Python (`tkinter`, `ttk`, `messagebox`, `filedialog`, `colorchooser`, `simpledialog`).
- **Lanzador Gráfico Integrado (`launcher.py`):** Un panel de control central con buscador para ejecutar y probar cualquiera de los scripts con un solo clic.

---

## ⚙ Requisitos e Instalación

### 1. Python 3.8 o superior
Tkinter viene incluido por defecto en las instalaciones oficiales de Python para **Windows** y **macOS**.

### 2. Verificar la instalación de Tkinter
Puedes verificar que Tkinter está correctamente instalado ejecutando en tu terminal:

```bash
python -m tkinter
```
*(Debería abrirse una pequeña ventana de prueba demostrando que Tkinter funciona).*

> [!NOTE]
> **Usuarios de Linux (Ubuntu/Debian):**
> Si tu distribución no incluye Tkinter por defecto, instálalo con:
> ```bash
> sudo apt-get update
> sudo apt-get install python3-tk
> ```

---

## 🚀 Inicio Rápido y Lanzador Central

Puedes probar cualquiera de los módulos de dos formas:

### Opción A: A través del Lanzador Central Gráfico
Ejecuta el panel interactivo que te permite buscar por tema y lanzar cualquier módulo con un clic:

```bash
python launcher.py
```

### Opción B: Ejecución Individual de Módulos
Puedes ejecutar directamente cualquier archivo específico según el tema que desees estudiar:

```bash
python 01_hola_mundo_basico.py
python 02_layout_managers.py
python 03_widgets_interactivos.py
python 04_ttk_widgets_modernos.py
python 05_eventos_y_bindings.py
python 06_menus_y_dialogos.py
python 07_lienzo_canvas_y_graficos.py
python 08_arquitectura_poo_app.py
```

---

## 📚 Catálogo Detallado de Archivos y Módulos

---

### `01_hola_mundo_basico.py`

#### 🎯 Propósito
Punto de partida ideal para comprender el ciclo de vida esencial de una ventana en Tkinter, la configuración de dimensiones y la interacción básica entre widgets de entrada, botón y etiqueta.

#### 🔑 Conceptos y Widgets Cubiertos
- `tk.Tk()`: Inicialización de la ventana raíz.
- Propiedades de ventana: `title()`, `geometry("500x380")`, `minsize()`, `configure(bg=...)`.
- `tk.Label`: Etiquetas de texto estático y dinámico con personalización de fuente, color de fondo (`bg`) y texto (`fg`).
- `tk.Entry`: Campo de entrada de texto de una sola línea (`.get()`, `.delete()`, `.focus()`).
- `tk.Button`: Botones interactivos asociados a funciones callback mediante el parámetro `command=...`.
- `tk.Frame`: Contenedor para agrupar horizontalmente los botones "Saludar" y "Limpiar".
- `pack(side=..., fill=..., pady=...)`: Empaquetado básico y espaciados.
- `root.mainloop()`: Inicio del bucle despachador de eventos del sistema operativo.

#### 💡 Interacciones para probar
1. Escribe tu nombre en la caja de texto y haz clic en **Saludar** (o presiona la tecla `Enter`).
2. Observa cómo cambia dinámicamente el texto y el color del mensaje de bienvenida.
3. Haz clic en **Limpiar** para vaciar el campo y restaurar el foco.
4. Presiona **Cerrar Ventana** para finalizar de forma segura con `root.destroy()`.

---

### `02_layout_managers.py`

#### 🎯 Propósito
Demostrar y contrastar los **tres administradores de geometría** que ofrece Tkinter (`pack`, `grid` y `place`), explicando cuándo usar cada uno y cómo evitar errores comunes como mezclarlos en el mismo contenedor padre.

#### 🔑 Conceptos y Widgets Cubiertos
- **Pestaña 1: `pack()` (Empaquetador Direccional)**
  - Opciones `side`: `TOP`, `BOTTOM`, `LEFT`, `RIGHT`.
  - Opciones de expansión: `fill="x"`, `fill="y"`, `fill="both"`, `expand=True`.
  - Margen exterior (`padx`, `pady`) e interior (`ipadx`, `ipady`).
- **Pestaña 2: `grid()` (Sistema de Rejilla / Filas y Columnas)**
  - Estructuración tabular: `row`, `column`.
  - Fusión de celdas: `columnspan=2` y `rowspan`.
  - Alineación dentro de la celda: `sticky="w"`, `sticky="ew"`, `sticky="nsew"`.
  - Responsividad: `grid_columnconfigure(1, weight=1)` para permitir que los campos se estiren al redimensionar la ventana.
- **Pestaña 3: `place()` (Posicionamiento Absoluto y Relativo)**
  - Coordenadas absolutas en píxeles: `x=15`, `y=15`, `width=...`, `height=...`.
  - Coordenadas relativas porcentuales: `relx=0.5`, `rely=0.5` (centrado dinámico), `relwidth=0.9`.
  - Puntos de anclaje: `anchor="center"`, `anchor="ne"`.

#### 💡 Interacciones para probar
- Navega entre las tres pestañas y maximiza o cambia el tamaño de la ventana para observar cómo reacciona cada administrador de geometría a los cambios de dimensiones.

---

### `03_widgets_interactivos.py`

#### 🎯 Propósito
Presentar la colección completa de controles de formulario estándar de Tkinter y el mecanismo de **enlace de datos reactivo (Data Binding)** mediante variables de control.

#### 🔑 Conceptos y Widgets Cubiertos
- **Variables de Control de Tkinter:**
  - `tk.StringVar`: Manejo de cadenas de texto vinculadas a campos.
  - `tk.IntVar`: Manejo de números enteros (edad, selecciones numéricas).
  - `tk.BooleanVar`: Manejo de valores booleanos para casillas de verificación.
  - `tk.DoubleVar`: Manejo de números decimales de coma flotante.
  - Métodos `.get()`, `.set()` y observadores reactivos `.trace_add("write", callback)`.
- **Widgets Demostrados:**
  - `tk.Entry` con soporte para contraseña oculta (`show="*"`) y botón para alternar visibilidad.
  - `tk.Radiobutton` agrupados por una misma variable para selección mutuamente excluyente.
  - `tk.Checkbutton` para opciones múltiples independientes.
  - `tk.Scale`: Control deslizante (slider) horizontal con rangos numéricos continuos.
  - `tk.Spinbox`: Selector por incrementos y decrementos discretos.
  - `tk.Text` con `tk.Scrollbar` acoplada bidireccionalmente (`yscrollcommand` y `command=text.yview`).
- **Panel de Estado en Tiempo Real:**
  - Tarjeta de diagnóstico que se actualiza automáticamente cada vez que el usuario mueve un control o escribe una letra.

---

### `04_ttk_widgets_modernos.py`

#### 🎯 Propósito
Explorar el subsistema **ttk (Tk Themed Widgets)**, que provee una apariencia nativa moderna en cada sistema operativo y componentes avanzados que no existen en el Tk clásico.

#### 🔑 Conceptos y Widgets Cubiertos
- `ttk.Style`:
  - Inspección de los temas disponibles en el sistema con `style.theme_names()`.
  - Cambio dinámico de temas en caliente (`style.theme_use(tema)`).
- `ttk.Combobox`:
  - Lista desplegable con opción de solo lectura (`state="readonly"`).
  - Captura del evento de selección de ítem mediante `<<ComboboxSelected>>`.
- `ttk.Progressbar`:
  - **Modo Determinado:** Barra cuantificada con porcentaje de 0% a 100%, avance programático y reinicio.
  - **Modo Indeterminado:** Animación continua de carga ("spinner/busy") para procesos en segundo plano.
- `ttk.Treeview`:
  - Visualización tabular avanzada de datos con columnas configurables (`show="headings"`).
  - Definición de anchos, alineaciones (`center`, `w`, `e`) y nombres de encabezados.
  - Inserción dinámica de filas (`.insert()`), obtención y eliminación del ítem seleccionado (`.selection()`, `.delete()`), y vaciado completo.
  - Barra de desplazamiento vertical (`ttk.Scrollbar`) sincronizada.
- `ttk.Separator`: Divisores estéticos horizontales y verticales.

---

### `05_eventos_y_bindings.py`

#### 🎯 Propósito
Comprender en profundidad el **sistema de despacho y vinculación de eventos** de Tkinter, permitiendo que la interfaz responda a acciones del ratón, combinaciones de teclado y cambios de estado de la ventana.

#### 🔑 Conceptos y Widgets Cubiertos
- Sintaxis general: `widget.bind("<SecuenciaDeEvento>", manejador)`.
- El objeto `event`: inspección de atributos como `event.x`, `event.y`, `event.char`, `event.keysym`, `event.keycode` y `event.widget`.
- **Eventos de Ratón:**
  - `<Button-1>`, `<Button-2>`, `<Button-3>`: Clics izquierdo, central y derecho.
  - `<Double-Button-1>`: Detección de doble clic.
  - `<Motion>`: Seguimiento continuo de las coordenadas del cursor.
  - `<B1-Motion>`: Arrastre continuo manteniendo presionado el botón izquierdo (trazo de puntos).
  - `<Enter>` y `<Leave>`: Efectos de entrada y salida del cursor sobre un widget (*hover*).
- **Eventos de Teclado y Atajos:**
  - `<KeyPress>`: Captura de caracteres ordinarios y teclas especiales (`Return`, `Escape`, etc.).
  - Combinaciones con tecla control: `<Control-s>` (Guardado simulado) y `<Control-l>` (Limpiar consola).
- **Eventos de Ventana y Foco:**
  - `<FocusIn>` y `<FocusOut>`: Detección de activación de controles.
  - `<Configure>`: Detección de redimensionamiento o movimiento de la ventana.
- **Consola de Registro Integrada:**
  - Área tipo terminal en color oscuro que imprime cada evento capturado con marca de tiempo precisa (`HH:MM:SS.mmm`).

---

### `06_menus_y_dialogos.py`

#### 🎯 Propósito
Aprender a implementar estructuras de menús completas (tanto de barra superior como emergentes contextuales) e integrar todos los cuadros de diálogo estándar del sistema operativo.

#### 🔑 Conceptos y Widgets Cubiertos
- `tk.Menu`:
  - Barra de menús superior con `root.config(menu=menubar)`.
  - Menú cascada con aceleradores de teclado (`accelerator="Ctrl+O"`, etc.).
  - Separadores visuales (`add_separator()`).
  - Opciones con estado: `add_checkbutton` (ej. alternar Modo Oscuro) y `add_radiobutton` (ej. selector de zoom).
  - Menú contextual emergente disparado con clic derecho mediante `.post(event.x_root, event.y_root)`.
- `tkinter.messagebox`:
  - Notificaciones: `showinfo()`, `showwarning()`, `showerror()`.
  - Confirmaciones: `askyesno()`, `askokcancel()`, evaluando el retorno booleano `True`/`False`.
- `tkinter.filedialog`:
  - `askopenfilename()`: Selección y lectura de archivos con filtros de extensión.
  - `asksaveasfilename()`: Guardado de contenido en disco con extensión predeterminada.
  - `askdirectory()`: Selección de directorios locales.
- `tkinter.colorchooser`:
  - `askcolor()`: Paleta nativa de selección de color RGB/Hexadecimal para personalizar la interfaz en vivo.
- `tkinter.simpledialog`:
  - `askstring()` y `askinteger()` con validación de rangos numéricos.

---

### `07_lienzo_canvas_y_graficos.py`

#### 🎯 Propósito
Dominar el widget **Canvas**, una de las herramientas más potentes y versátiles de Tkinter para la creación de gráficos vectoriales 2D, pizarras de dibujo interactivas y animaciones con física en tiempo real.

#### 🔑 Conceptos y Widgets Cubiertos
- **Métodos Primitivos de Dibujo Vectorial:**
  - `create_line()`: Segmentos, grosores, extremos redondeados y puntas de flecha.
  - `create_rectangle()`: Figuras cuadrangulares con color de relleno y contorno.
  - `create_oval()`: Circunferencias, óvalos y elipses.
  - `create_polygon()`: Polígonos de vértices múltiples (ejemplo: generación matemática de una estrella de 5 puntas).
  - `create_arc()`: Sectores y arcos circulares para creación de gráficos de pastel.
  - `create_text()`: Renderizado de texto tipográfico vectorial sobre coordenadas exactas.
- **Pizarra de Dibujo Libre:**
  - Captura del trazo continuo uniendo coordenadas sucesivas con `capstyle=tk.ROUND` y `smooth=True`.
  - Selector de grosor de pincel y paleta interactiva de colores.
- **Arrastre de Objetos (Drag & Drop en Canvas):**
  - Asignación de etiquetas (`tags="movible"`).
  - `canvas.find_closest()` y `canvas.move()` para desplazar elementos seleccionados con el ratón.
- **Animación y Física en Tiempo Real:**
  - Bucle de renderizado a ~60 FPS utilizando `root.after(16, bucle)`.
  - Cálculo de colisiones contra los bordes del lienzo (`canvas.coords()`) y rebote mediante inversión de vectores de velocidad (`vel_x`, `vel_y`).
  - Botones de control: Iniciar, Pausar y Reiniciar.

---

### `08_arquitectura_poo_app.py`

#### 🎯 Propósito
Servir como plantilla y modelo de referencia para proyectos de software medianos o grandes. Demuestra cómo estructurar una aplicación en Tkinter aplicando **Programación Orientada a Objetos (POO)**, navegación multivista y desacoplamiento entre datos y vistas.

#### 🔑 Conceptos y Arquitectura Aplicada
- **Clase Principal Controladora (`AppGestorTareas(tk.Tk)`):**
  - Hereda de `tk.Tk`, centralizando la inicialización, la configuración base y el ciclo de vida.
  - Manejo seguro de cierre de ventana interceptando el protocolo `WM_DELETE_WINDOW` con confirmación al usuario.
- **Patrón de Navegación Multivista (Single Page Application para escritorio):**
  - Un contenedor común (`ttk.Frame`) donde se instancian y apilan las distintas vistas en la misma celda de rejilla (`row=0, column=0`).
  - Intercambio instantáneo de pantallas utilizando el método `.tkraise()`.
- **Barra Lateral de Navegación (Sidebar):**
  - Menú lateral moderno con botones que reflejan visualmente la vista activa.
- **Capa de Modelo / Datos Desacoplada (`GestorTareasDatos`):**
  - La lógica de negocio y el almacenamiento en memoria están separados de los widgets gráficos, facilitando pruebas y mantenimiento.
- **Vistas Modulares Implementadas:**
  1. `VistaDashboard`: Tarjetas de estadísticas (Total, Completadas, Pendientes) y barra de progreso calculada en tiempo real.
  2. `VistaTareas`: Interfaz CRUD completa con inserción de nuevas tareas, asignación de prioridades, filtrado dinámico por estado (Todas / Pendientes / Completadas), alternancia de completado y eliminación.
  3. `VistaAjustes`: Panel informativo y de principios arquitectónicos aplicados.
- **Barra de Estado Inferior Dinámica (Status Bar):**
  - Comunicación bidireccional entre vistas y la ventana principal mediante el paso de `controller`.
  - Reloj en vivo con fecha y hora actualizados cada segundo mediante recursión con `.after()`.

---

### `launcher.py`

#### 🎯 Propósito
Panel de control general del repositorio que actúa como índice visual interactivo y lanzador de procesos.

#### 🔑 Características
- **Buscador Reactivo:** Filtra la lista de módulos en tiempo real a medida que escribes palabras clave (por ejemplo: "grid", "canvas", "eventos", "treeview").
- **Ejecución Asíncrona:** Cada script se lanza como un proceso independiente utilizando `subprocess.Popen([sys.executable, script])`, lo que permite abrir múltiples ejemplos simultáneamente sin congelar la interfaz del lanzador.
- **Lienzo con Desplazamiento Suave:** Soporta scroll vertical con la rueda del ratón (`<MouseWheel>`) adaptándose dinámicamente al tamaño de la pantalla.
- **Botón de Apagado Centralizado:** Permite cerrar todas las ventanas hijas abiertas con un solo clic.

---

## 📁 Estructura del Proyecto

```text
Unidad 2. Practica 3/
├── .gitignore                     # Filtros para excluir __pycache__, entornos y temporales
├── LICENSE                        # Licencia de código abierto MIT
├── README.md                      # Documentación completa y detallada del repositorio
├── launcher.py                    # Panel de control gráfico con buscador de módulos
├── 01_hola_mundo_basico.py        # Fundamentos: tk.Tk, Label, Entry, Button, pack()
├── 02_layout_managers.py          # Comparativa de administradores: pack vs grid vs place
├── 03_widgets_interactivos.py     # Controles: StringVar, Checkbutton, Radio, Scale, Spinbox, Text
├── 04_ttk_widgets_modernos.py     # Widgets temáticos: ttk.Style, Combobox, Progressbar, Treeview
├── 05_eventos_y_bindings.py       # Manejo de eventos: bind, ratón, teclado, atajos y consola
├── 06_menus_y_dialogos.py         # Barras de menú, menú contextual, messagebox, filedialog
├── 07_lienzo_canvas_y_graficos.py # Dibujo vectorial, pizarra interactiva y animación 60FPS
└── 08_arquitectura_poo_app.py     # Arquitectura POO, navegación multivista (SPA) y Task CRUD
```

---

## 📊 Comparativa de Administradores de Geometría

| Administrador | Mecanismo | Fortalezas | Casos de Uso Recomendados |
| :--- | :--- | :--- | :--- |
| **`pack()`** | Apilamiento en los bordes (`top`, `bottom`, `left`, `right`) | Muy rápido de implementar; excelente para estructuras lineales. | Barras de herramientas, barras de estado, ventanas sencillas. |
| **`grid()`** | Matriz bidimensional de filas y columnas | Altamente estructurado; soporte responsivo con `columnconfigure(weight=1)`. | **Formularios**, tablas de datos, dashboards y vistas complejas. |
| **`place()`** | Coordenadas explícitas (`x`, `y`, `relx`, `rely`) | Control milimétrico de píxeles y posicionamiento relativo porcentual. | Animaciones, insignias superpuestas, lienzos o elementos flotantes. |

> [!WARNING]
> **Regla de Oro en Tkinter:**
> Nunca utilices `pack()` y `grid()` sobre el **mismo** contenedor padre. Hacerlo causará un bloqueo por conflicto de cálculo geométrico (*geometry manager loop freeze*). Para combinarlos, organiza tus componentes dentro de distintos `Frame`s.

---

## 💡 Buenas Prácticas en Tkinter

1. **Adoptar Programación Orientada a Objetos (POO):**
   Encapsula tus ventanas en clases para evitar el uso excesivo de variables globales y facilitar la modularidad de tu código.
2. **Utilizar `root.after()` para Bucles y Temporizadores:**
   Nunca utilices `time.sleep()` dentro del hilo principal de la interfaz, ya que detiene el bucle de eventos y congelará la ventana. Usa `widget.after(milisegundos, funcion)`.
3. **Manejar el Cierre Seguro de Ventana:**
   Configura siempre `root.protocol("WM_DELETE_WINDOW", callback)` para advertir al usuario sobre cambios sin guardar o liberar recursos antes de salir.
4. **Preferir `ttk` para Diseños Modernos:**
   Siempre que sea posible, utiliza componentes de `tkinter.ttk` (`ttk.Button`, `ttk.Entry`, `ttk.Treeview`) para obtener una apariencia integrada con el tema del sistema operativo.
5. **Separar la Lógica de Negocio de la Vista:**
   Mantén tus estructuras de datos y funciones de cálculo en clases o módulos independientes de los widgets visuales para un código limpio y mantenible.

---

## 📄 Licencia

Este proyecto está bajo la Licencia **MIT**. Consulta el archivo [LICENSE](LICENSE) para más información.
