import tkinter as tk
from tkinter import messagebox
import random
import json
import time

# Palabras por categoría
palabras = {
    "Billie eilish": ["birds of a feather", "lovely", "badguy", "oceaneyes","happierthanever"],
    "Lana del rey": ["youngandbeautiful", "borntodie", "lovesong","cinnamongirl", "summertimesadness "],
    "Taylor swift": ["cardigan", "alltoowell", "daylight", "enchanted", "thegreatwar "],
    "Olivia Rodigro": [" can't catch me now", "dejavu", "traitor", "driverslicense","jealousyjealousy"],
    "Adele": [" skyfall", " setfiretotherain", "someonelikeyou", "adelerollinginthedeep","hello"],

}

archivo_usuarios = "usuarios.json"


# Función para cargar datos del usuario
def cargar_datos_usuario(nombre):
    try:
        with open(archivo_usuarios, 'r') as f:
            datos = json.load(f)
            return datos.get(nombre, {"nivel": 1, "puntaje_total": 0})
    except FileNotFoundError:
        return {"nivel": 1, "puntaje_total": 0}


# Función para guardar datos del usuario
def guardar_datos_usuario(nombre, datos):
    try:
        with open(archivo_usuarios, 'r') as f:
            usuarios = json.load(f)
    except FileNotFoundError:
        usuarios = {}

    usuarios[nombre] = datos
    with open(archivo_usuarios, 'w') as f:
        json.dump(usuarios, f)


