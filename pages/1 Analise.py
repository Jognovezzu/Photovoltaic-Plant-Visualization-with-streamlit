#1. importar bibliotecas

import pandas as pd
import streamlit as st

st.set_page_config( page_title="Analysis",
                    layout="wide",
                    page_icon="📈",
                    menu_items={
        'Get help':None,
        'Report a Bug': None,
        'About': "## Projeto desenvolvido para turma *ECP10_T01*",
    })

st.title("Data Visualization")
st.caption("This Dashboard was generated with a focus on monitoring the generation of Photovoltaic Energy from the Power Plants.")






# 2. Chamar a API

lista_empresa = ['Plant 1', 'Plant 2']
with st.container():
    st.header("Choose an Plant:")

    planta_ = st.selectbox("Select the desired plant:", options=lista_empresa)
    planta = planta_.replace(' ','_')
    print(planta)


import numpy as np
import pandas as pd
import os
import matplotlib.pyplot as plt
import seaborn as sns
import statsmodels.api as sm
from scipy.stats import normaltest
import holoviews as hv
from holoviews import opts
import cufflinks as cf

file = f'./archive (1)/{planta}_Generation_Data.csv'
file1 = f'./archive (1)/{planta}_Weather_Sensor_Data.csv'
#3. Gera o Dataframe
plant = pd.read_csv(file)
plant_sensor = pd.read_csv(file1)


plant_sensor['DATE_TIME'] = pd.to_datetime(plant_sensor['DATE_TIME'], errors='coerce')
plant_sensor['date'] = pd.to_datetime(pd.to_datetime(plant_sensor['DATE_TIME']).dt.date)
plant_sensor['time'] = pd.to_datetime(plant_sensor['DATE_TIME']).dt.time
del plant_sensor['PLANT_ID']
del plant_sensor['SOURCE_KEY']


#print(df.tail)

with st.container():

    st.subheader(f"Main Details:")
    col1, col2 = st.columns(2)

    with col1:
        st.metric(f"Number of Inverters :",plant.groupby('SOURCE_KEY').sum().count()[0] )

    with col2:
        st.metric(f"Number of Days: ", 16)
plant_generation = plant.copy()
plant_generation = plant_generation.groupby('DATE_TIME')[['DC_POWER','AC_POWER', 'DAILY_YIELD','TOTAL_YIELD']].agg('sum')
plant_generation = plant_generation.reset_index()
plant_generation['DATE_TIME'] = pd.to_datetime(plant_generation['DATE_TIME'], errors='coerce')
plant_generation['time'] = plant_generation['DATE_TIME'].dt.time
plant_generation['date'] = pd.to_datetime(plant_generation['DATE_TIME'].dt.date)

with st.container():
    st.title(""" DC Power""")
    col3, col4 = st.columns(2)


    
    with col3:
        #plant1_data.groupby('time')['DC_POWER'].agg('mean').plot(legend=True, colormap='Reds_r')
        plt.ylabel('DC Power')
        plt.title('DC POWER plot')
        plt.show()
        st.pyplot(plant_generation.plot(x= 'time', y='DC_POWER', style='.', figsize = (15, 8),title='DC Power',stacked=True).figure)


    with col4:
        daily_dc = plant_generation.groupby('date')['DC_POWER'].agg('sum')
        daily_dc.plot.bar(figsize=(15,5), legend=True)
        plt.title('Daily DC Power')
        plt.show()
        st.pyplot(daily_dc.plot.bar(figsize=(15,5), legend=True,stacked = True).figure)


with st.container():

    st.title(" Daily Yield")

    col5, col6 = st.columns(2)

    with col5:
    
        #plant1_data.groupby('time')['DAILY_YIELD'].agg('mean').plot(legend=True, colormap='Reds_r')
        plt.title('DAILY YIELD')
        plt.ylabel('Yield')
        plt.show()    
        st.pyplot(plant_generation.plot(x='time', y='DAILY_YIELD', style='.', figsize=(15,5),stacked=True,title='Yield an Day').figure)  


    with col6:

        dyield = plant_generation.groupby('date')['DAILY_YIELD'].agg('sum')  
        plt.title('Daily YIELD')
        plt.show()
        st.pyplot(dyield.plot.bar(figsize=(15,5), legend=True,stacked= True).figure)



with st.container():
    st.title('Plant Weather Sensor')

    col7, col8 = st.columns(2)

    with col7:

        st.text('Ambient Temperature')
        #plant1_sensor.groupby('time')['AMBIENT_TEMPERATURE'].agg('mean').plot(legend=True, colormap='Reds_r')
        plt.show()
        st.pyplot(plant_sensor.plot(xlabel='Time',ylabel='Temperature (°C)', x='time', y = 'AMBIENT_TEMPERATURE' , style='.',legend=True, figsize=(15,5),stacked=True).figure)

    with col8:

        st.text('Module Temperature')
        plant_sensor.plot(x='time', y='MODULE_TEMPERATURE', figsize=(15,8), style='b.')
        st.pyplot(plant_sensor.plot(xlabel='Time',
                                ylabel='Temperature (°C)',
                                x='time', 
                                y='MODULE_TEMPERATURE', 
                                figsize=(15,5), 
                                style='.').figure,plant_sensor.groupby('time')['MODULE_TEMPERATURE'].agg('mean').plot(colormap='Reds_r', legend=True))