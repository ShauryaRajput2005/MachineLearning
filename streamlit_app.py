import streamlit as st
import pandas as pd
st.title('🎈 Machine Learning App')

st.write('Hello world!')
st.info('This is a Machine learning model')
with st.expander('Data'):
  st.write('**Raw Data**')
  df=pd.read_csv('https://raw.githubusercontent.com/dataprofessor/data/refs/heads/master/penguins_cleaned.csv')
  df
