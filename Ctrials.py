import psycopg2
import pandas as pd

conn = psycopg2.connect(dbname='aact', user='git0bf', password=st.secrets["password"], host='aact-db.ctti-clinicaltrials.org', port='5432')
df = pd.read_sql_query("select count(*) from studies", con=conn)

print(df)

