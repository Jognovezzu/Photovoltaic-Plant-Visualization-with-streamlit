
import pandas as pd
import datetime as dt
import streamlit as st

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

st.set_page_config( page_title="Comparison between Plants",
                    layout="wide",
                    page_icon="💡",
                    menu_items={
        'Get help':None,
        'Report a Bug': None,
        'About': "## Projeto desenvolvido para turma *ECP10_T01*",
    })


st.title("Production Comparison")
st.caption("This Dashboard was generated with a focus on comparing data between two plants")


planta = 'Plant_1'
planta2 = 'Plant_2'

file = f'./archive (1)/{planta}_Generation_Data.csv'
file1 = f'./archive (1)/{planta}_Weather_Sensor_Data.csv'
file2 = f'./archive (1)/{planta2}_Generation_Data.csv'
file3 = f'./archive (1)/{planta2}_Weather_Sensor_Data.csv'


plant1 = pd.read_csv(file)
plant2 = pd.read_csv(file2)
plant_sensor1 = pd.read_csv(file1)
plant_sensor2 = pd.read_csv(file3)


#PLANT 1

plant1 = plant1.groupby('DATE_TIME')[['DC_POWER','AC_POWER', 'DAILY_YIELD','TOTAL_YIELD']].agg('sum')
plant1 = plant1.reset_index()
plant1['DATE_TIME'] = pd.to_datetime(plant1['DATE_TIME'], errors='coerce')
plant1['time'] = plant1['DATE_TIME'].dt.time
plant1['date'] = pd.to_datetime(plant1['DATE_TIME'].dt.date)


#PLANT 2

plant2 = plant2.groupby('DATE_TIME')[['DC_POWER','AC_POWER', 'DAILY_YIELD','TOTAL_YIELD']].agg('sum')
plant2 = plant2.reset_index()
plant2['DATE_TIME'] = pd.to_datetime(plant2['DATE_TIME'], errors='coerce')
plant2['time'] = plant2['DATE_TIME'].dt.time
plant2['date'] = pd.to_datetime(plant2['DATE_TIME'].dt.date)

#PLANT SENSOR 1

plant_sensor1['DATE_TIME'] = pd.to_datetime(plant_sensor1['DATE_TIME'], errors='coerce')
plant_sensor1['date'] = pd.to_datetime(pd.to_datetime(plant_sensor1['DATE_TIME']).dt.date)
plant_sensor1['time'] = pd.to_datetime(plant_sensor1['DATE_TIME']).dt.time
del plant_sensor1['PLANT_ID']
del plant_sensor1['SOURCE_KEY']

#PLANT SENSOR 2

plant_sensor2['DATE_TIME'] = pd.to_datetime(plant_sensor2['DATE_TIME'], errors='coerce')
plant_sensor2['date'] = pd.to_datetime(pd.to_datetime(plant_sensor2['DATE_TIME']).dt.date)
plant_sensor2['time'] = pd.to_datetime(plant_sensor2['DATE_TIME']).dt.time
del plant_sensor2['PLANT_ID']
del plant_sensor2['SOURCE_KEY']




with st.container():

    st.title("Power Per Hour")

    col1, col2  = st. columns(2)

    with col1:
        st.text('DC Power Comparison')

        #we conpare a dc power of two plant
        ax = plant1.plot(x='time', y='DC_POWER', figsize=(15,5), legend=True, style='.')
        

        st.pyplot(plant2.plot(xlabel='Time',
                            ylabel='Power (KW)',
                            title= 'Plant1(blue) vs Plant2(red)',                          x='time', 
                            y='DC_POWER', 
                            legend=True, 
                            style='r.',
                            figsize=(15,5), 
                            ax=ax).figure)
    
    with col2:
        st.text('AC Power Comparison')




        ax1 = plant1.plot(x='time', y='AC_POWER', figsize=(15,5), legend=True, style='.', )

        st.pyplot(plant2.plot(x='time', y='AC_POWER', 
                            figsize=(15,5),
                            xlabel='Time',
                            ylabel='Power (KW)',
                            title = 'Plant1(blue) vs Plant2(red)',
                            legend=True, style='r.', ax=ax1).figure)
    


with st.container():

    st.title("Power Per Day")

    col3, col4 = st.columns(2)

    with col3:
        st.text('DC Power Comparison')
        daily_dc = plant1.groupby('date')['DC_POWER'].agg('sum')
        p2_daily_dc = plant2.groupby('date')['DC_POWER'].agg('sum')
        axh = daily_dc.plot.bar( figsize=(15,5), label='DC_POWER Plant I')
        p2_daily_dc.plot.bar(color='Red', label='DC_POWER Plant II', stacked=False)
        st.pyplot(axh.figure)
        plt.close()

    with col4:
        st.text('AC Power Comparison')
        daily_ac = plant1.groupby('date')['AC_POWER'].agg('sum')
        p2_daily_ac = plant2.groupby('date')['AC_POWER'].agg('sum')
        ac = daily_ac.plot.bar( figsize=(15,5), label='AC_POWER Plant I')
        p2_daily_ac.plot.bar(color='Red', label='AC_POWER Plant II')
        st.pyplot(ac.figure)
        plt.close()


with st.container():
    st.title('Daily Yield')
    st.text('Daily Yield Comparison')
    dyield = plant1.groupby('date')['DAILY_YIELD'].agg('sum')
    p2_dyield = plant2.groupby('date')['DAILY_YIELD'].agg('sum')

    dy = dyield.plot.bar(ylabel='Energy (KWh)',figsize=(15,5), legend=True, label='DAILY_YIELD PLANT I')
    p2_dyield.plot.bar(legend=True, label='DAILY_YIELD PLANT II', color='Red')
    plt.title('Daily Yield Comparison')
    st.pyplot(dy.figure)
    plt.close()

    

with st.container():
    st.title('Weather Sensors')
    st.text('Irradiation Comparison')
    aq = plant_sensor1.plot(x='time', y='IRRADIATION', legend=True, label='IRRADIATION PLANT I', style='.', figsize=(15,5))
    st.pyplot(plant_sensor2.plot(x='time', y='IRRADIATION', title='Irradiation Comparison', legend=True, label='IRRADIATION PLANT II',  color='Red', style='.', ax=aq).figure)




