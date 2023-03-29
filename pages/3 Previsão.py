import streamlit as st
from pandas.tseries.offsets import DateOffset
from pmdarima.arima import auto_arima
from statsmodels.tsa.stattools import adfuller

st.set_page_config( page_title="Previsão Financeira",
                    layout="wide",
                    page_icon="📈",
                    menu_items={
        'Get help':None,
        'Report a Bug': None,
        'About': "## Projeto desenvolvido para turma *ECP10_T01*",
    })


st.title("Daily Yield Forecast")
st.caption("This Dashboard aims to generate a possible forecast of the daily yield of a Plant")



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
import pickle
from pmdarima.arima import auto_arima



file = f'./archive (1)/Plant_1_Generation_Data.csv'
file1 = f'./archive (1)/Plant_1_Weather_Sensor_Data.csv'
#3. Gera o Dataframe
gen_1 = pd.read_csv(file)
gen_1.drop('PLANT_ID',1,inplace=True)
sens_1 = pd.read_csv(file1)
sens_1.drop('PLANT_ID',1,inplace=True)

#format datetime
gen_1['DATE_TIME']= pd.to_datetime(gen_1['DATE_TIME'],errors='ignore' , format='%d-%m-%Y %H:%M')
sens_1['DATE_TIME']= pd.to_datetime(sens_1['DATE_TIME'],format='%Y-%m-%d %H:%M:%S')
pred_gen=gen_1.copy()
pred_gen=pred_gen.groupby('DATE_TIME').sum()
pred_gen=pred_gen['DAILY_YIELD'][-288:].reset_index()
pred_gen.set_index('DATE_TIME',inplace=True)
#pred_gen.head()

with st.container():
    st.set_option('deprecation.showPyplotGlobalUse', False)


    result = adfuller(pred_gen['DAILY_YIELD'])
    st.text('Augmented Dickey-Fuller Test:')
    labels = ['ADF Test Statistic','p-value','#Lags Used','Number of Observations Used']

    for value,label in zip(result,labels):
        st.text(label+' : '+str(value) )
        
    if result[1] <= 0.05:
        st.text("strong evidence against the null hypothesis, reject the null hypothesis. Data has no unit root and is stationary")
    else:
        st.text("weak evidence against null hypothesis, time series has a unit root, indicating it is non-stationary ")




    train=pred_gen[:192]
    test=pred_gen[-96:]
    plt.figure(figsize=(15,5))
    plt.plot(train,label='Train',color='blue')
    plt.plot(test,label='Test',color='red')
    plt.title('Last 4 days of daily yield',fontsize=17)
    plt.legend()

    st.pyplot(plt.plot())
    plt.close()



#Open model trained
with st.container():
        
    with open(f'arima_picklePlant_1','rb') as f:
        arima_model = pickle.load(f)



    future_dates = [test.index[-1] + DateOffset(minutes=x) for x in range(0,2910,15) ]
    
    prediction=pd.DataFrame(arima_model.predict(n_periods=96),index=test.index)
    prediction.columns=['predicted_yield']

    fig,ax= plt.subplots(ncols=2,nrows=1,dpi=100,figsize=(17,5))
    ax[0].plot(train,label='Train',color='navy')
    ax[0].plot(test,label='Test',color='darkorange')
    ax[0].plot(prediction,label='Prediction',color='green')
    ax[0].legend()
    ax[0].set_title('Forecast on test set',size=17)
    ax[0].set_ylabel('kW',color='navy',fontsize=17)


    f_prediction=pd.DataFrame(arima_model.predict(n_periods=194),index=future_dates)
    f_prediction.columns=['predicted_yield']
    ax[1].plot(pred_gen,label='Original data',color='navy')
    ax[1].plot(f_prediction,label='18th & 19th June',color='green')
    ax[1].legend()
    ax[1].set_title('Next days forecast',size=17)
    st.pyplot(plt.plot())
    plt.close()
