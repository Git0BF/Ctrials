import psycopg2
import pandas as pd

#Dl AACT db here :https://aact.ctti-clinicaltrials.org/snapshots
#install Postgres

# Data exploration. (Path to relevant files in the DB)

#Clinical trials analysis

#Source  ctgov.studies.source

#Title ctgov.studies.official_tittle /brief_tittle

#Indication ctgov.conditions.name (keys : nct_id; id)

#Objectives Primary/secondary/ Endpoint outcome ctgov.outcomes.outcome_type

#Number previous of studies/ results of previous phases ??

#Study protocol  ctgov.detailed_descriptions

#Analysis plan to evaluate the endpoints (Intention to treat?) ctgov.outcomes.population (Intent-to-treat)

#Hypothesis tested H0 ????

#Clinical outcome of interest ctgov.outcomes.outcome_type/title/desciption

#METHODS:

#- Name of the method ctgov.outcome_analyses.method

#- Type of studies (random/blind x2+) ctgov.studies.phase

#- Number of participant ctgov.studies.enrollement

#- Interventions (type of drugs given) ctgov.interventions.intervention_type/name/description/// ctgov.design_groups.title/description/timeframe (id; nct_id)

#- Evaluation method ctgov.outcome_analyses.method (t_test, ancova)/ method_description/ groups_description (Week 8 etc.)

#- Parameters ctgov.outcome_analyses.param_type / param_value / p_value/  p_value_description/ ci_n_sides/ ci_percent/ ci_lower_limit/ ci_upper_limit/

#Baseline values ctgov.baseline_measurements.title/ units/ param_value

#Delta to placebo (control group) ????

#Primary/Sec Endpoint outcome ctgov.outcomes.outcome_type/ title/ description/ time_frame/ population

#Group selection ????

#Previous papers ????

#Authors rep ????

#Sponsor/author conflict of interest ????

hostname = 'localhost'
database = 'aact'
username = 'postgres'
pwd = '*******'
port_id = 5432
conn = None
cur= None

try:
    conn = psycopg2.connect(dbname=database, user= username, password= pwd, host=hostname, port= port_id)
    cur = conn.cursor()
    
    dfdes = pd.read_sql_query("select * from ctgov.designs where ctgov.designs.allocation ='Randomized' and ctgov.designs.primary_purpose = 'Treatment' and ctgov.designs.masking = 'Quadruple'or ctgov.designs.masking = 'Triple' or ctgov.designs.masking = 'Double'", con=conn)
    #print(dfdes)
    #print(dfdesc['intervention_model_description'].value_counts())
    
    dfphase = pd.read_sql_query("SELECT * FROM ctgov.studies where ctgov.studies.phase = 'Phase 3' and ctgov.studies.is_fda_regulated_drug = False;", con=conn )
    #print(dfphase)
    dfoutcome = pd.read_sql_query("select * from ctgov.outcome_analyses", con=conn)
    #print(dfoutcome)
    #print(dfoutcome['method'].value_counts())
    
    dfjoin_des_out =pd.read_sql_query("select * from ctgov.outcome_analyses where nct_id in (select ctgov.designs.nct_id from ctgov.designs where ctgov.designs.allocation ='Randomized' and ctgov.designs.primary_purpose = 'Treatment' and ctgov.designs.masking = 'Quadruple'or ctgov.designs.masking = 'Triple' or ctgov.designs.masking = 'Double');", con=conn)
    #print(dfjoin_des_out)
    query= "create table ctgov.join as select * from ctgov.studies inner join ctgov.outcome_analyses using (nct_id);"
    dfj = pd.read_sql_query(query, con=conn)
   
    
    conn.close()
    cur.close()
finally:
    if conn is not None :
        conn.close()
    if cur is not None :
        cur.close()

