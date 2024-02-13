# -*- coding: utf-8 -*-
"""
Created on Fri Sep 29 14:17:46 2023

@author: Chaimaa
"""

import streamlit as st # web development
import numpy as np # np mean, np random 
import pandas as pd # read csv, df manipulation
import time # to simulate a real time data, time loop 
import plotly.express as px # interactive charts 
import calendar
from plotly.subplots import make_subplots
import plotly.graph_objects as go



st.set_page_config(
    page_title = 'Bloc opératoire',
    layout = 'wide'
)

# Load DataFrame
data_bloc=pd.read_excel(r"C:\Users\Chaimae\data_bloc.xlsx")
st.markdown("<h1 style='text-align: center;'>Bloc Central Dashboard</h1>", unsafe_allow_html=True)





# Personnel
#data_bloc['operateur_principal'] = data_bloc['prenom_op'] +' '+ data_bloc['nom_op']
#data_bloc['operateur_secodaire'] = data_bloc['prenom_os'] +' '+ data_bloc['nom_os']
#data_bloc['medecin_anesthesiste'] = data_bloc['prenom_an'] +' '+ data_bloc['nom_an']
#data_bloc['inf_bloc'] = data_bloc['prenom_ibo'] +' '+ data_bloc['nom_ibo']
#data_bloc['inf_bloc2'] = data_bloc['prenom_ibo2'] +' '+ data_bloc['nom_ibo2']
data_bloc['patient'] = data_bloc['prenom'] +' '+ data_bloc['nom']

# Data_cro
#data_cro = data_bloc[(data_bloc['statut_cro'] == 'CRO') & ~(data_bloc['supprimee'] == 'FAUX')]
#end_date_cro = data_bloc['dateoperation'].max()
#data_cro = data_cro[(data_cro['dateoperation'] >= start) & (data_cro['dateoperation'] <= end_date_cro)]

#data_cro['dateoperation'] = pd.to_datetime(data_cro['dateoperation'])
#data_cro['jour'] = data_cro['dateoperation'].dt.day
#data_cro['mois'] = data_cro['dateoperation'].dt.month
#data_cro['année'] = data_cro['dateoperation'].dt.year

#data_cro_service = data_cro[data_cro['module'].isin(selected_service)]

# Data_intervention
# Date



    
#data_cro_service['mois_name'] = data_cro_service.apply(lambda row: f"{calendar.month_name[row['mois']]} {row['année']}", axis=1)
#custom_order = sorted(set(data_cro_service['mois_name']), key=lambda x: (int(x.split()[1]), list(calendar.month_name).index(x.split()[0])))
#data_cro_service['mois_name'] = pd.Categorical(data_cro_service['mois_name'], categories=custom_order, ordered=True)
#cro_per_months = data_cro_service.groupby('mois_name').size().reset_index(name='nombre_cro')
#fig = px.bar(
#    data_cro_service.groupby(['année', 'mois_name', 'module']).size().reset_index(name='nombre_cro'),
#    x='mois_name',
#    y='nombre_cro',
#    title='Nombre CRO générés par mois',
#    labels={'count': 'nombre_cro'},
#)
#fig.update_layout(xaxis_title='Mois', yaxis_title='Nombre CRO générés')
#st.plotly_chart(fig)




# Filter data for each status
start = pd.Timestamp(2023, 4, 28)
end_date_int = data_bloc['dateplanifiee'].max()

data_intervention = data_bloc[data_bloc['statut_int'].notna()]
data_intervention = data_intervention[(data_intervention['dateplanifiee'] >= start) & (data_intervention['dateplanifiee'] <= end_date_int)]

data_intervention['dateplanifiee'] = pd.to_datetime(data_intervention['dateplanifiee'])
data_intervention['jour'] = data_intervention['dateplanifiee'].dt.day
data_intervention['mois'] = data_intervention['dateplanifiee'].dt.month
data_intervention['année'] = data_intervention['dateplanifiee'].dt.year

