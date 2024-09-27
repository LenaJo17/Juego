import tkinter as tk
from tkinter import messagebox
import random

# Variables de juego
usuario = ""
nivel = 1
puntaje = 0
respuesta_correcta = 0
oportunidades = 5
tiempo_restante = 45  # Cambiado a 45 segundos
juego_terminado = False  # Bandera para saber si el juego ha terminado
tiempo_agotado_mostrado = False  # Control para mostrar el tiempo agotado solo una vez


# Función para comenzar un nuevo juego
def nuevo_juego(event=None):
    global usuario, nivel, puntaje, oportunidades, tiempo_restante, juego_terminado, tiempo_agotado_mostrado
    usuario = entry_usuario.get()
    if usuario == "":
        messagebox.showwarning("Advertencia", "Por favor, ingresa un nombre de usuario.")
        return

    nivel, puntaje = 1, 0  # Reiniciar nivel y puntaje
    oportunidades = 5
    tiempo_agotado_mostrado = False  # Reiniciar control de tiempo agotado

    messagebox.showinfo("Nuevo Juego", f"Bienvenido {usuario}, comenzaremos en el nivel {nivel} con {puntaje} puntos.")

    root.destroy()  # Cerrar la ventana principal antes de abrir la nueva ventana de preguntas
    crear_ventana_preguntas()


# Función para mostrar instrucciones
def mostrar_instrucciones():
    instrucciones = """
    Instrucciones:
    1. Se te harán preguntas matemáticas en diferentes niveles.
    2. Gana puntos por cada respuesta correcta.
    3. Tienes 5 oportunidades para responder correctamente.
    4. Cada pregunta tiene un límite de tiempo de 45 segundos.
    5. ¡Buena suerte y diviértete!
    """
    messagebox.showinfo("Instrucciones", instrucciones)


# Función para generar y mostrar una pregunta aleatoria
def mostrar_pregunta():
    global respuesta_correcta, lbl_pregunta_ventana, entry_respuesta_ventana, oportunidades, tiempo_restante, lbl_tiempo
    if oportunidades <= 0:
        mostrar_resultados()
        return

    operadores = ['+', '-', '*']
    num1 = random.randint(1, 10 * nivel)
    num2 = random.randint(1, 10 * nivel)
    operador = random.choice(operadores)
    pregunta = f"{num1} {operador} {num2}"
    respuesta_correcta = eval(pregunta)

    lbl_pregunta_ventana.config(text=f"Pregunta: {pregunta}")
    entry_respuesta_ventana.delete(0, tk.END)

    # Reiniciar el temporizador
    global tiempo_restante, tiempo_agotado_mostrado
    tiempo_restante = 45  # Cambiado a 45 segundos
    lbl_tiempo.config(text=f"Tiempo restante: {tiempo_restante} segundos")
    contar_tiempo()  # Iniciar el conteo del temporizador


# Función para verificar la respuesta
def verificar_respuesta(event=None):
    global puntaje, nivel, oportunidades, tiempo_agotado_mostrado
    if juego_terminado:
        return

    try:
        respuesta_usuario = int(entry_respuesta_ventana.get())
        if respuesta_usuario == respuesta_correcta:
            puntaje += 10 * nivel
            messagebox.showinfo("Correcto", "¡Respuesta correcta!")
            nivel += 1
            oportunidades = 5  # Reiniciar oportunidades en cada respuesta correcta
            tiempo_agotado_mostrado = False  # Reiniciar control de tiempo agotado
        else:
            oportunidades -= 1  # Restar una oportunidad
            messagebox.showerror("Incorrecto",
                                 f"Respuesta incorrecta. La respuesta era {respuesta_correcta}. Te quedan {oportunidades} oportunidades.")

        mostrar_pregunta()  # Mostrar la siguiente pregunta
    except ValueError:
        messagebox.showwarning("Error", "Por favor, ingresa un número válido.")


