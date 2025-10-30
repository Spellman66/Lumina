# Librerias
import os
import json
import random
import tkinter as tk
from datetime import datetime
from transformers import pipeline
from tkinter import scrolledtext
import tkinter as tk
from tkinter import scrolledtext
import customtkinter as ctk

# Configuramos Entorno
os.environ["PYTORCH_ENABLE_MPS_FALLBACK"] = "1"

# Cargamos Modelo
analizador_emocion = pipeline(
    "sentiment-analysis",
    model="UMUTeam/roberta-spanish-sentiment-analysis",
    device=-1
)

# Definimos Diccionario de Respuestas
respuestas = {
    "positive": [
        "Me alegra que compartas algo bueno. Tu luz importa ✨",
        "Qué bonito que te sientas así. Estoy contigo.",
        "Gracias por dejarme ver ese lado tuyo."
    ],
    "negative": [
        "Lamento que te sientas así. Estoy aquí para ti 🤍",
        "No estás solo. Podemos hablar de lo que necesites.",
        "Tu dolor importa. Estoy contigo."
    ],
    "neutral": [
        "Gracias por compartirlo. ¿Quieres que exploremos más?",
        "Estoy aquí si quieres seguir hablando.",
        "Tu presencia ya es valiosa."
    ],
    "crisis": [
        "Respira conmigo. No estás solo. Estoy aquí.",
        "Si estás en peligro, por favor busca ayuda inmediata. ¿Quieres que te muestre recursos?",
        "Tu vida importa. Estoy contigo en este momento."
    ]
}

# Funcion Guardar Entrada Emocional
def guardar_memoria(texto, emocion):
    entrada = {
        "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "texto": texto,
        "emocion": emocion
    }
    try:
        with open("memoria_emocional.json", "r", encoding="utf-8") as f:
            historial = json.load(f)
    except FileNotFoundError:
        historial = []
    historial.append(entrada)
    with open("memoria_emocional.json", "w", encoding="utf-8") as f:
        json.dump(historial, f, indent=2, ensure_ascii=False)

# Mostramos Frase de Anclaje
def mostrar_frase_anclaje():
    try:
        with open("frases_anclaje.json", "r", encoding="utf-8") as f:
            frases = json.load(f)
        if frases:
            return f"“{random.choice(frases)}”"
    except FileNotFoundError:
        return "No tienes frases guardadas aún."

# Mostramos Recursos de Ayuda
def mostrar_recursos():
    try:
        with open("recursos_ayuda.json", "r", encoding="utf-8") as f:
            recursos = json.load(f)
        lista = "\n".join([f"- {r['nombre']}: {r['contacto']} ({r['tipo']})" for r in recursos])
        return f"Aquí hay algunos recursos que podrían ayudarte:\n{lista}"
    except FileNotFoundError:
        return "No se encontraron recursos de ayuda."

# Generamos Respuesta Empática
def generar_respuesta(texto):
    emocion = analizador_emocion(texto)[0]['label'].lower()
    if any(p in texto.lower() for p in [
        "suicidio", "no quiero vivir", "me quiero morir", "ya no puedo",
        "ya no quiero seguir", "quiero desaparecer"
    ]):
        emocion = "crisis"
    guardar_memoria(texto, emocion)
    return random.choice(respuestas.get(emocion, [
        "No estoy seguro de cómo responder, pero estoy contigo."
    ]))

