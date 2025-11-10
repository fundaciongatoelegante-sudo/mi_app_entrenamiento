import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

# Configuración general
st.set_page_config(page_title="Mi Entrenamiento Semanal", page_icon="💪", layout="centered")

# Estado inicial
if "registro" not in st.session_state:
    st.session_state.registro = []

# Encabezado
st.title("🏋️‍♂️ Mi App de Entrenamiento Semanal")
st.write("Registra tus entrenamientos, mira tu progreso y mantente motivado 💥")

# Sección: Registrar entrenamiento
st.subheader("📅 Registrar entrenamiento")
dia = st.selectbox("Selecciona el día", ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"])
duracion = st.slider("Duración (minutos)", 10, 120, 30)
tipo = st.text_input("Tipo de entrenamiento", placeholder="Ej: Cardio, pesas, abdomen...")

if st.button("Guardar entrenamiento"):
    st.session_state.registro.append({
        "día": dia,
        "duración": duracion,
        "tipo": tipo,
        "fecha": datetime.now().strftime("%Y-%m-%d %H:%M")
    })
    st.success(f"✅ Entrenamiento guardado: {tipo} el {dia} ({duracion} min).")

# Sección: Mostrar progreso
st.subheader("📊 Tu progreso")
if st.session_state.registro:
    df = pd.DataFrame(st.session_state.registro)
    st.dataframe(df)

    # Gráfico
    fig, ax = plt.subplots()
    df.groupby("día")["duración"].mean().plot(kind="bar", ax=ax)
    ax.set_ylabel("Minutos promedio")
    ax.set_xlabel("Día")
    ax.set_title("Duración promedio por día")
    st.pyplot(fig)

    # Frases motivacionales simples
    total = df["duración"].sum()
    if total < 100:
        st.info("🚀 ¡Buen comienzo! Cada paso cuenta.")
    elif total < 300:
        st.success("🔥 ¡Excelente! Se nota la constancia.")
    else:
        st.balloons()
        st.success("🏆 ¡Increíble! Eres un ejemplo de disciplina.")
else:
    st.warning("Aún no registras entrenamientos.")

# Reiniciar
if st.button("🔄 Reiniciar datos"):
    st.session_state.registro = []
    st.info("Los datos han sido reiniciados.")
