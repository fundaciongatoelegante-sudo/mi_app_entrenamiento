# app_entrenamiento_moderno.py
import json
import os
import datetime
import threading
import time
import tkinter as tk
from tkinter import messagebox
from ttkbootstrap import Style
from ttkbootstrap import ttk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# ----------------------------------------
# CONFIGURACIÓN Y DATOS
# ----------------------------------------
ARCHIVO_DATOS = "progreso_entrenamiento.json"
ARCHIVO_CONFIG = "config_entrenamiento.json"
DIAS = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
EJERCICIOS_POR_DEFECTO = ["Pecho", "Espalda", "Piernas", "Core", "Cardio", "Brazos", "Descanso"]

# ----------------------------------------
# FUNCIONES DE GUARDADO Y CARGA
# ----------------------------------------
def inicializar_datos():
    return {
        "progreso_dias": {dia: False for dia in DIAS},
        "ejercicios_realizados": {dia: "" for dia in DIAS},
        "historial": [],
        "ultima_semana": datetime.datetime.now().isoformat(),
        "racha_actual": 0,
        "mejor_racha": 0
    }

def archivar_semana_automatico(data):
    data["historial"].append({
        "fecha": str(datetime.date.today()),
        "resumen": data["progreso_dias"].copy(),
        "ejercicios": data["ejercicios_realizados"].copy()
    })

def cargar_datos():
    if os.path.exists(ARCHIVO_DATOS):
        try:
            with open(ARCHIVO_DATOS, "r", encoding="utf-8") as f:
                data = json.load(f)
        except Exception:
            # Si el archivo está corrupto o vacío, reiniciamos
            return inicializar_datos()
        # Comprobar cambio de semana (número ISO)
        if "ultima_semana" in data:
            try:
                semana_guardada = datetime.datetime.fromisoformat(data["ultima_semana"]).isocalendar()[1]
                semana_actual = datetime.datetime.now().isocalendar()[1]
                if semana_actual != semana_guardada:
                    if messagebox.askyesno("Nueva semana", "Se detectó una nueva semana. ¿Deseas reiniciar el progreso?"):
                        archivar_semana_automatico(data)
                        return inicializar_datos()
            except Exception:
                # Si falla el parseo, re-inicializamos
                return inicializar_datos()
        # Asegurar estructura mínima
        if "progreso_dias" not in data or "ejercicios_realizados" not in data:
            return inicializar_datos()
        return data
    return inicializar_datos()

def guardar_datos():
    # actualizar ultima_semana al guardar
    datos["ultima_semana"] = datetime.datetime.now().isoformat()
    with open(ARCHIVO_DATOS, "w", encoding="utf-8") as f:
        json.dump(datos, f, indent=4, ensure_ascii=False)

def cargar_config():
    if os.path.exists(ARCHIVO_CONFIG):
        try:
            with open(ARCHIVO_CONFIG, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    # Por defecto
    return {"hora_recordatorio": 19, "minuto_recordatorio": 0, "recordatorio_activo": True}

def guardar_config():
    with open(ARCHIVO_CONFIG, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=4, ensure_ascii=False)

# ----------------------------------------
# LÓGICA
# ----------------------------------------
def actualizar_racha():
    """
    Cuenta la racha mirando hacia atrás desde hoy (conteo de días consecutivos finalizando hoy).
    """
    hoy_idx = datetime.datetime.now().weekday()  # 0 lunes ... 6 domingo
    racha = 0
    # recorrer desde hoy hacia atrás
    for i in range(hoy_idx, -1, -1):
        dia = DIAS[i]
        if datos["progreso_dias"].get(dia, False):
            racha += 1
        else:
            break
    datos["racha_actual"] = racha
    if racha > datos.get("mejor_racha", 0):
        datos["mejor_racha"] = racha
    etiqueta_racha.config(text=f"🔥 Racha: {datos['racha_actual']} días | Mejor: {datos['mejor_racha']}")

def marcar_completado(dia):
    datos["progreso_dias"][dia] = True
    botones[dia].configure(bootstyle="success")
    guardar_datos()
    actualizar_barra()
    actualizar_racha()
    messagebox.showinfo("¡Excelente!", f"Entrenamiento del {dia} completado 💪")

def guardar_ejercicio(dia):
    valor = entradas[dia].get().strip()
    if valor:
        datos["ejercicios_realizados"][dia] = valor
        guardar_datos()
        messagebox.showinfo("Guardado", f"Ejercicio de {dia}: {valor}")
    else:
        messagebox.showwarning("Atención", "Escribe un ejercicio antes de guardar.")

def mostrar_resumen():
    completados = sum(1 for v in datos["progreso_dias"].values() if v)
    total = len(DIAS)
    porcentaje = (completados / total) * 100 if total else 0
    resumen = f"✅ {completados}/{total} días completados ({porcentaje:.1f}%)\n"
    resumen += f"🔥 Racha actual: {datos['racha_actual']} días\n\n"
    for dia in DIAS:
        estado = "✅" if datos["progreso_dias"].get(dia)_]()
