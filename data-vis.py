from serial import Serial
import serial.tools.list_ports
import streamlit as st
import re
import pandas as pd
from datetime import datetime, timedelta

# Verfügbare COM-Ports abfragen
available_ports = [port.device for port in serial.tools.list_ports.comports()]

# Seitenleiste Konfiguration
if not available_ports:
    st.sidebar.error("Keine COM-Ports gefunden. Bitte schließen Sie ein Gerät an.")
    st.stop()
else:
    port = st.sidebar.selectbox("COM-Port auswählen", available_ports)

baud = st.sidebar.number_input("Baudrate", 9600)
minutes = st.sidebar.number_input("Zeitraum (Minuten)", min_value=1, value=10)

st.title("Arduino Datenanzeige")

# Session State für Datenhistorie initialisieren
if 'history' not in st.session_state:
    st.session_state.history = []

# Platzhalter für die UI-Elemente erstellen
# "Soll" wird oben angezeigt
soll_placeholder = st.empty()
# Darunter das Diagramm
chart_placeholder = st.empty()
# Fehlermeldungen
error_placeholder = st.empty()

# Verbindung herstellen
try:
    # Hinweis: Dies öffnet den Port bei jedem Script-Rerun neu.
    ser = Serial(port, baud, timeout=1)
except Exception as e:
    error_placeholder.error(f"Fehler beim Öffnen von {port}: {e}")
    st.stop()

while True:
    try:
        # Lese Zeile vom Serial Port
        line = ser.readline().decode().strip()
    except Exception as e:
        # Falls Lesen fehlschlägt (z.B. Gerät getrennt)
        continue

    if not line:
        continue

    # Regex Pattern Matching
    pattern = r"Soll: (\d+\.\d+) C, Ist: (\d+\.\d+) C, T_sicher: (\d+\.\d+) C, Leistung: (\d+\.\d+) %"
    match = re.match(pattern, line)

    if match:
        # Werte extrahieren
        soll, ist, t_sicher, leistung = map(float, match.groups())
        
        # Aktueller Zeitstempel
        now = datetime.now()
        
        # Neuen Datensatz zur Historie hinzufügen
        st.session_state.history.append({
            "Zeit": now,
            "Ist": ist,
            "T_sicher": t_sicher,
            "Leistung": leistung
        })
        
        # Daten bereinigen (nur Daten im gewünschten Zeitraum behalten)
        cutoff_time = now - timedelta(minutes=minutes)
        st.session_state.history = [
            d for d in st.session_state.history if d["Zeit"] > cutoff_time
        ]
        
        # 1. Soll-Wert als Metrik anzeigen
        soll_placeholder.metric("Soll Temperatur", f"{soll} °C")
        
        # 2. Liniendiagramm aktualisieren
        if st.session_state.history:
            df = pd.DataFrame(st.session_state.history)
            # Zeit als Index setzen für korrekte x-Achse im Chart
            df = df.set_index("Zeit")
            chart_placeholder.line_chart(df)
    else:
        # Optional: Warnung bei unerwartetem Format, aber nicht bei jedem Loop spammen
        pass