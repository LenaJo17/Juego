import tkinter as tk
from tkinter import messagebox, simpledialog, Menu
import random
import sqlite3

# Conexión a la base de datos
conn = sqlite3.connect('quiz_game.db')
cursor = conn.cursor()

# Crear tabla si no existe
cursor.execute('''CREATE TABLE IF NOT EXISTS usuarios (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nombre TEXT,
                    nivel INTEGER,
                    puntaje INTEGER)''')

# Preguntas de ejemplo
PREGUNTAS = [
    {"pregunta": "¿Cuál es la capital de Francia?", "opciones": ["Madrid", "París", "Roma", "Berlín"],
     "respuesta": "París"},
    {"pregunta": "¿Cuál es el animal más rápido?", "opciones": ["Tigre", "Guepardo", "León", "Águila"],
     "respuesta": "Guepardo"},
    {"pregunta": "¿Cuánto es 7 * 8?", "opciones": ["54", "56", "49", "64"], "respuesta": "56"},
    {"pregunta": "¿Quién pintó La Última Cena?", "opciones": ["Picasso", "Van Gogh", "Da Vinci", "Monet"],
     "respuesta": "Da Vinci"},
    {"pregunta": "¿Qué planeta es conocido como el planeta rojo?", "opciones": ["Marte", "Júpiter", "Saturno", "Venus"],
     "respuesta": "Marte"},
    {"pregunta": "¿Dónde originaron los juegos olímpicos?", "opciones": ["Grecia", "Roma", "Egipto", "China"],
     "respuesta": "Grecia"},
    {"pregunta": "¿Qué tipo de animal es la ballena?", "opciones": ["Reptil", "Pájaro", "Mamífero", "Pez"],
     "respuesta": "Mamífero"},
    {"pregunta": "¿De qué colores es la bandera de México?",
     "opciones": ["Rojo, Verde, Blanco", "Rojo, Azul, Blanco", "Verde, Amarillo, Rojo", "Blanco, Azul, Verde"],
     "respuesta": "Rojo, Verde, Blanco"},
    {"pregunta": "¿Cuántos huesos tiene un adulto?", "opciones": ["206", "300", "180", "250"], "respuesta": "206"},
    {"pregunta": "¿Cuándo acabó la II Guerra Mundial?", "opciones": ["1945", "1944", "1950", "1939"],
     "respuesta": "1945"},
    {"pregunta": "¿Quién es el autor de El Quijote?", "opciones": ["Cervantes", "Shakespeare", "Dante", "Hemingway"],
     "respuesta": "Cervantes"},
    {"pregunta": "¿En qué país se encuentra la Torre de Pisa?", "opciones": ["Italia", "Francia", "España", "Grecia"],
     "respuesta": "Italia"},
    {"pregunta": "¿Qué son los humanos: omnívoros, herbívoros o carnívoros?",
     "opciones": ["Omnívoros", "Herbívoros", "Carnívoros", "Ninguno"], "respuesta": "Omnívoros"},
    {"pregunta": "¿Cuál es el océano más grande?", "opciones": ["Atlántico", "Índico", "Pacífico", "Ártico"],
     "respuesta": "Pacífico"},
    {"pregunta": "¿Qué año llegó Cristóbal Colón a América?", "opciones": ["1492", "1500", "1485", "1510"],
     "respuesta": "1492"},
    {"pregunta": "¿En qué año llegó el ser humano a la Luna?", "opciones": ["1968", "1969", "1970", "1971"],
     "respuesta": "1969"},
    {"pregunta": "¿En qué año se produjeron los atentados sobre las Torres Gemelas de Nueva York?",
     "opciones": ["1999", "2001", "2003", "2005"], "respuesta": "2001"},
    {"pregunta": "¿En qué año se inicia la Revolución Rusa?", "opciones": ["1916", "1917", "1918", "1919"],
     "respuesta": "1917"},
    {"pregunta": "¿Cuál fue el primer presidente democrático de España tras la dictadura franquista?",
     "opciones": ["Felipe González", "Adolfo Suárez", "José María Aznar", "Zapatero"], "respuesta": "Adolfo Suárez"},
    {"pregunta": "¿Cuántos lados tiene un hexágono?", "opciones": ["4", "5", "6", "7"], "respuesta": "6"},
    {"pregunta": "¿Dónde se encuentra la Patagonia?", "opciones": ["Chile", "Argentina", "Uruguay", "Brasil"],
     "respuesta": "Argentina"},
    {"pregunta": "¿En qué año se independizó la India del Imperio Británico?",
     "opciones": ["1945", "1947", "1949", "1950"], "respuesta": "1947"},
    {"pregunta": "¿Quién fue Mohamed Alí?", "opciones": ["Un boxeador", "Un político", "Un científico", "Un artista"],
     "respuesta": "Un boxeador"},
    {"pregunta": "¿En qué año cayó el muro de Berlín?", "opciones": ["1987", "1988", "1989", "1990"],
     "respuesta": "1989"},
    {"pregunta": "¿Cuál es el estado que tiene menos habitantes del mundo?",
     "opciones": ["Mónaco", "Nauru", "Ciudad del Vaticano", "Tuvalu"], "respuesta": "Ciudad del Vaticano"},
    {"pregunta": "¿Cuál es la bandera del mundo con más colores?",
     "opciones": ["Sudáfrica", "Sudán del Sur", "Bélgica", "Italia"], "respuesta": "Sudáfrica"},
    {"pregunta": "¿Cuál es el país de América que tiene mayor población?",
     "opciones": ["Brasil", "México", "Estados Unidos", "Argentina"], "respuesta": "Estados Unidos"},
]


class QuizGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Quiz Game")
        self.usuarios_jugando = []  # Lista para usuarios en partida
        self.usuario = None
        self.nivel = 1
        self.puntaje = 0
        self.vidas = 3
        self.preguntas_contestadas = set()  # Conjunto para índices de preguntas ya mostradas

        self.create_menu()
        self.mostrar_inicio()

    def create_menu(self):
        # Crear menú
        menu = Menu(self.root)
        self.root.config(menu=menu)

        # Menú "Juego"
        juego_menu = Menu(menu)
        menu.add_cascade(label="Juego", menu=juego_menu)
        juego_menu.add_command(label="Nuevo Juego", command=self.nuevo_juego)
        juego_menu.add_command(label="Instrucciones", command=self.mostrar_instrucciones)
        juego_menu.add_command(label="Ver Usuarios", command=self.mostrar_usuarios)
        juego_menu.add_separator()
        juego_menu.add_command(label="Salir", command=self.root.quit)

    def mostrar_inicio(self):
        self.clear_window()

        # Mostrar instrucciones en el inicio
        instrucciones = (
            "Instrucciones:\n"
            "1. Responde las preguntas para avanzar de nivel.\n"
            "2. Por cada respuesta correcta, ganarás 10 puntos.\n"
            "3. Tienes 3 vidas. Cada respuesta incorrecta te resta una vida.\n"
            "4. El juego termina cuando pierdes todas las vidas o contestas todas las preguntas.\n"
            "5. Puedes ver el puntaje y nivel actual de los jugadores en la opción 'Ver Usuarios'."
        )

        tk.Label(self.root, text="Bienvenido al Quiz Game", font=("Arial", 18)).pack(pady=10)
        tk.Label(self.root, text=instrucciones, font=("Arial", 12), justify="left").pack(pady=10)
        tk.Button(self.root, text="Presiona Enter para comenzar", command=self.nuevo_juego).pack(pady=10)

        # Mostrar puntaje y usuarios actuales
        if self.usuarios_jugando:
            usuarios_info = "\n".join(
                [f"{u['nombre']} - Nivel: {u['nivel']} - Puntaje: {u['puntaje']}" for u in self.usuarios_jugando])
            tk.Label(self.root, text="Usuarios Jugando Actualmente:", font=("Arial", 14)).pack(pady=10)
            tk.Label(self.root, text=usuarios_info, font=("Arial", 12), justify="left").pack(pady=10)
        else:
            tk.Label(self.root, text="No hay usuarios jugando actualmente.", font=("Arial", 12)).pack(pady=10)

        # Vincular tecla Enter al botón "Nuevo Juego"
        self.root.bind('<Return>', lambda event: self.nuevo_juego())

    def nuevo_juego(self):
        nombre = simpledialog.askstring("Nombre del Jugador", "Ingresa tu nombre:")
        if not nombre:
            messagebox.showwarning("Advertencia", "Por favor, ingresa un nombre.")
            return

        self.usuario = nombre
        self.nivel = 1
        self.puntaje = 0
        self.vidas = 3
        self.preguntas_contestadas.clear()  # Reiniciar preguntas contestadas

        # Agregar usuario a la lista de jugadores
        self.usuarios_jugando.append({"nombre": self.usuario, "nivel": self.nivel, "puntaje": self.puntaje})

        self.jugar_nivel()

    def jugar_nivel(self):
        self.clear_window()

        if self.vidas <= 0:
            messagebox.showinfo("Juego Terminado",
                                f"¡Lo siento, {self.usuario}! Has perdido. Puntaje final: {self.puntaje}")
            self.mostrar_inicio()
            return

        if len(self.preguntas_contestadas) == len(PREGUNTAS):
            messagebox.showinfo("Juego Terminado",
                                f"¡Felicidades, {self.usuario}! Has respondido todas las preguntas. Puntaje final: {self.puntaje}")
            self.mostrar_inicio()
            return

        # Seleccionar una pregunta aleatoria que no haya sido contestada
        pregunta = random.choice([p for i, p in enumerate(PREGUNTAS) if i not in self.preguntas_contestadas])
        self.preguntas_contestadas.add(PREGUNTAS.index(pregunta))  # Almacenar el índice de la pregunta

        tk.Label(self.root, text=pregunta["pregunta"], font=("Arial", 14)).pack(pady=10)
        for opcion in pregunta["opciones"]:
            tk.Button(self.root, text=opcion,
                      command=lambda opt=opcion, resp=pregunta["respuesta"]: self.verificar_respuesta(opt, resp)).pack(
                pady=5)

        # Mostrar puntaje y nivel actuales
        tk.Label(self.root, text=f"Nivel: {self.nivel} - Puntaje: {self.puntaje} - Vidas: {self.vidas}",
                 font=("Arial", 12)).pack(pady=10)

    def verificar_respuesta(self, opcion, respuesta_correcta):
        if opcion == respuesta_correcta:
            self.puntaje += 10
            messagebox.showinfo("Respuesta Correcta", "¡Respuesta correcta!")
        else:
            self.vidas -= 1
            messagebox.showinfo("Respuesta Incorrecta", "¡Respuesta incorrecta! Pierdes una vida.")

        # Actualizar nivel y puntaje en usuarios jugando
        for usuario in self.usuarios_jugando:
            if usuario['nombre'] == self.usuario:
                usuario['nivel'] = self.nivel
                usuario['puntaje'] = self.puntaje

        # Continuar al siguiente nivel
        self.jugar_nivel()

    def mostrar_instrucciones(self):
        instrucciones = (
            "Instrucciones:\n"
            "1. Responde las preguntas para avanzar de nivel.\n"
            "2. Por cada respuesta correcta, ganarás 10 puntos.\n"
            "3. Tienes 3 vidas. Cada respuesta incorrecta te resta una vida.\n"
            "4. El juego termina cuando pierdes todas las vidas o contestas todas las preguntas.\n"
            "5. Puedes ver el puntaje y nivel actual de los jugadores en la opción 'Ver Usuarios'."
        )
        messagebox.showinfo("Instrucciones", instrucciones)

    def mostrar_usuarios(self):
        if not self.usuarios_jugando:
            messagebox.showinfo("Usuarios Jugando", "Ningún usuario está jugando actualmente.")
        else:
            usuarios_info = "\n".join(
                [f"{u['nombre']} - Nivel: {u['nivel']} - Puntaje: {u['puntaje']}" for u in self.usuarios_jugando])
            messagebox.showinfo("Usuarios Jugando", f"Usuarios jugando actualmente:\n{usuarios_info}")

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()


# Configurar ventana principal
root = tk.Tk()
game = QuizGame(root)
root.mainloop()

# Cerrar conexión a base de datos al finalizar
conn.close()