selected_module = st.sidebar.multiselect("Module", data_bloc['module'].dropna().unique())

if not selected_module:
    # No module selected, show data for all modules
    data_intervention_module = data_intervention
else:
    data_intervention_module = data_intervention[data_intervention['module'].isin(selected_module)]

#st.subheader("Nombre d'interventions")
# Counts
col1, col2, col3 = st.columns(3)
with col1:
    interventions_programmees = data_intervention_module[data_intervention_module['statut_int'].isin(['TERMINEE', 'DEMARREE', 'VALIDEE','PROGRAMMEE','ANNULEE'])]
    nombre_interventions_programmees = interventions_programmees.shape[0]
    st.write(f"Nombre d'interventions programmées : {nombre_interventions_programmees}")
with col2:
    interventions_realisees = data_intervention_module[data_intervention_module['statut_int'].isin(['TERMINEE', 'DEMARREE'])]
    nombre_interventions_realisees = interventions_realisees.shape[0]
    st.write(f"Nombre d'interventions réalisées : {nombre_interventions_realisees}")
with col3:
    interventions_annulees = data_intervention_module[data_intervention_module['statut_int'] =='ANNULEE']
    nombre_interventions_annulees = interventions_annulees.shape[0]
    st.write(f"Nombre d'interventions annulées : {nombre_interventions_annulees}")

data_intervention_module['mois_name'] = data_intervention_module.apply(lambda row: f"{calendar.month_name[row['mois']]} {row['année']}", axis=1)
custom_order = sorted(set(data_intervention_module['mois_name']), key=lambda x: (int(x.split()[1]), list(calendar.month_name).index(x.split()[0])))
data_intervention_module['mois_name'] = pd.Categorical(data_intervention_module['mois_name'], categories=custom_order, ordered=True)

programmees = data_intervention_module[data_intervention_module['statut_int'].isin(['TERMINEE', 'DEMARREE', 'VALIDEE','PROGRAMMEE','ANNULEE'])]
realisees = data_intervention_module[data_intervention_module['statut_int'].isin(['TERMINEE', 'DEMARREE'])]
annulees = data_intervention_module[data_intervention_module['statut_int'] =='ANNULEE']

count_programmees = programmees.groupby('mois_name').size().reset_index(name='nombre_interventions')
count_realisees = realisees.groupby('mois_name').size().reset_index(name='nombre_interventions')
count_annulees = annulees.groupby('mois_name').size().reset_index(name='nombre_interventions')

intervention_salle_service = realisees.groupby(['salle_int', 'service_int']).size().reset_index(name='nombre_interventions_réalisées')

col1, col2 = st.columns(2)
with col1:
    fig = make_subplots(rows=1, cols=1)
    fig.add_trace(go.Bar(x=count_programmees['mois_name'], y=count_programmees['nombre_interventions'], name='Interventions programmées', marker_color='blue'))
    fig.add_trace(go.Bar(x=count_realisees['mois_name'], y=count_realisees['nombre_interventions'], name='Interventions réalisées', marker_color='green'))
    fig.add_trace(go.Bar(x=count_annulees['mois_name'], y=count_annulees['nombre_interventions'], name='Interventions annulées', marker_color='red'))
    fig.update_layout(
        xaxis_title='Mois',
        title='Nombre d\'interventions',
        yaxis_title='Nombre d\'interventions',
        barmode='group',  # Grouped bar mode
    )
    st.plotly_chart(fig)
with col2:
    fig = px.bar(
        intervention_salle_service,
        x='salle_int',
        y='nombre_interventions_réalisées',
        color='service_int',
        title='Nombre d\'interventions réalisées par salle et par service',
        labels={'nombre_interventions_réalisées': 'Nombre d\'interventions réalisées'})
    fig.update_layout(
        xaxis_title='Salle',
        yaxis_title='Nombre d\'interventions réalisées')
    st.plotly_chart(fig)

