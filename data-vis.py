import serial
import streamlit as st
import re

port = st.sidebar.text_input("COM-Port", "COM6")
baud = st.sidebar.number_input("Baudrate", 9600)

ser = serial.Serial(port, baud, timeout=1)

st.title("Arduino Datenanzeige")

placeholder = st.empty()

while True:
    line = ser.readline().decode().strip()
    if not line:
        continue

    # Prüfe das Format mit Regex
    pattern = r"Soll: (\d+\.\d+) C, Ist: (\d+\.\d+) C, T_sicher: (\d+\.\d+) C, Leistung: (\d+\.\d+) %"
    match = re.match(pattern, line)

    if match:
        # Extrahiere Werte
        soll, ist, t_sicher, leistung = map(float, match.groups())
        values = {
            "Soll": f"{soll} C",
            "Ist": f"{ist} C",
            "T_sicher": f"{t_sicher} C",
            "Leistung": f"{leistung} %"
        }
        placeholder.table(values)
    else:
        # Fehlermeldung bei falschem Format
        placeholder.error("Fehler: Ungültiges Datenformat empfangen.")
