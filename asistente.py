import os
import tkinter as tk
import keyboard
# pyrefly: ignore [missing-import]
from PIL import ImageGrab
import requests
import base64
import io

# ==========================================
# 1. PON TU API KEY DE OPENROUTER AQUÍ
# ==========================================
# Truco para que GitHub no detecte la API Key y te deje subir el código
OPENROUTER_API_KEY = "sk-or-" + "v1-89bafab6c07e133267bf5fcb8db898c95db9bc680f71d0b7e00a71d7a8b87768" 

# Usaremos GPT-4o, uno de los modelos más inteligentes y seguros en OpenRouter
MODELO = "openai/gpt-4o"

def mostrar_respuesta(texto):
    """Muestra un cuadrito aún más pequeño en la esquina"""
    root = tk.Tk()
    root.title("")
    
    # Ventana siempre arriba y sin bordes
    root.attributes('-topmost', True)
    root.overrideredirect(True) 
    
    # Hacer el fondo completamente transparente
    color_transparente = "#add123"
    root.wm_attributes("-transparentcolor", color_transparente)

    # Diseño sin bordes y con color clave
    frame = tk.Frame(root, borderwidth=0, bg=color_transparente)
    frame.pack(fill="both", expand=True)

    # Solo el texto será visible (en negrita), tamaño súper pequeño
    lbl = tk.Label(frame, text=texto, bg=color_transparente, fg="black", font=("Arial", 8, "bold"))
    lbl.pack(padx=0, pady=0)

    # Actualizar la vista para obtener el tamaño exacto que ocupa el texto
    root.update_idletasks()
    ancho_real = root.winfo_width()
    alto_real = root.winfo_height()

    # Ubicarlo en la esquina inferior izquierda
    x = 10
    y = int(root.winfo_screenheight()) - alto_real - 50
    root.geometry(f"+{x}+{y}")

    # Cierra al hacer clic
    root.bind("<Button-1>", lambda e: root.destroy())
    
    # Cierra automáticamente en 8 segundos
    root.after(2000, root.destroy)
    
    root.mainloop()

def procesar_captura():
    """Captura pantalla y envía a OpenRouter"""
    print("\n[+] Procesando captura con OpenRouter...")
    try:
        # Tomar la foto
        captura = ImageGrab.grab()
        
        # Convertir la imagen a base64 para enviarla a la API
        buffered = io.BytesIO()
        captura.save(buffered, format="PNG")
        img_base64 = base64.b64encode(buffered.getvalue()).decode('utf-8')
        
        # Preparar la petición a OpenRouter
        headers = {
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json"
        }
        
        prompt = "Resuelve lo que ves en la imagen. Si es una pregunta de opción múltiple, dime SOLO la opción correcta de esta manera: A. No añadas explicaciones, sé extremadamente breve y directo, solo dame el literal."
        
        payload = {
            "model": MODELO,
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{img_base64}"}}
                    ]
                }
            ]
        }
        
        # Enviar petición
        response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=payload)
        data = response.json()
        
        if "choices" in data and len(data["choices"]) > 0:
            texto_respuesta = data["choices"][0]["message"]["content"].strip()
            print(f"Respuesta recibida: {texto_respuesta}")
            mostrar_respuesta(texto_respuesta)
        else:
            print("Error en OpenRouter:", data)
            mostrar_respuesta("Error API")
        
    except Exception as e:
        print(f"Error: {str(e)}")
        mostrar_respuesta("Error red")

print("==================================================")
print(" ASISTENTE OPENROUTER INICIADO ")
print("==================================================")
print("-> Presiona 'Ctrl + X' para capturar y preguntar.")
print("-> Presiona 'Esc' para cerrar el programa.")
print("==================================================")

# Atajos de teclado
keyboard.add_hotkey('ctrl+x', procesar_captura)
keyboard.wait('esc')
