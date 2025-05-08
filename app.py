# archivo: app.py

import streamlit as st
import pandas as pd
import plotly.express as px
from io import StringIO

st.set_page_config(page_title="Análisis de Datos - TODO Mining", layout="centered")

st.title("📊 Análisis Rápido de tus Datos")
st.markdown(
    """
    Sube un archivo `.csv` y te mostraré insights y gráficos automáticamente.

    ⚠️ **Formato esperado**:
    - El archivo debe estar separado por punto y coma (`;`) o coma (`,`).
    - Los decimales pueden estar con coma o punto.
    - Debe tener encabezados en la primera fila.
    

    """
)

uploaded_file = st.file_uploader("📂 Cargar archivo CSV", type=["csv"])

if uploaded_file is not None:
    try:
        # Leer como texto
        stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))
        text = stringio.read()
        stringio.seek(0)

        # Detectar separador automáticamente
        sep = ";" if text.count(";") > text.count(",") else ","
        decimal = "," if sep == ";" else "."

        df = pd.read_csv(StringIO(text), sep=sep, decimal=decimal)

        st.subheader("🔍 Vista previa de tus datos")
        st.dataframe(df.head())

        st.subheader("📈 Estadísticas generales")
        st.write(df.describe())

        st.subheader("📊 Gráfico de barras automático")
        numeric_cols = df.select_dtypes(include='number').columns

        if len(numeric_cols) >= 1:
            x_col = st.selectbox("Selecciona columna para eje X", df.columns)
            y_col = st.selectbox("Selecciona columna numérica para eje Y", numeric_cols)

            fig = px.bar(df, x=x_col, y=y_col)
            st.plotly_chart(fig)
        else:
            st.warning("Tu archivo no contiene columnas numéricas para graficar.")

        st.success("✅ Análisis completado. Puedes probar con otro archivo si deseas.")

    except Exception as e:
        st.error(f"❌ Error al procesar el archivo: {e}")
else:
    st.info("📌 Carga un archivo CSV para comenzar.")