# Función para contar el tiempo
def contar_tiempo():
    global tiempo_restante, tiempo_agotado_mostrado
    if tiempo_restante > 0:
        tiempo_restante -= 1
        lbl_tiempo.config(text=f"Tiempo restante: {tiempo_restante} segundos")
        lbl_tiempo.after(1000, contar_tiempo)  # Llama a esta función de nuevo después de 1000 ms (1 segundo)
    else:
        if not tiempo_agotado_mostrado:  # Verifica si el mensaje ya fue mostrado
            messagebox.showinfo("Tiempo agotado",
                                "Se te ha agotado el tiempo. La respuesta era: " + str(respuesta_correcta))
            tiempo_agotado_mostrado = True  # Marca que se ha mostrado el tiempo agotado
        oportunidades -= 1  # Restar una oportunidad si se agota el tiempo
        mostrar_pregunta()  # Mostrar la siguiente pregunta


# Función para mostrar resultados finales y reiniciar el juego
def mostrar_resultados():
    global juego_terminado
    juego_terminado = True  # Marcar el juego como terminado
    messagebox.showinfo("Fin del juego", f"Fin del juego!\nNivel alcanzado: {nivel}\nPuntaje total: {puntaje}")
    reiniciar_juego()  # Llama a la función para reiniciar el juego


# Función para reiniciar el juego
def reiniciar_juego():
    global usuario, nivel, puntaje, oportunidades, tiempo_restante, juego_terminado, tiempo_agotado_mostrado
    nivel = 1
    puntaje = 0
    oportunidades = 5
    tiempo_restante = 45  # Cambiado a 45 segundos
    juego_terminado = False
    tiempo_agotado_mostrado = False  # Reiniciar control de tiempo agotado
    root.destroy()  # Cerrar la ventana de preguntas
    mostrar_instrucciones()  # Mostrar las instrucciones nuevamente


# Función para mostrar el puntaje actual
def mostrar_puntaje():
    messagebox.showinfo("Puntaje", f"Usuario: {usuario}\nNivel: {nivel}\nPuntaje Total: {puntaje}")


# Función para crear la ventana de preguntas
def crear_ventana_preguntas():
    global lbl_pregunta_ventana, entry_respuesta_ventana, lbl_tiempo

    # Crear la nueva ventana para las preguntas
    ventana_preguntas = tk.Tk()  # La nueva ventana principal será ahora "ventana_preguntas"
    ventana_preguntas.title("Preguntas")
    ventana_preguntas.geometry("300x200")

    lbl_pregunta_ventana = tk.Label(ventana_preguntas, text="Pregunta:")
    lbl_pregunta_ventana.pack(pady=10)

    entry_respuesta_ventana = tk.Entry(ventana_preguntas)
    entry_respuesta_ventana.pack(pady=5)

    btn_verificar = tk.Button(ventana_preguntas, text="Verificar Respuesta", command=verificar_respuesta)
    btn_verificar.pack(pady=10)

    # Vincular la tecla Enter para verificar la respuesta
    entry_respuesta_ventana.bind("<Return>", verificar_respuesta)

    # Etiqueta para mostrar el tiempo restante
    lbl_tiempo = tk.Label(ventana_preguntas, text=f"Tiempo restante: {tiempo_restante} segundos")
    lbl_tiempo.pack(pady=5)

    mostrar_pregunta()  # Muestra la primera pregunta al abrir la ventana

    ventana_preguntas.mainloop()


# Configuración de la ventana principal
root = tk.Tk()
root.title("Juego de Quiz Matemático")
root.geometry("500x400")

# Crear el Frame principal donde estarán las opciones del juego (usuario, nuevo juego, puntaje, instrucciones)
frame_opciones = tk.Frame(root)
frame_opciones.pack(fill="both", expand=True, padx=20, pady=20)

lbl_usuario = tk.Label(frame_opciones, text="Nombre de usuario:")
lbl_usuario.pack(pady=10)
entry_usuario = tk.Entry(frame_opciones)
entry_usuario.pack(pady=5)

btn_nuevo_juego = tk.Button(frame_opciones, text="Comenzar Nuevo Juego", command=nuevo_juego)
btn_nuevo_juego.pack(pady=10)

# Vincular la tecla Enter para comenzar el nuevo juego
entry_usuario.bind("<Return>", nuevo_juego)

btn_instrucciones = tk.Button(frame_opciones, text="Mostrar Instrucciones", command=mostrar_instrucciones)
btn_instrucciones.pack(pady=10)

btn_puntaje = tk.Button(frame_opciones, text="Mostrar Puntaje", command=mostrar_puntaje)
btn_puntaje.pack(pady=10)

root.mainloop()

