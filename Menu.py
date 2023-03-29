#1. importar bibliotecas

import streamlit as st
from PIL import Image


st.set_page_config( page_title="PROJETO",
                    layout="wide",
                    page_icon="📈",
                    menu_items={
                                'Get help':None,
                                'Report a Bug': None,
                                'About': "## Projeto desenvolvido para turma *ECP10_T01*",
    })

st.write("# PHOTOVOLTAIC DATA VISUALIZATION ANALYSIS PROJECT! 💡")

st.sidebar.success("⬆️ Choose an option.")

image = Image.open('./how-work.png')

st.markdown(
    """
    
    #### Welcome to the Electrical Data Visualization System produced by Photovoltaic Plants, where this information can be transformed into valuable insights.
    The system has some valuable Dashboards with important information about the production of the Plants.
    

    **👈 Select one of the side options** to access the features
    of the system!
    ### System Composition:
    - **WEB Interface**: [Streamlit](https://docs.streamlit.io)
    - **Data Analytics**: [Pandas](https://pandas.pydata.org/docs/)
    - **Forecast Method**: [ARIMA (pmdarima)](http://alkaline-ml.com/pmdarima/)

    ### How work an Photovoltaic Plants

    ##### Every solar power plant consists at least of two basic components:

    **1**   Modules- that convert sunlight into electricity

    **2**   One or more inverters- devices that convert direct current into alternating current.

    
    """

)
st.image(image)
