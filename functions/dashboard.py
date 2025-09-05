import streamlit as st
import pandas as pd
import time
from functions.consumer import fill_dataframe

'''

STILL IN DEVELOPMENT

'''

st.set_page_config(page_title="Streamlit + Event Hubs", layout="wide")

st.title("Dashboard en Tiempo Real desde Azure Event Hub")

# Iniciar el lector de eventos
df = fill_dataframe()

# DataFrame para mostrar los eventos
df = pd.DataFrame(columns=["timestamp", "mensaje"])
chart = st.line_chart(df)

placeholder = st.empty()

while True:
    while not event_queue.empty():
        mensaje = event_queue.get()
        now = pd.Timestamp.utcnow()
        df = pd.concat([df, pd.DataFrame({"timestamp": [now], "mensaje": [mensaje]})], ignore_index=True)

        # Mostrar últimos 20 eventos
        df = df.tail(20)

        # Actualizar gráfico de cantidad de mensajes por segundo (solo como ejemplo visual)
        chart_data = df.groupby(df['timestamp'].dt.second).count()["mensaje"]
        chart.add_rows(chart_data)

        # Mostrar tabla
        placeholder.table(df)

    time.sleep(1)