# Procesamos la Entrada
def enviar():
    entrada = campo_texto.get().strip()
    if not entrada:
        return
    chat.insert(tk.END, f"Tú: {entrada}\n", "usuario")
    campo_texto.delete(0, tk.END)

    entrada_lower = entrada.lower()

    if entrada_lower in ["salir", "adiós", "me voy"]:
        frase = mostrar_frase_anclaje()
        cierre = random.choice([
            "Tu existencia tiene valor, incluso en los días oscuros.",
            "No estás solo. Hay luz en ti.",
            "Cada paso que das, incluso el más pequeño, importa."
        ])
        chat.insert(tk.END, f"LUMINA: {frase}\nLUMINA: {cierre}\n", "lumina")
        return

    elif entrada_lower in ["hola", "buenas", "qué onda", "hey", "holi", "buen día", "buenas tardes", "buenas noches"]:
        saludo = random.choice([
            "¡Hola! Qué gusto tenerte aquí 🤍",
            "Hola, estoy contigo. ¿Cómo te sientes hoy?",
            "Buen día. Puedes contarme lo que quieras."
        ])
        chat.insert(tk.END, f"LUMINA: {saludo}\n", "lumina")
        return

    elif entrada_lower in ["estoy en crisis", "ayuda urgente"]:
        recursos = mostrar_recursos()
        chat.insert(tk.END, f"LUMINA: {recursos}\n", "lumina")
        return

    elif entrada_lower.startswith("guardar frase:"):
        nueva_frase = entrada.replace("guardar frase:", "").strip()
        try:
            with open("frases_anclaje.json", "r", encoding="utf-8") as f:
                frases = json.load(f)
        except FileNotFoundError:
            frases = []
        frases.append(nueva_frase)
        with open("frases_anclaje.json", "w", encoding="utf-8") as f:
            json.dump(frases, f, indent=2, ensure_ascii=False)
        chat.insert(tk.END, "LUMINA: Frase guardada para ti 💙", "lumina")
        return

    respuesta = generar_respuesta(entrada)
    chat.insert(tk.END, f"LUMINA: {respuesta}\n", "lumina")
    chat.yview(tk.END)

# Creamos la Interfaz Gráfica
ventana = tk.Tk()
ventana.title("LUMINA — Tu espacio emocional")
ventana.geometry("580x640")
ventana.configure(bg="#c7a5e9") 

encabezado = tk.Label(
    ventana,
    text="🧠 LUMINA — Tu espacio emocional seguro",
    font=("Segoe UI", 20, "bold"),
    bg="#c7a5e9",
    fg="#333333",
    pady=12
)
encabezado.pack()

# Área de Chat
chat_frame = tk.Frame(ventana, bg="#e5d5f0", padx=8, pady=8)
chat_frame.pack(fill=tk.BOTH, expand=True)

chat = scrolledtext.ScrolledText(
    chat_frame,
    wrap=tk.WORD,
    font=("Segoe UI", 14),
    bg="#c7a5e9",
    fg="#000000",
    bd=0,
    relief=tk.FLAT
)
chat.pack(fill=tk.BOTH, expand=True)

# Burbujas de Chat
chat.tag_config("usuario", foreground="#000000", background="#d9fdd3", justify="right", spacing1=2, spacing3=4, lmargin1=50, rmargin=10)
chat.tag_config("lumina", foreground="#000000", background="#e6e6e6", justify="left", spacing1=2, spacing3=4, lmargin1=10, rmargin=50)
chat.tag_config("usuario", foreground="#000000", background="#d9fdd3", justify="right", spacing1=2, spacing3=4, lmargin1=20, rmargin=20)
chat.tag_config("lumina", foreground="#000000", background="#e6e6e6", justify="left", spacing1=2, spacing3=4, lmargin1=20, rmargin=20)

# Campo de Entrada
campo_texto = tk.Entry(
    ventana,
    font=("Segoe UI", 14),
    relief=tk.FLAT,
    bd=0,
    bg="#ffffff",
    fg="#000000"
)
campo_texto.pack(padx=12, pady=(0,10), fill=tk.X)

# Botón Enviar
boton_enviar = tk.Button(
    ventana,
    text="Enviar",
    font=("Segoe UI", 14),
    bg="#007acc",
    fg="black",
    relief=tk.FLAT,
    command=enviar
)
boton_enviar.pack(padx=12, pady=(0,12))

# Mensaje de Bienvenida
chat.insert(tk.END, "🧠 Bienvenido a LUMINA. Puedes hablar conmigo cuando lo necesites.\n", "lumina")

# Ejecutamos la Ventana
ventana.mainloop()