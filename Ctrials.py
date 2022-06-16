import pyodbc 
import pandas as pd
import streamlit as st

server = 'aact-db.ctti-clinicaltrials.org' 
database = 'aact' 
username = 'git0bf' 
password =  st.secrets["password"]
cnxn = pyodbc.connect('Driver={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)


df = pd.read_sql_query('select count(*) from studies', cnxn)

st.write(df)