# TAUX D'OCCUPATION
data_intervention_module['datedebut'] = pd.to_datetime(data_intervention_module['datedebut'])
data_intervention_module['datefin'] = pd.to_datetime(data_intervention_module['datefin'])

data_intervention_module['day_of_week'] = data_intervention_module['datedebut'].dt.dayofweek
data_intervention_module['hour_of_day'] = data_intervention_module['datedebut'].dt.hour

filtered_data = data_intervention_module[
    (data_intervention_module['day_of_week'] >= 0) &  # Monday
    (data_intervention_module['day_of_week'] <= 4) &  # Friday
    (data_intervention_module['hour_of_day'] >= 8) &  # 8:30 AM
    (data_intervention_module['hour_of_day'] <= 16)    # 4:30 PM
]

occupation_rate_data = filtered_data.groupby(['salle_int', filtered_data['datedebut'].dt.to_period("M")])['dureereelle'].sum()

data_intervention_module['availability'] = np.where(data_intervention_module['module'] == 'Urgence', 24 * 60 * 7, (16.5 - 8.5) * 60 * 5)

occupation_rate_data = data_intervention_module.groupby(['salle_int', data_intervention_module['datedebut'].dt.to_period("M")])['dureereelle'].sum()

occupation_rate_data = occupation_rate_data.reset_index()
data_intervention_module = data_intervention_module.reset_index()

occupation_rate_data['occupation_rate'] = (occupation_rate_data['dureereelle'] / data_intervention_module['availability']) * 100
occupation_rate_data['occupation_rate'] = occupation_rate_data['occupation_rate'].clip(upper=100)


occupation_rate_data['datedebut_str'] = occupation_rate_data['datedebut'].astype(str)

fig_occupation_rate = px.line(
    occupation_rate_data,
    x='datedebut_str',
    y='occupation_rate',
    color='salle_int',
    labels={'occupation_rate': "Taux d'occupation (%)", 'salle_int' : "Salle", "datedebut_str": "Date"},
    title="Taux d'occupation par salle",
)

fig_occupation_rate.update_layout(xaxis_title='Month', yaxis_title="Taux d'occupation (%)")
st.plotly_chart(fig_occupation_rate)

# REPARTTION PAR ORGANE
fig_treemap = px.treemap(
    data_intervention_module,
    path=['organe'],
    title='Répartition par organe',
)
st.plotly_chart(fig_treemap)
# Assuming you already have data_intervention_module DataFrame

# Calculate overflow
data_intervention_module['overflow'] = data_intervention_module['dureereelle'] - data_intervention_module['dureeprevue']

# Create a bar chart for global overflow per salle
fig_overflow = px.bar(
    data_intervention_module,
    x='salle_int',
    y='overflow',
    title='Débordement global par salle',
    labels={'overflow': 'Débordement'},
)

# Show the plot
st.plotly_chart(fig_overflow)







all_combinations = pd.DataFrame(
    [(mois_name, salle_int) for mois_name in data_intervention_module['mois_name'].unique() for salle_int in data_intervention_module['salle_int'].unique()],
    columns=['mois_name', 'salle_int']
)

# Merge the existing DataFrame with the complete DataFrame to fill missing combinations
occupation_rate_data = pd.merge(all_combinations, occupation_rate_data, how='left', on=['mois_name', 'salle_int'])

# Fill missing values with 0
occupation_rate_data['occupation_rate'].fillna(0, inplace=True)

# Set a maximum value of 100 for occupation rate
occupation_rate_data['occupation_rate'] = occupation_rate_data['occupation_rate'].clip(upper=100)

# Create a bar chart for occupation rate per salle per month
fig_occupation_rate = px.bar(
    occupation_rate_data,
    x='mois_name',
    y='occupation_rate',
    color='salle_int',
    title='Taux d\'occupation par salle et par mois',
    labels={'occupation_rate': 'Taux d\'occupation'},
)

# Show the plot
st.plotly_chart(fig_occupation_rate)