# Clase del juego
class JuegoAhorcado:
    def __init__(self, root):
        self.root = root
        self.root.title("Juego de Ahorcado")
        self.nivel_actual = 1
        self.intentos_restantes = 5
        self.puntaje_total = 0
        self.usuario = ""
        self.palabra_actual = ""
        self.categoria_actual = ""
        self.tiempo_restante = 60  # 60 segundos para el temporizador

        self.nombre_usuario = tk.StringVar()

        self.frame_inicio()

    # Pantalla de inicio
    def frame_inicio(self):
        self.limpiar_pantalla()

        tk.Label(self.root, text="Bienvenido al Juego de Ahorcado").pack(pady=10)
        tk.Label(self.root, text="Introduce tu nombre:").pack()
        tk.Entry(self.root, textvariable=self.nombre_usuario).pack()

        tk.Button(self.root, text="Comenzar Juego", command=self.comenzar_juego).pack(pady=10)
        tk.Button(self.root, text="Instrucciones", command=self.mostrar_instrucciones).pack()
        tk.Button(self.root, text="Ver Puntajes", command=self.mostrar_puntajes).pack()
        tk.Button(self.root, text="Ver Usuarios", command=self.mostrar_usuarios).pack()  # Nuevo botón para ver usuarios

    # Instrucciones del juego
    def mostrar_instrucciones(self):
        instrucciones = """
        Instrucciones del Juego:
        1. Tienes 4 intentos para adivinar la palabra.
        2. Cada palabra pertenece a una categoría: estrategia, matemáticas, habilidad, adivinación, laberinto o memoria.
        3. Tienes 1 minuto para adivinar la palabra.
        4. Si fallas, pierdes el nivel.
        """
        messagebox.showinfo("Instrucciones", instrucciones)

    # Mostrar los puntajes
    def mostrar_puntajes(self):
        datos = cargar_datos_usuario(self.nombre_usuario.get())
        puntaje_info = f"Puntaje Total: {datos['puntaje_total']}\nNivel Superado: {datos['nivel']}"
        messagebox.showinfo("Puntajes", puntaje_info)

    # Mostrar usuarios y sus puntajes
    def mostrar_usuarios(self):
        try:
            with open(archivo_usuarios, 'r') as f:
                usuarios = json.load(f)

            lista_usuarios = "Usuarios y sus puntajes:\n\n"
            for nombre, datos in usuarios.items():
                lista_usuarios += f"Nombre: {nombre}, Nivel: {datos['nivel']}, Puntaje Total: {datos['puntaje_total']}\n"

            messagebox.showinfo("Usuarios", lista_usuarios)
        except FileNotFoundError:
            messagebox.showinfo("Usuarios", "No hay usuarios registrados.")

    # Comenzar juego
    def comenzar_juego(self):
        self.usuario = self.nombre_usuario.get()
        if not self.usuario:
            messagebox.showwarning("Error", "Por favor introduce tu nombre.")
            return

        datos_usuario = cargar_datos_usuario(self.usuario)
        self.nivel_actual = datos_usuario["nivel"]
        self.puntaje_total = datos_usuario["puntaje_total"]

        self.nueva_partida()

    # Iniciar nueva partida
    def nueva_partida(self):
        self.intentos_restantes = 4
        self.tiempo_restante = 60  # Reiniciar el tiempo
        categorias = list(palabras.keys())
        self.categoria_actual = categorias[self.nivel_actual % len(categorias)]
        self.palabra_actual = random.choice(palabras[self.categoria_actual])
        self.palabra_oculta = ["_"] * len(self.palabra_actual)

        self.frame_juego()

    # Pantalla de juego
    def frame_juego(self):
        self.limpiar_pantalla()

        tk.Label(self.root, text=f"Categoría: {self.categoria_actual}").pack(pady=10)
        self.label_palabra = tk.Label(self.root, text=" ".join(self.palabra_oculta))
        self.label_palabra.pack(pady=10)

        self.letra = tk.StringVar()
        entrada = tk.Entry(self.root, textvariable=self.letra)
        entrada.pack()

        tk.Button(self.root, text="Adivinar Letra", command=self.adivinar_letra).pack(pady=10)

        # Enlazar la tecla Enter para que llame a la función adivinar_letra
        self.root.bind('<Return>', lambda event: self.adivinar_letra())

        self.label_intentos = tk.Label(self.root, text=f"Intentos Restantes: {self.intentos_restantes}")
        self.label_intentos.pack(pady=10)

        # Mostrar tiempo restante
        self.label_tiempo = tk.Label(self.root, text=f"Tiempo Restante: {self.tiempo_restante} segundos")
        self.label_tiempo.pack(pady=10)

        self.actualizar_tiempo()  # Iniciar el temporizador

    # Actualizar tiempo
    def actualizar_tiempo(self):
        if self.tiempo_restante > 0:
            self.tiempo_restante -= 1
            self.label_tiempo.config(text=f"Tiempo Restante: {self.tiempo_restante} segundos")
            self.root.after(1000, self.actualizar_tiempo)  # Actualizar cada segundo
        else:
            self.tiempo_agotado()

    # Adivinar letra
    def adivinar_letra(self):
        letra = self.letra.get().lower()
        self.letra.set("")  # Limpiar entrada

        if letra in self.palabra_actual:
            for i, l in enumerate(self.palabra_actual):
                if l == letra:
                    self.palabra_oculta[i] = letra
            self.label_palabra.config(text=" ".join(self.palabra_oculta))
        else:
            self.intentos_restantes -= 1
            self.label_intentos.config(text=f"Intentos Restantes: {self.intentos_restantes}")

        if "_" not in self.palabra_oculta:
            self.nivel_superado()
        elif self.intentos_restantes == 0:
            self.fin_partida("Perdiste el nivel.")

    # Nivel superado
    def nivel_superado(self):
        self.puntaje_total += 100  # Ejemplo de puntaje
        self.nivel_actual += 1
        guardar_datos_usuario(self.usuario, {"nivel": self.nivel_actual, "puntaje_total": self.puntaje_total})
        self.fin_partida(f"¡Ganaste el nivel! Puntaje obtenido: {self.puntaje_total}")

    # Fin de la partida
    def fin_partida(self, mensaje):
        messagebox.showinfo("Resultado", mensaje)
        self.mostrar_resumen_final()  # Mostrar resumen final
        self.nueva_partida()

    # Mostrar resumen final
    def mostrar_resumen_final(self):
        resumen = f"Nivel alcanzado: {self.nivel_actual - 1}\nPuntaje total: {self.puntaje_total}"
        messagebox.showinfo("Resumen Final", resumen)

    # Manejar tiempo agotado
    def tiempo_agotado(self):
        if "_" in self.palabra_oculta:
            self.fin_partida("Tiempo agotado. Perdiste el nivel.")

    # Limpiar pantalla
    def limpiar_pantalla(self):
        for widget in self.root.winfo_children():
            widget.destroy()


# Configuración de la aplicación
if __name__ == "__main__":
    root = tk.Tk()
    app = JuegoAhorcado(root)
    root.mainloop()