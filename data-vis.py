import serial
import serial.tools.list_ports
import streamlit as st
import re
import pandas as pd
import time
import altair as alt
from datetime import datetime, timedelta

# Seitenleiste Konfiguration
st.sidebar.header("Konfiguration")
demo_mode = st.sidebar.toggle("Demo-Modus", value=False)

if demo_mode:
    st.sidebar.subheader("Demo Einstellungen")
    # Manuelle Werte für Demo-Modus
    soll_val = st.sidebar.number_input("Soll Temperatur (°C)", value=37.0)
    ist_val = st.sidebar.slider("Ist Temperatur (°C)", 20.0, 50.0, 36.5)
    t_sicher_val = st.sidebar.slider("T_sicher (°C)", 30.0, 60.0, 40.0)
    leistung_val = st.sidebar.slider("Leistung (%)", 0.0, 100.0, 50.0)
    
    port = None
    baud = 9600 # Dummy
else:
    # Verfügbare COM-Ports abfragen
    available_ports = [port.device for port in serial.tools.list_ports.comports()]

    if not available_ports:
        st.sidebar.error("Keine COM-Ports gefunden. Bitte schließen Sie ein Gerät an oder aktivieren Sie den Demo-Modus.")
        st.stop()
    else:
        port = st.sidebar.selectbox("COM-Port auswählen", available_ports)
        baud = st.sidebar.number_input("Baudrate", 9600)

st.title("Arduino Datenanzeige")

# Session State für Datenhistorie initialisieren
if 'history' not in st.session_state:
    st.session_state.history = []

# Platzhalter für die UI-Elemente
soll_placeholder = st.empty()
chart_placeholder = st.empty()
# Platzhalter für den Zeitraum-Input
minutes_placeholder = st.empty()
error_placeholder = st.empty()

ser = None
if not demo_mode:
    # Verbindung herstellen (nur im echten Modus)
    try:
        ser = serial.Serial(port, baud, timeout=1)
    except Exception as e:
        error_placeholder.error(f"Fehler beim Öffnen von {port}: {e}")
        st.stop()

# Das Eingabefeld wird EINMAL definiert (außerhalb der While-Schleife)
# Es wird aber erst sichtbar, wenn wir Daten haben (durch den Placeholder)
minutes_val = minutes_placeholder.number_input(
    "Zeitraum (Minuten)", 
    min_value=1, 
    value=10
)

while True:
    soll, ist, t_sicher, leistung = 0.0, 0.0, 0.0, 0.0
    valid_data = False

    if demo_mode:
        soll = soll_val
        ist = ist_val
        t_sicher = t_sicher_val
        leistung = leistung_val
        valid_data = True
    else:
        try:
            line = ser.readline().decode().strip()
            if not line:
                continue
            
            pattern = r"Soll: (\d+\.\d+) C, Ist: (\d+\.\d+) C, T_sicher: (\d+\.\d+) C, Leistung: (\d+\.\d+) %"
            match = re.match(pattern, line)
            if match:
                soll, ist, t_sicher, leistung = map(float, match.groups())
                valid_data = True
        except Exception as e:
            continue

    if valid_data:
        now = datetime.now()
        
        # Neuen Datensatz zur Historie hinzufügen
        st.session_state.history.append({
            "Zeit": now,
            "Ist": ist,
            "T_sicher": t_sicher,
            "Leistung": leistung
        })
        
        # Daten bereinigen basierend auf dem aktuellen Wert des Inputs
        cutoff_time = now - timedelta(minutes=minutes_val)
        st.session_state.history = [
            d for d in st.session_state.history if d["Zeit"] > cutoff_time
        ]
        
        # 1. Soll-Wert als Metrik anzeigen
        soll_placeholder.metric("Soll Temperatur", f"{soll} °C")
        
        # 2. Liniendiagramm aktualisieren
        if st.session_state.history:
            df = pd.DataFrame(st.session_state.history)
            
            base = alt.Chart(df).encode(x=alt.X('Zeit', axis=alt.Axis(title='Zeit', format='%H:%M:%S')))

            temps = base.transform_fold(
                ['Ist', 'T_sicher'],
                as_=['Variable', 'Temperatur']
            ).mark_line().encode(
                y=alt.Y('Temperatur:Q', axis=alt.Axis(title='Temperatur (°C)')),
                color='Variable:N'
            )

            power = base.mark_line(color='red').encode(
                y=alt.Y('Leistung:Q', axis=alt.Axis(title='Leistung (%)', orient='right'))
            )

            combined_chart = alt.layer(temps, power).resolve_scale(y='independent')
            chart_placeholder.altair_chart(combined_chart, use_container_width=True)

    if demo_mode:
        time.sleep(0.5)