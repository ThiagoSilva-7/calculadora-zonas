
import streamlit as st

def pace_to_seconds(pace_str):
    """Converte ritmo em mm:ss para segundos"""
    try:
        minutes, seconds = map(int, pace_str.strip().split(':'))
        return minutes * 60 + seconds
    except:
        raise ValueError("Formato inválido. Use o formato mm:ss (ex: 8:18)")

def seconds_to_pace(seconds):
    """Converte segundos para ritmo no formato mm:ss"""
    minutes = int(seconds // 60)
    secs = int(round(seconds % 60))
    return f"{minutes}:{secs:02d}"

def calcular_zonas(pace_3k_str):
    """Calcula as zonas de treino com base no pace de 3 km"""
    pace_3k_sec = pace_to_seconds(pace_3k_str)

    zonas = {
        "Z1 (Muito leve / regenerativo)": (0.60, 0.70),
        "Z2 (Leve / base aeróbica)": (0.70, 0.80),
        "Z3 (Moderado / limiar aeróbico)": (0.80, 0.90),
        "Z4 (Forte / limiar anaeróbico)": (0.90, 1.00),
        "Z5 (Muito forte / VO2máx)": (1.00, 1.10),
    }

    resultados = []
    for nome_zona, (low_pct, high_pct) in zonas.items():
        ritmo_lento = pace_3k_sec / low_pct
        ritmo_rapido = pace_3k_sec / high_pct
        resultados.append((nome_zona, seconds_to_pace(ritmo_lento), seconds_to_pace(ritmo_rapido)))
    return resultados

# --- INTERFACE STREAMLIT ---

st.title("🏃‍♂️ Calculadora de Zonas de Corrida")
st.write("Insira seu pace médio no teste de 3 km para estimar suas zonas de treino.")

pace_input = st.text_input("📏 Pace do teste de 3 km (formato mm:ss)", value="8:18")

if st.button("Calcular zonas"):
    try:
        zonas = calcular_zonas(pace_input)
        st.subheader("📊 Zonas estimadas:")
        for nome, lento, rapido in zonas:
            st.markdown(f"**{nome}**: {lento} – {rapido} min/km")
    except ValueError as e:
        st.error(str(e))
