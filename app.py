import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
from io import BytesIO

st.set_page_config(layout='wide')

st.title("Fondos extrapresupuestales")

df = pd.read_csv('fondos_limpios.csv', low_memory=False)
df2 = df.copy()
df[['obligacion_pc', 'compromiso_pc', 'orden_pago_pc']] /= 1_000_000_000
VALS_DIC = {'Obligación': 'obligacion_pc',
                'Compromiso': 'compromiso_pc',
                'Orden de pago':'orden_pago_pc'}
tab1, tab2, tab3 = st.tabs(['General', 'Diferenciado', 'Descarga general'])

st.write("*Los valores están a precios constantes de 2024 y en miles de millones de pesos.")

with tab1:

    st.header("Fondos extrapresupuestales (tipo de gasto)")
    var = st.selectbox("Seleccione una variable", ['Obligación', 'Compromiso', 'Orden de pago'])
    piv = df.pivot_table(index=['AÑO', 'Tipo de gasto'],
                   values=VALS_DIC[var],
                   aggfunc='sum').reset_index()  

    fig = px.bar(piv, x='AÑO', y=VALS_DIC[var], color='Tipo de gasto')  

    st.plotly_chart(fig)




    st.header('Treemap')
    year = st.select_slider("Seleccione un año", df['AÑO'].unique().tolist())

    fil_year = df[df['AÑO'] == year]

    
    fig = px.treemap(data_frame=fil_year,
               path=[px.Constant('Fondos extrapresupuestales'),
                     'Sector',
                     'Entidad',
                     'Unidad',
                     'Tipo de gasto'],
               values=VALS_DIC[var])
    st.plotly_chart(fig)

    st.subheader("Fondo")

    piv = df.pivot_table(index=['AÑO', 'NOMBRE FIDUCIARIA'],
                   values=VALS_DIC[var],
                   aggfunc='sum').reset_index()  

    fig = px.bar(piv, x='AÑO', y=VALS_DIC[var], color='NOMBRE FIDUCIARIA')  
    fig.update_layout(showlegend=False)

    st.plotly_chart(fig)

    # flujo (sector fiduciaria o general fiduciaria)

with tab2:
     
    # seleccionar sector 
    # gráfico de área (discriminar por tipo de gasto)
    var = st.selectbox("Seleccione una variable", ['Obligación', 'Compromiso', 'Orden de pago'], key=100)

    st.subheader("Fondos extrapresupuestales por sector (tipo de gasto)")
    sector = st.selectbox("Seleccione un sector", df['Sector'].unique().tolist(), key=10)

    fil_sec = df[df['Sector'] == sector]
    piv = fil_sec.pivot_table(index=['AÑO', 'Tipo de gasto'],
                   values=VALS_DIC[var],
                   aggfunc='sum').reset_index()  

    fig = px.bar(piv, x='AÑO', y=VALS_DIC[var], color='Tipo de gasto')  
    st.plotly_chart(fig)

    st.subheader("Fondos extrapresupuestales por sector y entidad (tipo de gasto)")
    entidad = st.selectbox("Seleccione una entidad", fil_sec['Entidad'].unique().tolist(), key=20)
    filsec_ent = fil_sec[fil_sec['Entidad'] == entidad]
    piv = filsec_ent.pivot_table(index=['AÑO', 'Tipo de gasto'],
                   values=VALS_DIC[var],
                   aggfunc='sum').reset_index()  

    fig = px.bar(piv, x='AÑO', y=VALS_DIC[var], color='Tipo de gasto')  

    st.plotly_chart(fig)

    # seleccionar sector y entidad
    # gráfico de área (discriminar por tipo de gasto)


with tab3:

    st.dataframe(df2)

    binary_output = BytesIO()
    df.to_excel(binary_output, index=False)
    st.download_button(label = 'Descargar excel',
                    data = binary_output.getvalue(),
                    file_name = 'datos.xlsx')
