import tkinter as tk
from tkinter import messagebox
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





class QuizGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Quiz Game")
        self.usuario = None
        self.nivel = 1
        self.puntaje = 0
        self.vidas = 3  # Nuevas 3 oportunidades para el jugador
        self.respuesta_seleccionada = None  # Mantener la respuesta seleccionada
        self.root.bind('<Return>', self.procesar_enter)  # Vincular la tecla Enter con el evento

        # Pantalla principal
        self.main_menu()

    def main_menu(self):
        self.clear_window()

        tk.Label(self.root, text="Bienvenido al Quiz Game", font=("Arial", 18)).pack(pady=20)
        tk.Button(self.root, text="Nuevo Juego", command=self.nuevo_juego).pack(pady=10)
        tk.Button(self.root, text="Instrucciones", command=self.mostrar_instrucciones).pack(pady=10)
        tk.Button(self.root, text="Ver Puntaje", command=self.mostrar_puntaje).pack(pady=10)

    def nuevo_juego(self):
        self.clear_window()

        tk.Label(self.root, text="Ingresa tu nombre:", font=("Arial", 14)).pack(pady=10)
        self.nombre_entry = tk.Entry(self.root)
        self.nombre_entry.pack(pady=10)
        tk.Button(self.root, text="Comenzar", command=self.comenzar_juego).pack(pady=10)

    def comenzar_juego(self):
        nombre = self.nombre_entry.get()
        if nombre:
            self.usuario = nombre
            self.nivel = 1
            self.puntaje = 0
            self.vidas = 3  # Reiniciar las vidas a 3
            self.respuesta_seleccionada = None  # Reiniciar la respuesta seleccionada

            # Insertar nuevo usuario en la base de datos
            cursor.execute("INSERT INTO usuarios (nombre, nivel, puntaje) VALUES (?, ?, ?)",
                           (self.usuario, self.nivel, self.puntaje))
            conn.commit()

            self.jugar_nivel()
        else:
            messagebox.showwarning("Error", "Por favor ingresa un nombre")

    def jugar_nivel(self):
        self.clear_window()

        # Verificar si el jugador tiene vidas restantes
        if self.vidas == 0:
            messagebox.showinfo("Juego Terminado",
                                f"¡Lo siento {self.usuario}, has perdido todas tus vidas!\nPuntaje final: {self.puntaje}")
            self.main_menu()
            return

        # Seleccionar una pregunta aleatoria
        pregunta_data = self.seleccionar_pregunta()
        self.pregunta_actual = pregunta_data["pregunta"]
        self.opciones = pregunta_data["opciones"]
        self.respuesta_correcta = pregunta_data["respuesta"]

        # Mostrar la pregunta y vidas restantes
        tk.Label(self.root, text=f"Nivel {self.nivel}", font=("Arial", 14)).pack(pady=10)
        tk.Label(self.root, text=f"Vidas restantes: {self.vidas}", font=("Arial", 12), fg="red").pack(pady=5)
        tk.Label(self.root, text=self.pregunta_actual, font=("Arial", 14)).pack(pady=10)

        # Mostrar opciones
        for opcion in self.opciones:
            tk.Button(self.root, text=opcion, command=lambda o=opcion: self.seleccionar_respuesta(o)).pack(pady=5)

    def seleccionar_pregunta(self):
        """Seleccionar una pregunta aleatoria (puede repetirse)"""
        return random.choice(PREGUNTAS)

    def seleccionar_respuesta(self, respuesta):
        """Guardar la respuesta seleccionada"""
        self.respuesta_seleccionada = respuesta

    def procesar_enter(self, event):
        """Procesar la tecla Enter para verificar la respuesta seleccionada y avanzar"""
        if self.respuesta_seleccionada:  # Solo procesar si se seleccionó una respuesta
            self.verificar_respuesta(self.respuesta_seleccionada)
            self.respuesta_seleccionada = None  # Resetear la respuesta seleccionada para la siguiente pregunta

    def verificar_respuesta(self, respuesta):
        if respuesta == self.respuesta_correcta:
            self.puntaje += 10
            messagebox.showinfo("Correcto", "¡Respuesta correcta!")
        else:
            self.vidas -= 1  # Descontar una vida si la respuesta es incorrecta
            messagebox.showinfo("Incorrecto", f"Respuesta incorrecta. Te quedan {self.vidas} vidas.")

        # Actualizar nivel y puntaje en la base de datos
        self.nivel += 1
        cursor.execute("UPDATE usuarios SET nivel = ?, puntaje = ? WHERE nombre = ?",
                       (self.nivel, self.puntaje, self.usuario))
        conn.commit()

        # Jugar el siguiente nivel
        self.jugar_nivel()

    def mostrar_instrucciones(self):
        messagebox.showinfo("Instrucciones",
                            "Responde correctamente las preguntas para avanzar de nivel y ganar puntos.\nTienes 3 vidas. Si pierdes todas, el juego terminará.\nSelecciona una opción y presiona Enter para continuar.")

    def mostrar_puntaje(self):
        if self.usuario:
            messagebox.showinfo("Puntaje",
                                f"Usuario: {self.usuario}\nNivel: {self.nivel}\nPuntaje: {self.puntaje}\nVidas restantes: {self.vidas}")
        else:
            messagebox.showinfo("Puntaje", "No se ha comenzado un juego.")

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()


# Configurar la ventana
root = tk.Tk()
app = QuizGame(root)
root.mainloop()

# Cerrar la conexión a la base de datos
conn.close()

